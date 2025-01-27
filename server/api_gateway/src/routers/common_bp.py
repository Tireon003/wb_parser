from typing import Any

from flask import Blueprint
import logging

from flask_pydantic import validate

from src.schemas import Good
from src.services.logging_service import LogProducer
from src.services.parser_service import (
    ParserService,
    ParseFailedException,
    SaveFailedException,
)

log = logging.getLogger(__name__)

bp = Blueprint(
    name="common_bp",
    import_name=__name__,
    url_prefix="/api/common",
)


@bp.route(
    rule="/wb_parse/<int:article>",
    methods=["GET"],
)
async def parse_wb_card_by_article(article: int) -> tuple[dict, int]:
    try:
        good = await ParserService.parse_card(article)
        return {"status": "success", "data": good.model_dump()}, 200
    except ParseFailedException as parse_err:
        log.error(
            "Error while parsing article %s: %s",
            article,
            parse_err,
        )
        async with LogProducer.get_instance() as logger_service:
            await logger_service.send_log(
                parse_err.detail.get(
                    "info",
                    f"{parse_err}",
                )
            )
        return parse_err.detail, 400


@bp.route(
    rule="/gsheets/save",
    methods=["POST"],
)
@validate()
async def save_good_gsheets(body: Good) -> tuple[dict[str, Any], int]:
    """
    Endpoint for saving good's data to sheets.
    :param body: good data validated from request body
    :return: response body and status code
    """
    try:
        await ParserService.save_to_sheets(body)
        return {"status": "success", "data": "none"}, 200
    except SaveFailedException as save_err:
        log.error(
            "Error while saving good to sheets: %s",
            f"{save_err}",
        )
        async with LogProducer.get_instance() as logger_service:
            await logger_service.send_log(
                save_err.detail.get(
                    "info",
                    f"{save_err}",
                )
            )
        return save_err.detail, 400
