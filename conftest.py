import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

import requests
from typing import Generator
from config import Config


@pytest.fixture(scope="session")
def api_session() -> Generator[requests.Session, None, None]:
    """Фикстура для создания единой HTTP-сессии при API тестах."""
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def ui_page() -> Generator[Page, None, None]:
    """Фикстура для автоматического запуска браузера
    Playwright перед каждым UI-тестом."""
    with sync_playwright() as p:

        browser: Browser = p.chromium.launch(headless=False)
        context: BrowserContext = browser.new_context()
        page: Page = context.new_page()
        page.set_default_timeout(Config.TIMEOUT)

        yield page

        context.close()
        browser.close()
