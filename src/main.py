import sys
import pyautogui

sys.path.append(".")
    
from loguru import logger    
    
from src.config import Settings
from src.bot import Bot

def main():
    config = Settings()
    
    pyautogui.FAILSAFE = config.pyautogui_failsafe  
    
    bot = Bot()
    
    try:
        bot.run()
    except KeyboardInterrupt:
        logger.error("Бот был остановлен вручную")

if __name__ == "__main__":
    main()