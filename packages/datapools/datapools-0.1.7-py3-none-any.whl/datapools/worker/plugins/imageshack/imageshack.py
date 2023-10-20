import asyncio
import traceback
from typing import List

import httpx
from bs4 import BeautifulSoup

from ....common.logger import logger
from ....common.storage import BaseStorage
from ....common.types import (
    CrawlerBackTask,
    CrawlerContent,
    DatapoolContentType,
)
from ..base_plugin import BasePlugin


class ImageshackPlugin(BasePlugin):
    def __init__(self, storage):
        super().__init__(storage)

    def is_supported(self, url):
        u = self.parse_url(url)
        # logger.info( f'imageshack {u=}')
        return u.netloc == "imageshack.com"

    async def process(self, url) -> CrawlerContent:
        logger.info(f"imageshack::process({url})")

        # async with httpx.AsyncClient() as client:
        #     logger.info( f'loading url {url}')

        #     r = await client.get( url )
        #     #logger.info( f'got Response {r}')
        #     r = r.text
        logger.info(f"loading url {url}")
        r = await self.download(url)
        # logger.info( f'text: {r}')
        logger.info(f"got url content length={len(r)}")

        soup = BeautifulSoup(r, "html.parser")

        # check if <meta/> tag exists with our tag
        # header_tag_id = await BasePlugin.parse_meta_tag(soup)
        # if not header_tag_id:
        #     logger.info("No <meta> tag found, give up")
        #     return
        header_tag_id = "a35"  # FIXME: use a real tag!!!

        tag_id = header_tag_id

        # 1.search for photo LINKS and return them as new tasks
        links = soup.body.find_all("a", attrs={"class": "photo"})

        for l in links:
            yield CrawlerBackTask(url="https://imageshack.com" + l["href"])

        # 2. search for photo IMAGES
        img = soup.body.find("img", attrs={"id": "lp-image"})
        if img:
            logger.info(f'found image {img["src"]}')

            url = "https://imageshack.com" + img["src"]
            content = await self.download(url)
            if content:
                storage_id = BaseStorage.gen_id(url)

                try:
                    await self.storage.put(storage_id, content)

                    yield CrawlerContent(
                        tag_id=tag_id,
                        type=DatapoolContentType.Image,
                        storage_id=storage_id,
                        url=url,
                    )
                except Exception as e:
                    logger.error(f"failed put to storage {e}")
                    logger.error(traceback.format_exc())

                await asyncio.sleep(2)

            else:
                logger.error(f"failed download image")
