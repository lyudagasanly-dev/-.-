from pages.base_page import BasePage


class CatalogPage(BasePage):
    # Локаторы для поиска и карточки
    SEARCH_INPUT: str = "input#search_product"
    SEARCH_BUTTON: str = "button#submit_search"
    PRODUCT_CART: str = ".productinfo"
    VIEW_PRODUCT_LINK: str = "a.view-product"

    # Локаторы для корзины
    ADD_TO_CART_BUTTON: str = "button.add-to-cart"
    CART_LINK: str = "a[href='/cart']"

    # Локаторы для управления количеством в корзине
    QUANTITY_INPUT: str = ".cart_quantity_input"

    QUANTITY_UP: str = "a.cart_quantity_up"
    QUANTITY_DOWN: str = "a.cart_quantity_down"
    DELETE_BUTTON: str = "a.cart_quantity_delete"
    EMPTY_CART_LABEL: str = "#empty_cart"

    def search_item(self, item_name: str) -> None:
        """Метод для поиска книги (например, Война и мир)."""
        self.fill_input(self.SEARCH_INPUT, item_name)
        self.click(self.SEARCH_BUTTON)

    def is_product_visible(self) -> bool:
        """Проверка отображения карточки книги после поиска."""
        return self.page.locator(self.PRODUCT_CART).first.is_visible()
