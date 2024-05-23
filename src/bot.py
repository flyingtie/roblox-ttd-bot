import time
import pyautogui as pg

from loguru import logger
from typing import Iterable

from src.products_to_purchase import ProductToPurchase
from src.interactions import Device
from src.service import PurchaseManager
from src.vision import Vision
from src.templates import Template

class Bot:
    def __init__(
        self, 
        purchase_manager: PurchaseManager,
        vision: Vision,
        device: Device,
        products_to_purchase: Iterable[ProductToPurchase]
    ):
        self.purchase_manager = purchase_manager
        self.vision = vision
        self.device = device
        self.products_to_purchase = products_to_purchase

    def on_startup(self):
        logger.info("Бот запущен")
        self.vision.load_templates()
        self.vision.load_product_templates()
    
    def run(self):
        self.on_startup()        
        while True:
            self.vision.update_screenshot()
            # logger.info(self.products_to_purchase)
            logger.info(self.vision.product_templates)
            logger.info(self.vision.templates)
            
            time.sleep(5)
            break