from src.service import PurchaseManager
from src.game import Game

import time


class Bot:
    def __init__(
        self, 
        purchase_manager: PurchaseManager,
        game_manager: Game,
        products_to_purchase
    ):
        self.purchase_manager = purchase_manager
        self.game_manager = game_manager
        self.products_to_purchase = products_to_purchase

    def run(self):        
        while True:
            time.sleep(0.5)