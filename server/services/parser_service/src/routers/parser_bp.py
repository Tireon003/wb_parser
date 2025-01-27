from flask import Blueprint
import logging

from src.core.gs import InsertionError
from src.services.sheets_service import SheetsService
from src.schemas import Article
from src.services.parser_service import ParserService, GoodNotFoundException

log = logging.getLogger(__name__)

bp = Blueprint(
    name="parser_bp",
    import_name=__name__,
    url_prefix="/api/parser",
)


@bp.route(
    rule="/article/<int:number>",
    methods=["GET"],
)
async def parse_article_by_number(number: int) -> tuple[dict, int]:
    try:
        article = Article(number=number)
        card_data = await ParserService.parse_by_article_number(article)
        sheets_service = SheetsService()
        sheets_service.insert_good_to_sheet(card_data)
        return {"info": card_data.model_dump()}, 200
    except GoodNotFoundException as not_found_err:
        return {
            "error": True,
            "status": 404,
            "info": not_found_err,
        }, 200
    except InsertionError as err:
        return {
            "error": True,
            "status": 500,
            "info": err.detail,
        }, 200
    except Exception as e:
        log.exception(
            "Exception while parsing article %s: %s",
            number,
            e,
        )
        return {
            "error": True,
            "status": 500,
            "info": f"{e}",
        }, 400
