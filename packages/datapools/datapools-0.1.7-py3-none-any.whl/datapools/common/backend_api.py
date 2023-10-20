from typing import List

import httpx
from pydantic import BaseConfig, BaseModel

from ..common.logger import logger
from ..common.types import CrawlerHintURLStatus, DatapoolRules


class TagDatapools(BaseModel):
    id: int
    content_rules: DatapoolRules

    class BaseConfig:
        validate_assignment = True


class BackendAPI:
    def __init__(self, url):
        self.url = url

    async def get_hint_urls(self, limit):
        return await self.get_uri("get-hint-urls", {"limit": limit})

    async def set_hint_url_status(self, id, status: CrawlerHintURLStatus):
        return await self.get_uri(
            "set-hint-url-status", {"id": id, "status": status.value}
        )

    # async def add_crawler_contents( self, contents: dict ):
    #     return await self.get_uri( 'add-crawler-contents', { 'contents': contents } )

    # async def get_crawled_contents(self, limit):
    #     return await self.get_uri( 'get-crawled-contents', { 'limit': limit } )

    async def add_datapool_content(self, data):
        return await self.get_uri("add-datapool-content", data)

    async def get_tag_datapools(self, tag_id) -> TagDatapools:
        return await self.get_uri(
            f"get-tag-datapools", {"filter": {"tag_id": tag_id}}
        )

    async def get_uri(self, uri, data={}):
        async with httpx.AsyncClient() as client:
            url = self.url + uri
            logger.info(f"posting to {url=} {data=}")

            r = await client.post(url, json=data)
            if r.status_code == 200:
                return r.json()
            else:
                logger.error(f"Non 200 http response {r=}")
                raise Exception("non 200 response")
