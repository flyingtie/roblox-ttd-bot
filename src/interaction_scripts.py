import pyautogui as pg
import random 


def hide_cursor():
    random_y = random.randint(440, 640)
    pg.moveTo(1920, random_y, duration=0.1)




if __name__ == "__main__":
    pass