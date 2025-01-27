from aiormq import spec

from config import settings
from src.core import RabbitManager


class LogProducer(RabbitManager):
    """Class extends RabbitManager and provide tools for logging errors"""

    async def send_log(self, message: str) -> None:
        async with self._get_channel() as channel:
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
            await channel.basic_publish(
                body=message.encode(),
                exchange="logs",
                routing_key=declared_queue.queue,
                properties=spec.Basic.Properties(delivery_mode=2),
            )
