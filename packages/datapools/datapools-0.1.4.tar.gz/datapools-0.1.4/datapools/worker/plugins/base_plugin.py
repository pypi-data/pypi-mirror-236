import sys
from typing import List, Union
from urllib.parse import urlparse

import httpx

from ...common.logger import logger
from ...common.storage import BaseStorage
from ...common.types import CrawlerBackTask, CrawlerContent

try:
    from bs4 import BeautifulSoup
except ImportError:
    pass
try:
    from playwright.async_api import Locator, Page, async_playwright
except ImportError:
    pass
import re


class BasePlugin:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    async def download(self, url):
        try:
            async with httpx.AsyncClient(
                max_redirects=5
            ) as client:  # TODO: 5 should be parameter
                r = await client.get(
                    url, follow_redirects=True
                )  # TODO: follow_redirects should be parameter
                return r.content

        except Exception as e:
            logger.error(f"failed get content of {url}: {e}")

    def parse_url(self, url):
        return urlparse(url)

    def is_supported(self, url):
        raise Exception("implement in child class")

    async def process(
        self, url
    ) -> Union[CrawlerContent, CrawlerBackTask]:  # should yield
        raise Exception("implement in child class")

    @staticmethod
    def is_imported(module):
        return module in sys.modules

    @staticmethod
    async def parse_meta_tag(content):
        regexp = re.compile("^https://openlicense.ai/t/(\w+)$")
        if BasePlugin.is_imported("bs4") and type(content) is BeautifulSoup:
            tag = content.find("meta", attrs={"content": regexp})
            if tag is not None:
                return tag.group(1)
        if (
            BasePlugin.is_imported("playwright.async_api")
            and type(content) is Page
        ):
            metas = content.locator('meta[name="robots"]')
            for meta in await metas.all():
                c = await meta.get_attribute("content")
                tag = regexp.match(c)
                if tag is not None:
                    return tag.group(1)
