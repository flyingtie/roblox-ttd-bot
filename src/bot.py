import time
import pyautogui as pg

from loguru import logger
from typing import Iterable
from pyautogui import FailSafeException

from src.exceptions import UnsupportedScreenResolution, NotEnoughMoney
from src.enums import CommonTemplate, Product
from src.products_to_purchase import ProductToPurchase
from src.interaction_scripts import hide_cursor
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
            logger.info("Бот запущен")
            self._run()
        except FailSafeException:
            logger.error("Сработал failsafe pyautogui")
        except NotEnoughMoney:
            logger.error("Недостаточно средств для покупки")
        except UnsupportedScreenResolution:
            logger.error("Неподдерживаемое разрешение экрана")
    
    def _run(self):
        self.on_startup()
        # self.vision._find_template(self.vision.templates[CommonTemplate.MARKETPLACE], self.vision.product_templates[Product.DJ_TV_MAN])
        while True:
            hide_cursor()
            self.vision.update_screenshot()
            

            logger.info("lol bot xd")
            time.sleep(2)

#TODO:
# НАЧАЛО
# Уводит курсор
# Моргает
# Пытается обнаружить маркетплейс
#   Если не находит, ищет уведомления по шаблонам
#       Если не находит, уходит в начало цикла
#       Если находит окно "кто-то в трейде", нажимает ок и уходит в начало цикла
#       Если находит окно "недостаточно денег", то кидает ошибку
#       Если находит окно с подтверждением, нажимает confirm и уходит в начало цикла
#       Если находит окно "Продавец в сделке", нажимает ок и уходит в начало цикла
#   Если находит маркетплейс, ищет отслеживаемые товары на скрине
#       Если не найдёт, уходит в начало цикла
#       Если найдёт товар, пытается найти цену 
#           Если не найдёт цену, уходит в начало цикла
#           Если считал цену, принимает решение о покупке
#               Если решил не покупать, уходит в начало цикла
#               Если решил купить, пытается найти кнопку покупки товара
#                   Если не нашёл, уходит в начало цикла
#                   Если нашёл, нажимает её
#                       Цикл 3 раза:
#                           Ждёт
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