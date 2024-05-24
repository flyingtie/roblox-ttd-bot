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
            # Моргает
            # Пытается обнаружить маркетплейс
            # Если не находит, пытается понять что он видит
            # ...
            # Если вообще ничего не находит, уходит в начало цикла
            # Если находит маркетплейс, ищет отслеживаемые товары на скрине
            # Если не найдёт, уходит в начало цикла
            # Если найдёт, ищет координаты кнопки 
            # Моргает и проверяет ещё раз именно этот шаблон
            # Если не совпадает, то уходит в самое начало цикла
            # Если совпадает, то нажимает кнопку
            # Уходит в начало цикла
            
            time.sleep(5)
            break