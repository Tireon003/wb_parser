from flask import Flask
import logging
import asyncio

from config import settings
from src.routers import common_bp


def init_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
    )


def create_app() -> Flask:

    app = Flask(__name__)

    app.register_blueprint(common_bp)

    return app


def main() -> None:
    init_logging()
    app = create_app()
    app.run(
        host=settings.API_GATEWAY_HOST,
        port=settings.API_GATEWAY_PORT,
    )


if __name__ == "__main__":
    asyncio.run(main())
