import pyautogui as pg
import random 

#TODO: Антиспам фича с перемещением курсора в рандомный угол перед скриншотом
class Device:
    def __init__(self):
        pass

    def hide_cursor(self):
        random_y = random.randint(440, 640)
        pg.moveTo(1920, random_y, duration=0.1)


if __name__ == "__main__":
    d = Device()
    d.hide_cursor()