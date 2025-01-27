from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Self

import aiormq
from aiormq.abc import AbstractConnection, AbstractChannel

from config import settings


class RabbitManager:
    """Class contains general tools for working with RabbitMQ"""

    def __init__(self, connection: AbstractConnection) -> None:
        self._connection = connection

    @classmethod
    async def init(cls, url: str = settings.rmq_url) -> Self:
        connection = await aiormq.connect(url=url)
        return cls(connection)

    @asynccontextmanager
    async def _get_channel(self) -> AsyncIterator[AbstractChannel]:
        channel: AbstractChannel = await self._connection.channel()
        try:
            yield channel
        finally:
            await channel.close()

    @classmethod
    @asynccontextmanager
    async def get_instance(cls) -> AsyncIterator[Self]:
        instance = await cls.init()
        try:
            yield instance
        finally:
            await instance._connection.close()
