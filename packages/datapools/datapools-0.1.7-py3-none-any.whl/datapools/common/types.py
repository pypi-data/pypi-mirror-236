from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import AnyUrl, BaseModel, BaseSettings

QUEUE_WORKER_TASKS = "worker_tasks"
QUEUE_REPORTS = "worker_reports"
QUEUE_EVAL_TASKS = "eval_tasks"
TOPICS_EXCHANGE_NAME = "topics_exchange"


class CrawlerSettings(BaseSettings):
    RABBITMQ_CONNECTION_URL: str = "amqp://guest:guest@rabbitmq.crawler/"
    BACKEND_API_URL: str = "https://openlicense.ai/openlicense/api/"
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    BACKEND_HINTS_PERIOD: int = 10  # seconds


class WorkerSettings(BaseSettings):
    RABBITMQ_CONNECTION_URL: str = "amqp://guest:guest@rabbitmq.crawler/"
    ATTEMPTS_PER_URL: int = 3
    ATTEMPTS_DELAY: int = 5  # seconds
    STORAGE_PATH: str = "/storage/"


class BaseProducerSettings(BaseSettings):
    RABBITMQ_CONNECTION_URL: str = "amqp://guest:guest@rabbitmq.crawler/"
    BACKEND_API_URL: str = "https://openlicense.ai/openlicense/api/"
    STORAGE_PATH: str = "/storage/"
    WORKER_STORAGE_PATH: str = "/worker_storage/"


class CrawlerHintURLStatus(Enum):
    Unprocessed = 0
    Success = 1
    Failure = 2
    Processing = 3
    Rejected = 4


class DatapoolContentType(Enum):
    Text = "Text"
    Image = "Image"
    Video = "Video"
    Audio = "Audio"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        if self.value == DatapoolContentType.Text:
            return 1
        if self.value == DatapoolContentType.Image:
            return 2
        if self.value == DatapoolContentType.Video:
            return 3
        if self.value == DatapoolContentType.Audio:
            return 4
        raise Exception(
            f"Not supported DatapoolContentType __hash__ {self.value}"
        )


class CrawlerContent(BaseModel):
    tag_id: str
    type: DatapoolContentType
    storage_id: Any
    url: str

    def to_dict(self):
        res = self.__dict__
        res["type"] = res["type"].value
        return res


class CrawlerBackTask(BaseModel):
    url: str

    def to_dict(self):
        res = self.__dict__
        return res


class CrawlerNop:
    pass


class Evaluation(BaseModel):
    nsfw: bool
    score: float
    weight: float

    # def to_dict(self):
    #     return {
    #         'nsfw': self.nsfw,
    #         'score': self.score,
    #         'weight': self.weight
    #     }


class DatapoolRules(BaseModel):
    content_type: Union[List[DatapoolContentType], DatapoolContentType]
    domain: Optional[Union[List[AnyUrl], AnyUrl]]


class DatapoolRuleMatch(BaseModel):
    content_type: DatapoolContentType
    url: AnyUrl
