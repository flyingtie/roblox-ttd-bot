import sys
import pyautogui

sys.path.append(".")
    
from loguru import logger    
from pydantic import ValidationError

from src.config import Settings
from src.service import PurchaseManager
from src.bot import Bot
from src.game import Game
from src.products_data import ProductToPurchase, products_data

def main():
    config = Settings()
    
    pyautogui.FAILSAFE = config.pyautogui_failsafe  
    
    purchase_manager = PurchaseManager()
    game_manager = Game()

    try:
        products_to_purchase = [
            ProductToPurchase(
                name=product[0], 
                max_price=product[1]
            ) for product in products_data
        ]
    except ValidationError as e:
        logger.error(e)

    bot = Bot(
        purchase_manager=purchase_manager, 
        game_manager=game_manager, 
        products_to_purchase=products_to_purchase
    )
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.error("Бот был остановлен вручную")

if __name__ == "__main__":
    main()