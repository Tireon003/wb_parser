from typing import Any
import aiohttp

from config import settings
from src.schemas.good_schemas import Good


class ParserAPI:

    @staticmethod
    async def parse_article(article: int) -> tuple[int, dict[str, Any]]:
        """
        Method calls api and gets good
        :param article: article identification number
        :return: tuple of status and body of response
        """
        url = f"{settings.api_gateway_url}/api/common/wb_parse/{article}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.status, await response.json()

    # @staticmethod
    # async def save_to_sheets(good: Good) -> tuple[int, dict[str, Any]]:
    #     """
    #     Method calls api and save good to google sheets
    #     :param good: validated good's data
    #     :return: tuple of status and body of response
    #     """
    #     url = f"{settings.api_gateway_url}/api/common/gsheets/save"
    #     async with aiohttp.ClientSession() as session:
    #         async with session.post(url, json=good.model_dump()) as response:
    #             return response.status, await response.json()
