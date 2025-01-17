import time
import pyautogui as pg
import cv2 as cv

from loguru import logger
from typing import Iterable

from src.enums import CommonTemplate, Product, Window
from src.exceptions import UnsupportedScreenResolution
from src.products_for_purchase import ProductForPurchase
from src.interaction_scripts import (
    anti_afk, 
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
            self.vision.update_screenshot()

            if not self.vision.find_marketplace():
                found_window = self.vision.search_windows()
                
                if found_window is None:
                    logger.warning("Вне рабочей области")
                    time.sleep(1)
                    continue
                if found_window != Window.CONFIRM_PURCHASE:
                    press_okay()
                    continue
                else:
                    press_cancel_purchase()
                    continue
            
            anti_afk()

            for product_name, product_region in self.vision.search_products():
                if (product_price := self.vision.get_product_price(product_region[0], product_region[1])) is None:
                    logger.warning(f"Не получилось распознать цену товара {product_name}")
                    break 

                if not self.purchase_manager.make_purchase_decision(product_name, product_price):
                    continue
                
                press_buy_button(product_region[0], product_region[1])
                time.sleep(0.1)
                
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

# здесь был ишак