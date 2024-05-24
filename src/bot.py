import time
import pyautogui as pg

from loguru import logger
from typing import Iterable

from src.templates import CommonTemplate
from src.products_to_purchase import ProductToPurchase
from src.interaction import Device
from src.purchasing import PurchaseManager
from src.vision import Vision


class Bot:
    def __init__(
        self, 
        purchase_manager: PurchaseManager,
        vision: Vision,
        device: Device,
        # products_to_purchase: Iterable[ProductToPurchase]
    ):
        self.purchase_manager = purchase_manager
        self.vision = vision
        self.device = device
        # self.products_to_purchase = products_to_purchase

    def on_startup(self):
        logger.info("Бот запущен")
        self.vision.load_templates()
        self.vision.load_product_templates()
    
    def run(self):
        self.on_startup()
        while True:
            self.vision.update_screenshot()
            
            #TODO:
            # НАЧАЛО
            # Уводит курсор
            # Моргает
            # Пытается обнаружить маркетплейс
            #   Если не находит, уходит в начало цикла
            #   Если находит маркетплейс, ищет отслеживаемые товары на скрине
            #       Если не найдёт, уходит в начало цикла
            #       Если найдёт товар, пытается найти цену 
            #           Если не найдёт цену, уходит в начало цикла
            #           Если считал цену, принимает решение о покупке
            #               Если решил не покупать, уходит в начало цикла
            #               Если решил купить, пытается найти кнопку покупки товара
            #                   Если не нашёл, уходит в начало цикла
            #                   Если нашёл, нажимает
            #                       Ждёт
            #                       Моргает
            # 
            # 
            # 
            # КОНЕЦ
            
            time.sleep(5)
            break