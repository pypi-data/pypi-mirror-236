import json
from enum import Enum

from ..logger import logger


class QueueRole(Enum):
    Publisher = 1
    Receiver = 2


class QueueMessageType(Enum):
    Task = 1
    Report = 2
    StorageInvalidation = 3


class QueueMessage:
    def __init__(self, type: QueueMessageType, data):
        self.type = type
        self.data = data

    def encode(self):
        # logger.info( f'encoding {self.type=} {self.data=}')
        return json.dumps(
            {"type": self.type.value, "data": json.dumps(self.data)}
        ).encode()

    @staticmethod
    def decode(binary):
        j = json.loads(binary.decode())
        res = QueueMessage(
            type=QueueMessageType(j["type"]), data=json.loads(j["data"])
        )
        return res


class QueueTopicMessage:
    def __init__(self, topic, data):
        self.topic = topic.split(".")
        self.data = data

    def encode(self):
        # logger.info( f'encoding {self.type=} {self.data=}')
        return json.dumps({"data": json.dumps(self.data)}).encode()

    @staticmethod
    def decode(topic, binary):
        j = json.loads(binary.decode())
        res = QueueTopicMessage(topic=topic, data=json.loads(j["data"]))
        return res
