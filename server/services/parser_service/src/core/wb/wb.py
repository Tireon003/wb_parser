from collections.abc import Generator
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import asyncio
import aiohttp
import logging

from config import settings
from .wb_exc import WBConnectionError
from src.schemas import Good

logger = logging.getLogger(__name__)


class CardDataXPaths:
    """Class contains xpath's for WbParser."""

    CARD_IMAGES = "//ul[@class='swiper-wrapper']/li"
    SPECS = "//div[@class='product-params']"
    # DESCRIPTION = "//p[@class='option__text']"
    # DESCRIPTION = "//section[@class='product-details__description option']/p"
    DESCRIPTION = "//section[@class='product-details__description option']"
    BUTTON_SHOW_ALL_SPECS_DESCRIPTION = (
        "//button[@data-name-for-wba='Item_Description_Parameters_More']"
    )
    BUTTON_CLOSE_SPECS_DESCRIPTION_POPUP = (
        "//div[@class='popup popup-product-details shown']/a"
    )
    SPECS_ROW = "//div[@class='product-params']/table/tbody/tr"
    NOT_FOUND = "//div[@class='content404']"


class WbParser:
    """Class to interact with WB site using Selenium webdriver. _"""

    _WB_URL = settings.WB_URL
    _USER_AGENT = settings.USER_AGENT
    _options = webdriver.ChromeOptions()
    _WAITING_FOR_LOAD_TIMEOUT = 30

    def __init__(self, remote: bool = True):
        self._options.page_load_strategy = "eager"
        self._options.add_argument("--headless")  # Запуск без графического интерфейса
        self._options.add_argument("--no-sandbox")  # Отключение песочницы
        self._options.add_argument(
            "--disable-dev-shm-usage"
        )  # Устраняет проблему ограниченного объема shared memory
        self._options.add_argument("--disable-extensions")
        self._options.add_argument(
            "--disable-software-rasterizer"
        )  # Устранение GPU-сбоев
        self._options.add_argument("--disable-logging")
        self._options.add_argument(
            "--disable-gpu"
        )  # Отключение GPU-ускорения (нужно для headless)
        self._options.add_argument(
            "--window-size=1920,1080"
        )  # Задает размер окна (важно для headless)
        self._options.add_argument(
            "--disable-setuid-sandbox"
        )  # Отключение sandbox для повышения совместимости

        # Для предотвращения детектирования автоматизации
        self._options.add_experimental_option("detach", True)
        self._options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self._options.add_experimental_option("useAutomationExtension", False)
        self._options.add_argument("--disable-blink-features=AutomationControlled")

        # Настройки пользователя (можно заменить на свои)
        self._options.add_argument("--incognito")  # Инкогнито-режим

        # Установка пользовательского user-agent (опционально)
        self._options.add_argument(settings.USER_AGENT)

        # Создание WebDriver с учетом пути к chromedriver
        if remote:
            self._driver: WebDriver = webdriver.Remote(
                command_executor=settings.selenium_url,
                options=self._options,
            )
        else:
            self._driver: WebDriver = webdriver.Chrome(options=self._options)

        self._driver.maximize_window()

    @staticmethod
    async def _wb_healthcheck() -> bool:
        """
        Method check WB site availability.
        :return: True if wb site is up, False if wb site is down.
        """
        async with aiohttp.ClientSession() as session:
            url = settings.WB_URL
            async with session.get(url) as response:
                return response.status == 200

    @contextmanager
    def _show_specs_and_description_window(self) -> Generator[..., None]:
        """
        Context manager which show specs and description window while logic
        in manager executing.
        :return:
        """
        WebDriverWait(self._driver, self._WAITING_FOR_LOAD_TIMEOUT).until(
            ec.element_to_be_clickable(
                (
                    By.XPATH,
                    CardDataXPaths.BUTTON_SHOW_ALL_SPECS_DESCRIPTION,
                )
            )
        )
        show_all_button = self._driver.find_element(
            By.XPATH,
            CardDataXPaths.BUTTON_SHOW_ALL_SPECS_DESCRIPTION,
        )
        show_all_button.click()
        yield
        WebDriverWait(self._driver, self._WAITING_FOR_LOAD_TIMEOUT).until(
            ec.element_to_be_clickable(
                (
                    By.XPATH,
                    CardDataXPaths.BUTTON_CLOSE_SPECS_DESCRIPTION_POPUP,
                )
            )
        )
        close_popup_button = self._driver.find_element(
            By.XPATH,
            CardDataXPaths.BUTTON_CLOSE_SPECS_DESCRIPTION_POPUP,
        )
        close_popup_button.click()

    def _get_card_spec_description(self) -> list[dict[str, str], str]:
        specs_dict = dict()
        with self._show_specs_and_description_window():
            WebDriverWait(self._driver, self._WAITING_FOR_LOAD_TIMEOUT).until(
                ec.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        CardDataXPaths.SPECS_ROW,
                    )
                )
            )
            params_rows = self._driver.find_elements(
                By.XPATH,
                CardDataXPaths.SPECS_ROW,
            )
            for row in params_rows:
                param_col = row.find_element(By.TAG_NAME, "th")
                value_col = row.find_element(By.TAG_NAME, "td")
                specs_dict[param_col.text] = value_col.text

            WebDriverWait(self._driver, self._WAITING_FOR_LOAD_TIMEOUT).until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        CardDataXPaths.DESCRIPTION,
                    )
                )
            )
            description_element = self._driver.find_element(
                By.XPATH,
                CardDataXPaths.DESCRIPTION,
            )
            return [
                specs_dict,
                description_element.get_attribute("innerText"),
                # description_element.text,
            ]

    def _get_card_images(self) -> list[str]:
        """
        Method parse urls to images from card page
        :return: list of image urls
        """
        img_urls_list = list()
        image_list = self._driver.find_elements(
            By.XPATH,
            CardDataXPaths.CARD_IMAGES,
        )
        for item in image_list:
            try:
                image_tag = item.find_element(By.XPATH, "./div/img")
                img_url = image_tag.get_attribute("src")
                img_urls_list.append(img_url)
            except NoSuchElementException:
                continue

        return img_urls_list

    async def get_card_data(self, article_number: int) -> Good | None:
        """
        Method parse card data from WB
        :param article_number: article identification number
        :return: Good instance in good found by article number else None
        """
        is_wb_up = await self._wb_healthcheck()
        if not is_wb_up:
            raise WBConnectionError("WB is not responding")

        url = f"{self._WB_URL}/catalog/{article_number}/detail.aspx?targetUrl=SP"
        self._driver.get(url)
        await asyncio.sleep(8)

        page_loaded_condition = ec.element_to_be_clickable(
            (
                By.XPATH,
                CardDataXPaths.BUTTON_SHOW_ALL_SPECS_DESCRIPTION,
            )
        )

        try:
            WebDriverWait(
                driver=self._driver,
                timeout=self._WAITING_FOR_LOAD_TIMEOUT,
            ).until(page_loaded_condition)
        except TimeoutException:
            return None

        card_specs_description = self._get_card_spec_description()

        good_data_dict = dict(
            pictures=self._get_card_images(),
            specs=card_specs_description[0],
            description=card_specs_description[1],
        )

        async with aiohttp.ClientSession() as session:
            card_api_url = (
                f"https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&"
                f"dest=-1257786&spp=30&hide_dtype=10&ab_testing=false&"
                f"nm={article_number}"
            )
            async with session.get(card_api_url) as response:
                if response.status != 200:
                    return None

                card_data = (await response.json())["data"]["products"][0]

                good_data_dict.update(
                    article=card_data["id"],
                    title=card_data["name"],
                    category=card_data["entity"],
                    price=card_data["sizes"][0]["price"]["total"],
                    rating=card_data["reviewRating"],
                    feedbacks=card_data["feedbacks"],
                )

        return Good(**good_data_dict)

    def __del__(self) -> None:
        if hasattr(self, "_driver"):
            self._driver.quit()
