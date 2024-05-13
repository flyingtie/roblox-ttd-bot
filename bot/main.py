import sys
import pyautogui

sys.path.append(".")
    
from bot.config import Settings


def main():
    config = Settings()
    
    pyautogui.FAILSAFE = config.pyautogui_failsafe    

    

if __name__ == "__main__":
    main()