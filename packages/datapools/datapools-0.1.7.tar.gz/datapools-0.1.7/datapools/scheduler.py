import asyncio
import json
import time
import traceback
from typing import Union

import httpx

from .common.backend_api import BackendAPI
from .common.logger import logger
from .common.queues import (
    QueueMessage,
    QueueMessageType,
    QueueRole,
    RabbitmqQueue,
)
from .common.stoppable import Stoppable
from .common.tasks_db import Hash
from .common.tasks_db.redis import RedisTasksDB
from .common.types import *


class CrawlerScheduler(Stoppable):
    # 1. task:
    #   - get hint urls from the backend, put into tasks_db, status is changed at the backend at once
    #   - check "processing" tasks: ping worker. If it's dead then task is moved back to the queue
    # 2. api: get urls from workers, put into tasks_db
    #   tips:
    #   - reject existing urls: request redis by url hash
    # 3. api: worker gets a new task(s?) from queue:
    #   tips:
    #   - tasks_db: (redis) task should be moved into a separate key as "in progress", worker ID/IP/etc should be remembered to be able to ping
    # 4. api: worker notifies about finished task
    #    - remove task from "processing"
    #    - if it's a backend hint url, then update its status by calling backend api

    def __init__(self, cfg: CrawlerSettings = None):
        super().__init__()
        self.cfg = cfg if cfg is not None else CrawlerSettings()
        self.api = BackendAPI(url=self.cfg.BACKEND_API_URL)
        self.tasks_db = RedisTasksDB(
            host=self.cfg.REDIS_HOST, port=self.cfg.REDIS_PORT
        )
        self.todo_queue = RabbitmqQueue(
            QueueRole.Publisher,
            self.cfg.RABBITMQ_CONNECTION_URL,
            QUEUE_WORKER_TASKS,
        )
        self.reports_queue = RabbitmqQueue(
            QueueRole.Receiver, self.cfg.RABBITMQ_CONNECTION_URL, QUEUE_REPORTS
        )

    def run(self):
        self.tasks.append(asyncio.create_task(self.hints_loop()))
        self.tasks.append(asyncio.create_task(self.reports_loop()))
        self.todo_queue.run()
        self.reports_queue.run()
        super().run()

    async def stop(self):
        await self.todo_queue.stop()
        await self.reports_queue.stop()
        await super().stop()

    async def _set_task_status(self, data):
        # hash, status: CrawlerHintURLStatus, contents
        logger.info(f"set_task_status: {data=}")
        task = data["task"]
        status = CrawlerHintURLStatus(data["status"])
        # contents = data[ 'contents' ]

        if status == CrawlerHintURLStatus.Success:
            logger.info(f"------------------ task done --------------------")
            self.tasks_db.set_done(task["_hash"])

        if "user_id" in task:
            logger.info(f"--------------- set hint url status {status}")
            # this is hint url from server => have to update status on the backend
            await self.api.set_hint_url_status(task["id"], status)

        # if contents:
        #     logger.info( f'----------------- pushing contents {contents=}' )
        #     await self.api.add_crawler_contents( contents )

    async def _add_task(self, task, ignore_existing=False, ignore_done=False):
        # puts task to the todo_queue if it does not exist in new/done list
        hash = self.tasks_db.add(
            task, ignore_existing=ignore_existing, ignore_done=ignore_done
        )
        if hash:
            task["_hash"] = hash
            await self.todo_queue.push(
                QueueMessage(type=QueueMessageType.Task, data=task)
            )
            return hash
        return False

    async def hints_loop(self):
        # infinitely fetching URL hints by calling backend api
        try:
            while not await self.is_stopped():
                if self.tasks_db.is_ready():
                    try:
                        hints = await self.api.get_hint_urls(limit=10)
                    except Exception as e:
                        logger.error(f"Failed get hints: {e}")
                        hints = None

                    # logger.info( f'got hints: {hints}')
                    if type(hints) is list:
                        for hint in hints:
                            logger.info(f"got hint: {hint}")

                            ignore_existing = True  # TODO: for tests only!
                            if not await self._add_task(
                                hint,
                                ignore_existing=ignore_existing,
                                ignore_done=True,
                            ):
                                await self.api.set_hint_url_status(
                                    hint["id"], CrawlerHintURLStatus.Rejected
                                )
                await asyncio.sleep(self.cfg.BACKEND_HINTS_PERIOD)
        except Exception as e:
            logger.error(
                f"!!!!!!! Exception in CrawlerScheduler::hints_loop() {e}"
            )
            logger.error(traceback.format_exc())

    async def reports_loop(self):
        # receive reports from workers
        try:
            while not await self.is_stopped():
                message = await self.reports_queue.pop(timeout=1)
                if message:
                    try:
                        qm = QueueMessage.decode(message.body)
                        if qm.type == QueueMessageType.Task:
                            logger.info("new task from worker")
                            logger.info(f"{qm=}")
                            await self._add_task(qm.data)
                        elif qm.type == QueueMessageType.Report:
                            await self._set_task_status(qm.data)
                        else:
                            logger.error(f"Unsupported QueueMessage {qm=}")

                    except Exception as e:
                        logger.error(f"Failed decode process report")
                        logger.error(traceback.format_exc())

                    await self.reports_queue.mark_done(message)

        except Exception as e:
            logger.error(
                f"!!!!!!! Exception in CrawlerScheduler::reports_loop() {e}"
            )
            logger.error(traceback.format_exc())
