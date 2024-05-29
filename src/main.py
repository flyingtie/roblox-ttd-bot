import sys
import time
import os
import keyboard
import pyautogui

sys.path.append(os.getcwd())

from threading import Thread    
from pyautogui import FailSafeException
from loguru import logger    
from pydantic import ValidationError

from src.products_to_purchase import ProductToPurchase, products_to_purchase
from src.exceptions import UnsupportedScreenResolution, NotEnoughMoney
from src.purchasing import PurchaseManager
from src.interactions import Device
from src.vision import Vision
from src.bot import Bot
from src.config import config

class MainWorker(Thread):     
    def run(self):
        try:
            super().run()
        except FailSafeException:
            logger.error("Сработал failsafe pyautogui")
        except NotEnoughMoney:
            logger.error("Недостаточно средств для покупки")
        except UnsupportedScreenResolution:
            logger.error("Неподдерживаемое разрешение экрана")

def wait_shutdown_key(key: str):
    keyboard.wait(key)
    raise KeyboardInterrupt

def main():
    pyautogui.FAILSAFE = config.pyautogui_failsafe  
    
    purchase_manager = PurchaseManager(products_to_purchase)
    vision = Vision(products_to_purchase)
    device = Device()
    
    bot = Bot(
        purchase_manager=purchase_manager, 
        vision=vision,
        device=device, 
        # products_to_purchase=prods_to_purch
    )

    try:
        # time.sleep(4)
        MainWorker(target=bot.run, daemon=True).start()
        wait_shutdown_key(config.shutdown_key)
    except KeyboardInterrupt:
        logger.error("Бот был остановлен вручную")

if __name__ == "__main__":
    main()