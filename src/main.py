import sys
import pyautogui

sys.path.append(".")
    
from pyautogui import FailSafeException
from loguru import logger    
from pydantic import ValidationError

from src.products_to_purchase import ProductToPurchase, products_to_purchase
from src.exceptions import UnsupportedScreenResolution
from src.config import config
from src.service import PurchaseManager
from src.bot import Bot
from src.vision import Vision

def main():
    pyautogui.FAILSAFE = config.pyautogui_failsafe  
    
    try:
        prods_to_purch = [
            ProductToPurchase(
                name=product[0], 
                max_price=product[1]
            ) for product in products_to_purchase
        ]
    except ValidationError as e:
        logger.error(e)

    purchase_manager = PurchaseManager(prods_to_purch)
    vision = Vision(prods_to_purch)
    
    bot = Bot(
        purchase_manager=purchase_manager, 
        vision=vision, 
        products_to_purchase=prods_to_purch
    )
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.error("Бот был остановлен вручную")
    except FailSafeException:
        logger.error("Сработал failsafe pyautogui")
    except UnsupportedScreenResolution:
        logger.error("Неподдерживаемое разрешение экрана")

if __name__ == "__main__":
    main()