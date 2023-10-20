import asyncio
import traceback
from enum import Enum
from typing import List, Union

import aio_pika
import aiormq
from pydantic import BaseModel

from ..logger import logger
from ..stoppable import Stoppable
from .types import QueueRole, QueueTopicMessage


class RabbitmqParams(BaseModel):
    exchange_type: str = "direct"
    exchange_name: str = ""
    routing_key: Union[str, List[str]] = ""


class RabbitmqQueue(Stoppable):
    def __init__(
        self,
        role: QueueRole,
        connection_url: str,
        queue_name: str,
        params: RabbitmqParams = RabbitmqParams(),
    ):
        super().__init__()
        self.role = role
        self.url = connection_url
        self.params = params
        self.queue_name = queue_name  # rabbitmq router_key
        self.internal_queue = asyncio.Queue()
        self.ready_state = {
            self.role: asyncio.Event()
        }  # dict is for future: may support both server+client
        self.is_working = asyncio.Lock()

    def run(self):
        if self.role == QueueRole.Publisher:
            self.tasks.append(asyncio.create_task(self.server_loop()))
        else:
            self.tasks.append(asyncio.create_task(self.client_loop()))
        super().run()

    async def stop(self):
        await self.internal_queue.join()
        await super().stop()

    async def push(self, data):
        await self.internal_queue.put(data)

    async def pop(self, timeout=None):
        if timeout is None:
            return await self.internal_queue.get()
        try:
            async with asyncio.timeout(timeout):
                return await self.internal_queue.get()
        except TimeoutError:
            return None

    async def mark_done(self, message):
        await message.ack()

    async def reject(self, message):
        await message.reject()

    async def is_ready(self):
        await self.ready_state[self.role].wait()

    async def server_loop(self):
        try:
            while not await self.is_stopped():
                try:
                    connection = await aio_pika.connect_robust(self.url)
                except aiormq.exceptions.AMQPConnectionError:
                    logger.info("Failed connect to rabbitmq, waiting..")
                    await asyncio.sleep(5)  # TODO
                    continue

                logger.info(f"rabbitmq {connection=} --------------------")

                async with connection:
                    channel = await connection.channel()
                    logger.info(f"rabbitmq {channel=} ----------------------")

                    if (
                        self.params.exchange_type
                        == aio_pika.ExchangeType.DIRECT
                    ):
                        exchange = channel.default_exchange
                    else:
                        exchange = await channel.declare_exchange(
                            name=self.params.exchange_name,
                            type=self.params.exchange_type,
                        )

                    self.ready_state[QueueRole.Publisher].set()

                    try:
                        while not await self.is_stopped():
                            message = await self.pop(1)
                            if message is not None:
                                # logger.info( f'-------------------publishing msg {message.encode()}')

                                if type(message) is QueueTopicMessage:
                                    routing_key = ".".join(message.topic)
                                else:
                                    routing_key = self.queue_name

                                # logger.info( f'publishing into {exchange=} {routing_key=}')
                                await exchange.publish(
                                    aio_pika.Message(
                                        body=message.encode(),
                                        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                                    ),
                                    routing_key=routing_key,
                                )
                                # logger.info( f'published')

                                self.internal_queue.task_done()

                    except Exception as e:
                        logger.error(
                            f"!!!!!!!!!!!!!!!!!! exception in RabbitmqQueue::server_loop"
                        )
                        logger.error(traceback.format_exc())

                self.ready_state[QueueRole.Publisher].clear()

        except Exception as e:
            logger.error(f"!!!!!!!!!!!!!!!!!! exception in rabbitmq")
            logger.error(traceback.format_exc())

    async def receive_message(
        self, message: aio_pika.abc.AbstractIncomingMessage
    ) -> None:
        logger.info(
            "RABBITMQ income message --------------------------------------------------"
        )
        logger.info(message.body)
        await self.push(message)

    async def client_loop(self):
        try:
            while not await self.is_stopped():
                try:
                    connection = await aio_pika.connect_robust(self.url)
                except aiormq.exceptions.AMQPConnectionError:
                    logger.info("Failed connect to rabbitmq, waiting..")
                    await asyncio.sleep(5)
                    continue

                logger.info(f"rabbitmq {connection=} -----------------------")

                try:
                    # Creating channel
                    channel = await connection.channel()
                    logger.info(f"rabbitmq {channel=} ----------------------")

                    # Maximum message count which will be processing at the same time.
                    await channel.set_qos(prefetch_count=1)

                    # Declaring queue
                    queue = await channel.declare_queue(
                        self.queue_name, durable=True
                    )
                    if (
                        self.params.exchange_type
                        == aio_pika.ExchangeType.TOPIC
                    ):
                        await channel.declare_exchange(
                            name=self.params.exchange_name,
                            type=aio_pika.ExchangeType.TOPIC,
                        )
                        if type(self.params.routing_key) is not list:
                            await queue.bind(
                                self.params.exchange_name,
                                routing_key=self.params.routing_key,
                            )
                        else:
                            for rk in self.params.routing_key:
                                await queue.bind(
                                    self.params.exchange_name, routing_key=rk
                                )
                    self.ready_state[QueueRole.Receiver].set()

                    logger.info(
                        "rebbigmq consume start----------------------------"
                    )

                    await queue.consume(self.receive_message)

                    await self.stop_event.wait()

                    logger.info(
                        "rebbigmq consume done----------------------------"
                    )
                except Exception as e:
                    logger.error(
                        f"!!!!!!!!!!!!!!!!!! exception in rabbitmq consume"
                    )
                    logger.error(traceback.format_exc())

                self.ready_state[QueueRole.Receiver].clear()
        except Exception as e:
            logger.error(f"!!!!!!!!!!!!!!!!!! exception in rabbitmq")
            logger.error(traceback.format_exc())
