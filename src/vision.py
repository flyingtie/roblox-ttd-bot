import cv2 as cv
import numpy as np
import re

from loguru import logger
from enum import Enum, auto
from cv2.typing import MatLike
from PIL import ImageGrab
from numpy.typing import NDArray
from typing import Union
from matplotlib import pyplot as plt

from src.exceptions import UnsupportedScreenResolution, PriceValidationError
from src.products_to_purchase import ProductToPurchase
from src.enums import (
    InterfaceElement, 
    Product, 
    CommonTemplate,
    Window,
    Button
)
from src.config import config


class Vision:
    product_templates: dict[Product, MatLike]
    templates: dict[CommonTemplate, MatLike]
    screenshot: NDArray
    
    def __init__(self, products_to_purchase: dict[Product, ProductToPurchase]):
        self.products_to_purchase = products_to_purchase
        self.product_templates = dict()
        self.templates = dict()
        self.screenshot = None
        self._interface_elements_methods = {
            Button.CONFIRM: self.find_confirm_button,
            Button.CANCEL: self.find_cancel_button,
            Button.OKAY: self.find_okay_button,
            Button.BUY: self.find_buy_button,
            Window.NOT_ENOUGH_MONEY: self.find_not_enough_money_window,
            Window.IN_TRADE: self.find_in_trade_window,
            Window.MARKETPLACE: self.find_marketplace_window,
            Window.NOT_FOUND: self.find_not_found_window
        }
    
    def load_product_templates(self):
        for product_name in self.products_to_purchase:
            path = config.path_to_product_templates.joinpath(product_name + ".png")
            template = cv.imread(str(path), cv.IMREAD_GRAYSCALE)
            if template is None:
                raise FileNotFoundError(path)
            self.product_templates[product_name] = template
    
    def load_templates(self):
        for template_name in CommonTemplate:
            path = config.path_to_templates.joinpath(template_name + ".png")
            template = cv.imread(str(path), cv.IMREAD_GRAYSCALE)
            if template is None:
                raise FileNotFoundError(path)
            self.templates[template_name] = template
    
    def update_screenshot(self):
        img = ImageGrab.grab()
        self.screenshot = np.array(img, dtype=np.uint8)
        
        # if self.screenshot.size != (1920, 1080):
        #     raise UnsupportedScreenResolution

    @staticmethod
    def _find_template(self, img: Union[MatLike, NDArray], template: Union[MatLike, NDArray]):
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        bottom_right = (max_loc[0] + w, max_loc[1] + h)
        # cv.rectangle(screenshot, max_loc, bottom_right, 255, 2)
        # plt.subplot(121),plt.imshow(res,cmap = 'gray')
        # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(self.screenshot,cmap = 'gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # plt.show()
    
    def find_product(self, product_name: Product):
        pass
        
    def find_interface_element(self, element: InterfaceElement, region):
        if not isinstance(element, InterfaceElement):
            raise TypeError(f"expected InterfaceElement type, got \"{type(element)}\" instead")
        
        try:    
            return self._interface_elements_methods[element]()
        except KeyError:
            raise ValueError("unknown interface element")
    
    def find_marketplace_window(self):
        pass
    
    def find_not_found_window(self):
        pass
    
    def find_in_trade_window(self):
        pass
    
    def find_not_enough_money_window(self):
        pass
    
    def find_confirm_button(self):
        pass
    
    def find_cancel_button(self):
        pass
    
    def find_okay_button(self):
        pass
    
    def find_buy_button(self):
        pass
    
    def find_product_name_in_confirm_window(self):
        pass
    
    def find_price_in_confirm_window(self):
        pass
    
    def find_price(self):
        pass
    
    @staticmethod
    def validate_price(price: str) -> int:
        price = price.replace(" ", "").lower()
        
        if price.isdigit():
            return int(price)
        
        match_groups = re.match(r"^(\d+|\d+\.\d+)([kmb])$", price)
        
        if not match_groups:
            raise PriceValidationError(f"could not convert {price} to an integer")
        
        price = float(match_groups.group(1))
    
        match match_groups.group(2):
            case "k":
                price *= 1000
            case "m":
                price *= 1_000_000
            case "b":
                price *= 1_000_000_000
        
        return int(price)

# image_1 = cv.imread('templates/no_money 1366 768.png')
# img_2 = cv.imread('templates/marketplace 1366 768.png', cv.IMREAD_GRAYSCALE)


# # ret, img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

# # img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

# cv.imshow("result", img)
# cv.waitKey(0)
# cv.destroyAllWindows()