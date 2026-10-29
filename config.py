class Config:
    # Базовые URL для реального тестирования интернет-магазина "Читай-город"
    UI_URL: str = "https://chitai-gorod.ru"
    API_URL: str = "https://webapi.chitai-gorod.ru/api/v1"
    TIMEOUT: int = 15000  # Увеличим таймаут до 15 секунд для стабильности на реальной сети
