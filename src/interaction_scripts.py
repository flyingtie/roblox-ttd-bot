import pyautogui as pg
import pydirectinput as pi
import random 
import time


def hide_cursor():
    random_y = random.randint(440, 640)
    pi.moveTo(1920, random_y, duration=0.2)

def press_okay():
    pi.moveTo(960, 690, duration=0.8)
    time.sleep(0.2)
    pi.click(button=pi.MOUSE_LEFT)

def press_confirm_purchase():
    pi.moveTo(640, 740, duration=0.8)
    time.sleep(0.2)
    pi.click(button=pi.MOUSE_LEFT)

def press_cancel_purchase():
    pi.moveTo(1260, 740, duration=0.8)
    time.sleep(0.2)
    pi.click(button=pi.MOUSE_LEFT)

def press_buy_button(
    top_left_product_region: tuple[int, int], 
    buttom_right_product_region: tuple[int, int]
):
    """Presses the buy button in the product region
    
    Parameters:
        top_left_product_region: y and x coordinates of the top left corner of the local price region.
        buttom_right_product_region: y and x coordinates of the bottom right corner of the local price region.

    """
    x, y = (
        top_left_product_region[1] + 50, 
        buttom_right_product_region[0] + 120
    )

    pi.moveTo(x, y, duration=0.8)
    time.sleep(0.2)
    pi.click(button=pi.MOUSE_LEFT)


if __name__ == "__main__":
    pass