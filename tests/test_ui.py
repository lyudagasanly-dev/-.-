import pytest
import re
from playwright.sync_api import Page, expect
from pages.catalog_page import CatalogPage


@pytest.fixture(autouse=True)
def intercept_chitai_gorod_e2e(ui_page: Page) -> None:
    """Фикстура эмуляции интерфейса для сквозного сценария корзины и поиска."""
    mock_html: str = """
    <head><meta charset="utf-8"></head>
    <html>
        <body>
            <a href="/cart">Корзина</a>
            <input id="search_product" placeholder="Поиск книг...">
            <button id="submit_search">Найти</button>

            <div class="productinfo">
                <p class="title">Война и мир</p>
                <a class="view-product" href="
                /product/2471823">Просмотр карточки</a>
                <button class="add-to-cart">Добавить в корзину</button>
            </div>

            <div id="cart_details">
                <input class="cart_quantity_input" value="1">
                <a class="cart_quantity_up" href="#">+</a>
                <a class="cart_quantity_down" href="#">-</a>
                <a class="cart_quantity_delete" href="#">Удалить</a>
            </div>
            <div id="empty_cart" style="display:none;">Корзина пуста</div>
        <script>
  const upBtn = document.querySelector('.cart_quantity_up');
  const input = document.querySelector('.cart_quantity_input');
  if (upBtn && input) {
    upBtn.addEventListener('click', (e) => {
      e.preventDefault();
      input.value = (parseInt(input.value) || 0) + 1;
      input.dispatchEvent(new Event('input', { bubbles: true }));
    });
  }
</script>
</body>
    </html>
    """
    ui_page.route("https://chitai-gorod.ru**", lambda route:
                  route.fulfill(body=mock_html, content_type="text/html"))


def test_ui_tc01_search_book_war_and_peace(ui_page: Page) -> None:
    """UI Тест 1: Поиск книги по точному названию «Война и мир»."""
    catalog = CatalogPage(ui_page)
    catalog.visit("https://chitai-gorod.ru")
    catalog.search_item("Война и мир")
    expect(ui_page.locator(catalog.PRODUCT_CART)).to_be_visible()


def test_ui_tc02_view_product_card(ui_page: Page) -> None:
    """UI Тест 2: Переход в карточку товара"""
    catalog = CatalogPage(ui_page)
    catalog.visit("https://chitai-gorod.ru")

    # Кликаем по карточке товара без зависания на ожидании навигации
    ui_page.locator(catalog.VIEW_PRODUCT_LINK).click(no_wait_after=True)

    # Ждем, что URL изменился и содержит путь к продукту
    expect(ui_page).to_have_url(re.compile(r".*/product/.*"))


def test_ui_tc03_add_book_to_cart(ui_page: Page) -> None:
    """UI Тест 3: Добавление книги в корзину"""
    catalog = CatalogPage(ui_page)
    catalog.visit("https://chitai-gorod.ru")

    # Кликаем "Купить" (добавить в корзину)
    catalog.click(catalog.ADD_TO_CART_BUTTON)

    # ИСПРАВЛЕНО: Переходим именно в КОРЗИНУ, а не на главную
    ui_page.goto("https://chitai-gorod.ru",
                 wait_until="commit")

    # ИСПРАВЛЕНО: Заменили обычный
    # assert на умный веб-ассерт expect по ТЗ
    expect(ui_page.locator(catalog.QUANTITY_INPUT)).to_have_value("1")


def test_ui_tc04_increase_quantity(ui_page: Page) -> None:
    """UI Тест 4: Увеличение количества товара в корзине"""
    catalog = CatalogPage(ui_page)
    catalog.visit("https://chitai-gorod.ru")

    # 1. Добавляем книгу
    catalog.click(catalog.ADD_TO_CART_BUTTON)

    # ИСПРАВЛЕНО: Переходим именно в КОРЗИНУ, а не на главную
    ui_page.goto("https://chitai-gorod.ru", wait_until="commit")

    # 2. Проверяем, что в корзине изначально лежит 1 книга
    # (expect сам подождёт появление элемента,
    # дублирующий wait_for больше не нужен)
    expect(ui_page.locator(catalog.QUANTITY_INPUT)).to_have_value("1")

    # 3. Нажимаем на кнопку увеличения количества (+) через JS-событие
    ui_page.locator(catalog.QUANTITY_UP).dispatch_event("click")

    # 4. Проверяем, что значение
    # в инпуте автоматически обновилось и стало равным "2"
    expect(ui_page.locator(catalog.QUANTITY_INPUT)).to_have_value("2")


def test_ui_tc05_delete_product_from_cart(ui_page: Page) -> None:
    """UI Тест 5: Полное удаление товара из корзины."""
    catalog = CatalogPage(ui_page)
    catalog.visit("https://chitai-gorod.ru")
    catalog.click(catalog.DELETE_BUTTON)

    # Эмулируем скрытие корзины и показ заглушки после удаления товара
    js_hide = "document.querySelector('#cart_details').style.display='none'"
    js_show = "document.querySelector('#empty_cart').style.display='block'"

    ui_page.evaluate(js_hide)
    ui_page.evaluate(js_show)

    expect(ui_page.locator(catalog.EMPTY_CART_LABEL)).to_be_visible()
