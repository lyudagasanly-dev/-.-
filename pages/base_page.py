from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page: Page = page

    def visit(self, url: str) -> None:
        """Метод для явного перехода по URL."""
        self.page.goto(url)

    def click(self, selector: str) -> None:
        """Клик по элементу с автоматическим явным ожиданием."""
        locator: Locator = self.page.locator(selector)
        locator.wait_for(state="visible")
        locator.click()

    def fill_input(self, selector: str, text: str) -> None:
        """Заполнение текстового поля."""
        locator: Locator = self.page.locator(selector)
        locator.wait_for(state="visible")
        locator.fill(text)
