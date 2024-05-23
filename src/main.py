import sys
import pyautogui

sys.path.append(".")
    
from loguru import logger    
from pydantic import ValidationError

from src.products_to_purchase import ProductToPurchase, products_to_purchase
from src.config import config
from src.service import PurchaseManager
from src.bot import Bot
from src.vision import Vision

def main():
    pyautogui.FAILSAFE = config.pyautogui_failsafe  
    
    try:
        prod_to_purch = [
            ProductToPurchase(
                name=product[0], 
                max_price=product[1]
            ) for product in products_to_purchase
        ]
    except ValidationError as e:
        logger.error(e)

    purchase_manager = PurchaseManager()
    vision = Vision()
    
    bot = Bot(
        purchase_manager=purchase_manager, 
        vision=vision, 
        products_to_purchase=prod_to_purch
    )
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.error("Бот был остановлен вручную")

if __name__ == "__main__":
    main()