import pyautogui as pg
import random 
import time


def hide_cursor():
    random_y = random.randint(440, 640)
    pg.moveTo(1920, random_y, duration=0.1)

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

    pg.click(x, y, duration=0.1, button="left")


if __name__ == "__main__":
    pass