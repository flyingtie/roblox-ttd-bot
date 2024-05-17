import sys
import pyautogui

sys.path.append(".")
    
from loguru import logger    
    
from src.config import Settings
from src.service import PurchaseManager
from src.bot import Bot
from src.game import Game


def main():
    config = Settings()
    
    pyautogui.FAILSAFE = config.pyautogui_failsafe  
    
    purchase_manager = PurchaseManager()
    game_manager = Game()

    bot = Bot(
        purchase_manager=purchase_manager, 
        game_manager=game_manager, 
        products_to_purchase={1: 2}
    )
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.error("Бот был остановлен вручную")

if __name__ == "__main__":
    main()