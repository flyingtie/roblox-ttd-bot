import sys
import time
import os
import keyboard

sys.path.append(os.getcwd())

from threading import Thread    
from loguru import logger    
from dotenv import load_dotenv

load_dotenv()

from src.products_for_purchase import products_for_purchase
from src.purchasing import PurchaseManager
from src.vision import Vision
from src.bot import Bot
from src.config import config

# 325 381
def wait_shutdown_key(key: str):
    keyboard.wait(key)
    raise KeyboardInterrupt

def main():
    purchase_manager = PurchaseManager(products_for_purchase)
    vision = Vision(products_for_purchase)
    
    bot = Bot(
        purchase_manager=purchase_manager, 
        vision=vision
    )

    try:
        # фора для открытия игры
        # time.sleep(5)

        Thread(target=bot.run, daemon=True).start()

        wait_shutdown_key(config.shutdown_key)
    except KeyboardInterrupt:
        logger.error("Бот был остановлен вручную")

if __name__ == "__main__":
    main()