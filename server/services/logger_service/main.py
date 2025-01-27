import asyncio
import logging

from config import settings
from src import LogConsumer, Logger


def init_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
    )


async def main() -> None:
    init_logging()
    async with LogConsumer.get_instance() as log_consumer:
        logging.warning("Started listening logs")
        while True:
            await log_consumer.listen_logs(on_message=Logger.write_log)
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
