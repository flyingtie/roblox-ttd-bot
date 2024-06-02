import time
import pyautogui as pg
import cv2 as cv

from loguru import logger
from typing import Iterable

from src.exceptions import UnsupportedScreenResolution, NotEnoughMoney
from src.enums import CommonTemplate, Product
from src.products_for_purchase import ProductForPurchase
from src.interaction_scripts import hide_cursor, press_buy_button
from src.purchasing import PurchaseManager
from src.vision import Vision, Button, Window


class Bot:
    def __init__(
        self, 
        purchase_manager: PurchaseManager,
        vision: Vision
    ):
        self.purchase_manager = purchase_manager
        self.vision = vision

    def on_startup(self):
        self.vision.load_templates()
        self.vision.load_product_templates()

    def run(self):
        try:
            self.on_startup()
            self._run()
        except NotEnoughMoney:
            logger.error("Недостаточно средств для покупки")
        except UnsupportedScreenResolution:
            logger.error("Неподдерживаемое разрешение экрана")
    
    def _run(self):
        logger.info("Бот запущен")
        
        while True:
            hide_cursor()
            self.vision.update_screenshot()
            if not self.vision.find_marketplace():
                #TODO: найти уведы
                logger.warning("Не нашёл маркетплейс")
                time.sleep(1.5)
                continue
            for product, product_region in self.vision.search_products():
                if (product_price := self.vision.get_product_price(product_region[0], product_region[1])) is None:
                    logger.warning(f"Не получилось распознать цену товара {product}")
                    break                    
                if self.purchase_manager.make_purchase_decision(product, product_price) is False:
                    continue
                press_buy_button(product_region[0], product_region[1])
                time.sleep(3)
                #TODO

            time.sleep(1)

#TODO:
# НАЧАЛО
# Уводит курсор
# Моргает
# Пытается обнаружить маркетплейс
#   Если не находит, ищет уведомления по шаблонам
#       Если не находит, уходит в начало цикла
#       Если находит окно "кто-то в трейде", нажимает ок и уходит в начало цикла
#       Если находит окно "недостаточно денег", то кидает ошибку
#       Если находит окно с подтверждением, нажимает cancel и уходит в начало цикла
#       Если находит окно "Продавец в сделке", нажимает ок и уходит в начало цикла
#   Если находит маркетплейс, ищет отслеживаемые товары на скрине
#       Если не найдёт, уходит в начало цикла
#       Если найдёт товар, пытается найти цену 
#           Если не найдёт цену, уходит в начало цикла
#           Если считал цену, принимает решение о покупке
#               Если решил не покупать, ищет оставшиеся товары (уходит в начало локального цикла)
#               Если решил купить, нажимает кнопку покупки
#                           Ждёт 3.5 секунды
#                           Отводит курсор
#                           Моргает
#                           Ищет окно подтверждения
#                               Если не находит 3 раза, уходит в начало цикла
#                               Если не находит, continue
#                               Если находит, break
#                       Сверяет данные на окне подтверждения
#                           Если данные не совпадают, уходит в начало цикла
#                           Если совпадают, нажимает confirm
#                       Ждёт
#                       Уходит в начало цикла
# 
# 
# 
# КОНЕЦ