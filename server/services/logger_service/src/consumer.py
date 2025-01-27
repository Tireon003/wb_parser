from collections.abc import Callable
from aiormq.abc import DeliveredMessage, CallbackCoro

from config import settings
from src.broker import RabbitManager


class LogConsumer(RabbitManager):

    async def listen_logs(
        self,
        on_message: Callable[[DeliveredMessage], CallbackCoro],
    ) -> None:
        async with self.get_channel() as channel:
            await channel.basic_qos(prefetch_count=1)
            await channel.exchange_declare(
                exchange="logs",
                exchange_type="direct",
            )
            declared_queue = await channel.queue_declare(
                queue=settings.LOGGER_QUEUE_NAME,
                durable=True,
                auto_delete=False,
            )
            await channel.queue_bind(
                queue=declared_queue.queue,
                exchange="logs",
                routing_key=declared_queue.queue,
            )
            await channel.basic_consume(
                queue=declared_queue.queue,
                consumer_callback=on_message,
                no_ack=True,
            )
