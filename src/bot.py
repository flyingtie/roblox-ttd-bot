import time
import pyautogui as pg
import cv2 as cv

from loguru import logger
from typing import Iterable

from src.enums import CommonTemplate, Product, Window
from src.exceptions import UnsupportedScreenResolution
from src.products_for_purchase import ProductForPurchase
from src.interaction_scripts import (
    hide_cursor, 
    press_buy_button,
    press_confirm_purchase,
    press_cancel_purchase,
    press_okay
)    
from src.purchasing import PurchaseManager
from src.vision import Vision


class Bot:
    def __init__(
        self, 
        purchase_manager: PurchaseManager,
        vision: Vision
    ):
        self.purchase_manager = purchase_manager
        self.vision = vision

    # def test(self):
    #     img = cv.imread("templates/test/test_market.png", cv.IMREAD_GRAYSCALE)
    #     tmpl = cv.cvtColor(self.vision.product_templates[Product.HYPER_UPGRADED_TITAN_SPEAKERMAN], cv.COLOR_BGR2GRAY)
    #     res = cv.matchTemplate(img, tmpl, cv.TM_CCOEFF_NORMED)
    #     print(cv.minMaxLoc(res))

    def on_startup(self):
        self.vision.load_templates()
        self.vision.load_product_templates()

    def run(self):
        try:
            self.on_startup()
            self._run()
        except UnsupportedScreenResolution:
            logger.error("Неподдерживаемое разрешение экрана")
    
    def _run(self):
        logger.info("Бот запущен")
        
        while True:
            hide_cursor()
            self.vision.update_screenshot()

            if not self.vision.find_marketplace():
                found_window = self.vision.search_windows()
                
                if found_window is None:
                    logger.warning("Вне рабочей области")
                    continue
                if found_window != Window.CONFIRM_PURCHASE:
                    press_okay()
                    continue
                else:
                    press_cancel_purchase()
                    continue

            for product_name, product_region in self.vision.search_products():
                if (product_price := self.vision.get_product_price(product_region[0], product_region[1])) is None:
                    logger.warning(f"Не получилось распознать цену товара {product_name}")
                    break 

                if not self.purchase_manager.make_purchase_decision(product_name, product_price):
                    continue
                
                press_buy_button(product_region[0], product_region[1])
                time.sleep(0.1)
                
                hide_cursor()
                self.vision.update_screenshot()
                
                if not self.vision.find_confirm_window():
                    break

                confirm, clean_price = self.vision.confirm_purchase(product_name, product_price)
                if not (confirm and self.purchase_manager.make_purchase_decision(product_name, clean_price)):
                    press_cancel_purchase()
                    continue
                press_confirm_purchase()
                continue

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
#                               Если не находит 2 раза, уходит в начало цикла
#                               Если не находит, continue
#                               Если находит, break
#                       Сверяет данные на окне подтверждения
#                           Если данные не совпадают, нажимает cancel
#                           Если совпадают, нажимает confirm
#                       Ждёт
#                       Уходит в начало цикла
# 
# 
# 
# КОНЕЦ