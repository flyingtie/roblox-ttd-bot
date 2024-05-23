import time

from loguru import logger
from typing import Iterable

from src.service import PurchaseManager
from src.vision import Vision
from src.products_to_purchase import ProductToPurchase


class Bot:
    def __init__(
        self, 
        purchase_manager: PurchaseManager,
        vision: Vision,
        products_to_purchase: Iterable[ProductToPurchase]
    ):
        self.purchase_manager = purchase_manager
        self.vision = vision
        self.products_to_purchase = products_to_purchase

    def run(self):        
        self.vision.load_products_templates(self.products_to_purchase)
        while True:
            logger.info(self.products_to_purchase)
            time.sleep(1)