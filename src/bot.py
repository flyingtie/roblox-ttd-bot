import time

from loguru import logger
from typing import Iterable

from src.service import PurchaseManager
from src.game import Game
from src.products_data import ProductToPurchase


class Bot:
    def __init__(
        self, 
        purchase_manager: PurchaseManager,
        game_manager: Game,
        products_to_purchase: Iterable[ProductToPurchase]
    ):
        self.purchase_manager = purchase_manager
        self.game_manager = game_manager
        self.products_to_purchase = products_to_purchase

    def run(self):        
        while True:
            logger.info("Бот работает")
            time.sleep(1)