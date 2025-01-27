import aiohttp

from config import settings
from src.schemas import Good
from .exc import ParseFailedException, SaveFailedException


class ParserService:

    @staticmethod
    async def parse_card(article: int) -> Good:
        url = f"{settings.parser_service_url}/api/parser/article/{article}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                body = await response.json()
                if response.status == 200:
                    return Good(**body["info"])
                else:
                    raise ParseFailedException(detail=body)

    @staticmethod
    async def save_to_sheets(good: Good) -> None:
        url = f"{settings.parser_service_url}/api/sheets/add"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=good.model_dump()) as response:
                body = await response.json()
                if response.status == 200:
                    return
                else:
                    raise SaveFailedException(detail=body)
