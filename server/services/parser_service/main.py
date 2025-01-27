from flask import Flask
import logging
import asyncio

from config import settings
from src.routers import parser_bp


def init_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
    )


def create_app() -> Flask:

    app = Flask(__name__)

    app.register_blueprint(parser_bp)

    return app


def main() -> None:
    init_logging()
    app = create_app()
    app.run(
        host=settings.PARSER_SERVICE_HOST,
        port=settings.PARSER_SERVICE_PORT,
    )


if __name__ == "__main__":
    asyncio.run(main())
