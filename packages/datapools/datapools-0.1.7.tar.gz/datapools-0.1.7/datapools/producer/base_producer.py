import asyncio
import importlib
import inspect
import os
import sys
import traceback
from enum import Enum
from typing import Any

import aio_pika
from pydantic import BaseModel

from ..common.backend_api import BackendAPI, TagDatapools
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
from ..common.storage.file_storage import FileStorage
from ..common.types import *
from ..worker import CrawlerWorker
from .rules import *


class BaseProducer(Stoppable):
    def __init__(self, cfg: BaseProducerSettings = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else BaseProducerSettings()
        self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)
        self.storage = FileStorage(self.cfg.STORAGE_PATH)

        # receives tasks from workers
        self.eval_queue = RabbitmqQueue(
            QueueRole.Receiver,
            self.cfg.RABBITMQ_CONNECTION_URL,
            QUEUE_EVAL_TASKS,
        )

        # will wait messages from workers
        self.todo_queue = RabbitmqQueue(
            QueueRole.Publisher,
            self.cfg.RABBITMQ_CONNECTION_URL,
            QUEUE_WORKER_TASKS,
        )

        # will invalidate worker cache entries
        self.topics_queue = RabbitmqQueue(
            QueueRole.Publisher,
            self.cfg.RABBITMQ_CONNECTION_URL,
            None,
            RabbitmqParams(
                exchange_type=aio_pika.ExchangeType.TOPIC,
                exchange_name=TOPICS_EXCHANGE_NAME,
            ),
        )
        self.datapool_rules_checker = DatapoolRulesChecker()

    def run(self):
        self.tasks.append(asyncio.create_task(self.router_loop()))
        self.eval_queue.run()
        self.topics_queue.run()
        super().run()

    async def stop(self):
        await self.eval_queue.stop()
        await self.topics_queue.stop()
        await super().stop()

    async def router_loop(self):
        try:
            while not await self.is_stopped():
                message = await self.eval_queue.pop(timeout=1)
                if message:
                    qm = QueueMessage.decode(message.body)
                    try:
                        assert qm.type == QueueMessageType.Task

                        task = qm.data
                        logger.info(f"Producer got: {task}")

                        # TODO: this storage must be associated with the worker!
                        #   For example, storage path or url can be formatted accordingly to worker id
                        worker_storage = FileStorage(
                            self.cfg.WORKER_STORAGE_PATH
                        )
                        raw_data = await worker_storage.get(task["storage_id"])

                        datapools = await self._get_tag_datapools(
                            task["tag_id"]
                        )
                        logger.info(f"tag_id {task['tag_id']} in {datapools=}")
                        for datapool_data in datapools:
                            logger.info(
                                f"matching content for {datapool_data['id']=}"
                            )
                            against = DatapoolRuleMatch(
                                content_type=task[
                                    "type"
                                ],  # DatapoolContentType
                                url=task[
                                    "parent_url"
                                ],  # for image it should be site image, not image src itself
                            )
                            content_rules = DatapoolRules(
                                **datapool_data["rules"]
                            )
                            if self.datapool_rules_checker.match(
                                content_rules, against
                            ):
                                logger.info("matched")
                                await self.process_content(
                                    datapool_data["id"], raw_data, task
                                )
                            else:
                                logger.info("not matched")

                            # evaluation = await self.evaluator.process( raw_data, DatapoolContentType( task[ 'type' ] ) )
                            # logger.info( f'{evaluation=}')
                            # await self._add_datapool_content( datapool_id, raw_data, task, evaluation )

                        # tell worker that his storage item can be removed
                        await self.topics_queue.push(
                            QueueTopicMessage(
                                CrawlerWorker.get_storage_invalidation_topic(
                                    task["worker_id"]
                                ),
                                {"storage_id": task["storage_id"]},
                            )
                        )

                        await self.eval_queue.mark_done(message)
                    except Exception as e:
                        logger.error(f"Catched: {traceback.format_exc()}")
                        logger.error(f"failed evaluate {e}")
                        await self.eval_queue.reject(message)

        except Exception as e:
            logger.error(f"Catched: {traceback.format_exc()}")
            logger.error(f"!!!!!!! Exception in Datapools::router_loop() {e}")

    async def _get_tag_datapools(self, tag_id) -> TagDatapools:
        # TODO: tag_id: datapool_ids pairs should be cached with cache TTL:
        #   CACHE CONSIDERATION: user may leave datapool while datapool_id may still be associated with tag_id in cache
        return await self.api.get_tag_datapools(tag_id)

    async def process_content(self, datapool_id, raw_data, task):
        # put data into persistent storage
        await self.storage.put(
            task["storage_id"], raw_data
        )  # TODO: consider using datapool_id
