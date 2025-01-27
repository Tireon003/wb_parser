from src.core.wb import WbParser
from src.schemas import Article, Good
from .exc import GoodNotFoundException


class ParserService:

    @staticmethod
    async def parse_by_article_number(article: Article) -> Good:
        wb_parser = WbParser(remote=True)
        parsed_good = await wb_parser.get_card_data(article.number)

        if not parsed_good:
            raise GoodNotFoundException(
                f"Card with article {article.number} not found."
            )

        return parsed_good
