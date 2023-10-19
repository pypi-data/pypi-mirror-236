import asyncio
import importlib
import inspect
import os
import sys
import time
import traceback
import uuid

import aio_pika
import httpx

from ..common.logger import logger
from ..common.queues import (
    QueueMessage,
    QueueMessageType,
    QueueRole,
    QueueTopicMessage,
    RabbitmqParams,
    RabbitmqQueue,
)
from ..common.stoppable import Stoppable
from ..common.storage import FileStorage
from ..common.types import *


class CrawlerWorker(Stoppable):
    def __init__(self, cfg: WorkerSettings = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else WorkerSettings()
        self.id = uuid.uuid4().hex
        logger.info(f"worker id={self.id}")
        self.storage = FileStorage(self.cfg.STORAGE_PATH)
        self.init_plugins()
        self.todo_queue = RabbitmqQueue(
            QueueRole.Receiver,
            self.cfg.RABBITMQ_CONNECTION_URL,
            QUEUE_WORKER_TASKS,
        )
        self.reports_queue = RabbitmqQueue(
            QueueRole.Publisher,
            self.cfg.RABBITMQ_CONNECTION_URL,
            QUEUE_REPORTS,
        )
        self.producer_queue = RabbitmqQueue(
            QueueRole.Publisher,
            self.cfg.RABBITMQ_CONNECTION_URL,
            QUEUE_EVAL_TASKS,
        )
        self.topics_queue = RabbitmqQueue(
            QueueRole.Receiver,
            self.cfg.RABBITMQ_CONNECTION_URL,
            "",
            RabbitmqParams(
                exchange_type=aio_pika.ExchangeType.TOPIC,
                exchange_name=TOPICS_EXCHANGE_NAME,
                routing_key=CrawlerWorker.get_storage_invalidation_topic(
                    self.id
                ),
            ),
        )

    def run(self):
        # self.tasks.append( asyncio.create_task( self.tasks_fetcher_loop() ) )
        self.todo_queue.run()
        self.reports_queue.run()
        self.producer_queue.run()
        self.topics_queue.run()
        self.tasks.append(asyncio.create_task(self.worker_loop()))
        self.tasks.append(asyncio.create_task(self.topics_loop()))
        super().run()

    async def stop(self):
        await self.todo_queue.stop()
        await self.reports_queue.stop()
        await self.producer_queue.stop()
        await self.topics_queue.stop()
        await super().stop()

    def init_plugins(self):
        self.plugins = []
        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")

        for dir in os.listdir(plugins_dir):
            if dir != "__pycache__" and os.path.isdir(
                os.path.join(plugins_dir, dir)
            ):
                logger.info(f"loading module {dir}")
                module = importlib.import_module(
                    f"datapools.worker.plugins.{dir}"
                )
                clsmembers = inspect.getmembers(module, inspect.isclass)
                # logger.info( f'{clsmembers=}')

                for cls in clsmembers:
                    for base in cls[1].__bases__:
                        # logger.info( f'{base=}')
                        if base.__name__ == "BasePlugin":
                            # logger.info( f'valid plugin class {cls[1]}')
                            self.plugins.append(cls)
                            break

    async def topics_loop(self):
        # receives storage_id which content can be removed from Evaluator
        try:
            while not await self.is_stopped():
                message = await self.topics_queue.pop(timeout=1)
                if message:
                    qm = QueueTopicMessage.decode(
                        message.routing_key, message.body
                    )
                    if (
                        message.routing_key
                        == CrawlerWorker.get_storage_invalidation_topic(
                            self.id
                        )
                    ):
                        logger.info(
                            f"invalidating storage {qm.data[ 'storage_id' ]}"
                        )
                        await self.storage.remove(qm.data["storage_id"])

                        await self.topics_queue.mark_done(message)
                    else:
                        logger.error(
                            f"!!!!!!!!!!!!!!! BUG: unexpected topic {message=} {qm=}"
                        )
                        await self.topics_queue.reject(message)
        except Exception as e:
            logger.error(f"!!!!!!!!Exception in topics_loop() {e}")
            logger.error(traceback.format_exc())

    async def worker_loop(self):
        # fetches urls one by one from the queue and scans them using available plugins
        try:
            while not await self.is_stopped():
                message = await self.todo_queue.pop(timeout=1)
                if message:
                    qm = QueueMessage.decode(message.body)

                    if qm.type == QueueMessageType.Task:
                        task = qm.data
                        logger.info(f"got {task=}")
                        url = task["url"]
                        logger.info(f"processing {url=}")

                        plugin = self.get_url_plugin(url)
                        logger.info(f"suitable {plugin=}")

                        done = False
                        for attempt in range(0, self.cfg.ATTEMPTS_PER_URL):
                            if attempt > 0:
                                logger.info(f"{attempt=}")

                            try:
                                async for content_or_task in plugin.process(
                                    url
                                ):
                                    # logger.info( f'{type( content_or_task )=}')
                                    t = type(content_or_task)
                                    # logger.info( f'{(t is CrawlerNop)=}')
                                    if t is CrawlerContent:
                                        await self._set_task_status(
                                            task,
                                            CrawlerHintURLStatus.Processing,
                                        )

                                        # notifying datapool pipeline about new crawled data
                                        await self.producer_queue.push(
                                            QueueMessage(
                                                QueueMessageType.Task,
                                                {
                                                    "parent_url": url,
                                                    "url": content_or_task.url,
                                                    "storage_id": content_or_task.storage_id,
                                                    "tag_id": content_or_task.tag_id,
                                                    "type": DatapoolContentType(
                                                        content_or_task.type
                                                    ).value,
                                                    "worker_id": self.id,
                                                },
                                            )
                                        )

                                    elif t is CrawlerBackTask:
                                        await self._add_back_task(
                                            content_or_task
                                        )
                                    elif t is CrawlerNop:
                                        pass
                                    else:
                                        raise Exception(
                                            f"unknown {content_or_task=}"
                                        )
                                    # logger.info( '=================================== process iteration done')

                                logger.info("plugin.process done")
                                await self._set_task_status(
                                    task, CrawlerHintURLStatus.Success
                                )

                                done = True
                                break
                            except Exception as e:
                                logger.error(f"failed get url: {e}")
                                logger.error(traceback.format_exc())
                                await asyncio.sleep(self.cfg.ATTEMPTS_DELAY)
                            if done:
                                break
                        if done:
                            logger.info(
                                f"sending ack for {message.message_id}"
                            )
                            await self.todo_queue.mark_done(message)
                        else:
                            await self.todo_queue.reject(message)
                            await self._set_task_status(
                                task, CrawlerHintURLStatus.Failure
                            )
                    else:
                        logger.error(
                            f"!!!!!!!!!!!!!!! BUG: unexpected {message=} {qm=}"
                        )
                        await self.todo_queue.reject(message)

        except Exception as e:
            logger.error(f"!!!!!!!!Exception in worker_loop() {e}")
            logger.error(traceback.format_exc())

    # async def _set_task_status( self, task, status: CrawlerHintURLStatus, contents = None ):
    #     await self.reports_queue.push( QueueMessage( QueueMessageType.Report, { 'task': task, 'status': status.value, 'contents': contents } ) )

    async def _set_task_status(self, task, status: CrawlerHintURLStatus):
        await self.reports_queue.push(
            QueueMessage(
                QueueMessageType.Report, {"task": task, "status": status.value}
            )
        )

    async def _add_back_task(self, task: CrawlerBackTask):
        await self.reports_queue.push(
            QueueMessage(QueueMessageType.Task, task.to_dict())
        )

    def get_url_plugin(self, url):
        default_obj = None
        for cls in self.plugins:
            obj = cls[1](self.storage)
            if cls[0] != "DefaultPlugin":
                if obj.is_supported(url):
                    return obj
            else:
                default_obj = obj
        return default_obj

    @staticmethod
    def get_storage_invalidation_topic(id):
        return (
            f"worker.id_{id}.type_{QueueMessageType.StorageInvalidation.value}"
        )
