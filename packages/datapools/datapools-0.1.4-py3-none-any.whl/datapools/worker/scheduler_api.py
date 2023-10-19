from typing import Union

import httpx

from ..common.logger import logger
from ..common.types import CrawlerHintURLStatus, Evaluation


class SchedulerAPI:
    def __init__(self, url, worker_id):
        self.url = url
        self.worker_id = worker_id

    async def fetch_task(self):
        return await self.get_uri("fetch-task", {})

    async def set_task_status(
        self, task_id, status: CrawlerHintURLStatus, contents: list = []
    ):
        return await self.get_uri(
            "set-task-status",
            {"id": task_id, "status": status.value, "contents": contents},
        )

    async def add_task(self, url):
        return await self.get_uri("add-task", {"url": url})

    async def get_uri(self, uri, data) -> Union[dict, False]:
        async with httpx.AsyncClient() as client:
            url = self.url + uri
            logger.info(f"posting to {url=} {data=}")
            try:
                r = await client.post(
                    url, json=data, headers={"X-Worker-ID": self.worker_id}
                )

                if r.status_code == 200:
                    logger.info(f"response: {r.json()=}")
                    return r.json()
                else:
                    logger.error(f"Error response: {r}")
            except (httpx.ConnectError, httpx.ConnectTimeout) as e:
                logger.info("failed connect scheduler")
            return False
