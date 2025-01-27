from typing import TYPE_CHECKING
import aiofiles
import logging
from datetime import datetime as dt

if TYPE_CHECKING:
    from aiormq.abc import DeliveredMessage

log = logging.getLogger(__name__)


class Logger:

    @staticmethod
    async def write_log(msg: "DeliveredMessage") -> None:
        date = dt.now()
        log.info(
            "Log handled at %s",
            date.strftime("%Y.%m.%d %H:%M:%S"),
        )
        async with aiofiles.open(
            file=f"./logs/{date.strftime('%Y%m%d')}.log",
            mode="a",
        ) as file:
            log_text = "{} {}\n".format(
                date.strftime("%Y.%m.%d %H:%M:%S"), msg.body.decode("utf-8")
            )
            await file.write(log_text)
