import sys
import time
import os
import keyboard

sys.path.append(os.getcwd())

from threading import Thread    
from loguru import logger    

from src.products_to_purchase import products_to_purchase
from src.purchasing import PurchaseManager
from src.vision import Vision
from src.bot import Bot
from src.config import config


def wait_shutdown_key(key: str):
    keyboard.wait(key)
    raise KeyboardInterrupt

def main():
    purchase_manager = PurchaseManager(products_to_purchase)
    vision = Vision(
        products_to_purchase,
        config.path_to_templates,
        config.path_to_product_templates
    )
    
    bot = Bot(
        purchase_manager=purchase_manager, 
        vision=vision
    )

    try:
        # time.sleep(4)
        Thread(target=bot.run, daemon=True).start()
        wait_shutdown_key(config.shutdown_key)
    except KeyboardInterrupt:
        logger.error("Бот был остановлен вручную")

if __name__ == "__main__":
    main()