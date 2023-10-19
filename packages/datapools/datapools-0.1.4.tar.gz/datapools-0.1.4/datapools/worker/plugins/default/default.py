from ....common.logger import logger
from ..base_plugin import BasePlugin


class DefaultPlugin(BasePlugin):
    def __init__(self, storage):
        super().__init__(storage)

    def is_supported(self, url):
        return True

    async def process(self, url):
        raise Exception("DefaultPlugin::process() is not implemented")
