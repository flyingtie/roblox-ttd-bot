import cv2 as cv
import numpy as np
import re

from loguru import logger
from enum import Enum, auto
from cv2.typing import MatLike
from PIL import ImageGrab
from numpy.typing import NDArray

from src.exceptions import UnsupportedScreenResolution, PriceValidationError
from src.products_to_purchase import ProductToPurchase
from src.enums import (
    InterfaceElement, 
    Product, 
    CommonTemplate,
    Window,
    Button,
    Template
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
            Button.CONFIRM: self._find_confirm_button,
            Button.CANCEL: self._find_cancel_button,
            Button.OKAY: self._find_okay_button,
            Button.BUY: self._find_buy_button,
            Window.NOT_ENOUGH_MONEY: self._find_not_enough_money_window,
            Window.SELLER_IN_TRADE: self._find_seller_in_trade_window,
            Window.MARKETPLACE: self._find_marketplace_window
        }
    
    def load_product_templates(self):
        for product_name in self.products_to_purchase:
            path = config.path_to_products_templates.joinpath(product_name)
            template = cv.imread(str(path) + ".png", cv.IMREAD_GRAYSCALE)
            self.product_templates[product_name] = template
    
    def load_templates(self):
        for template_name in CommonTemplate:
            path = config.path_to_templates.joinpath(template_name)
            template = cv.imread(str(path) + ".png")
            self.templates[template_name] = template
    
    def update_screenshot(self):
        img = ImageGrab.grab()
        self.screenshot = np.array(img, dtype=np.uint8)
        
        if self.screenshot.size != (1920, 1080):
            raise UnsupportedScreenResolution

    def test(self):
        # result = cv.GaussianBlur(result, (5,5), 0)
        # result = cv.Canny(result,100,200)
        
        # img[:, :, 0] = 0
        # img[:, :, 1] = 0
        
        # img_0 = cv.imread("m.jpg")
        
        # img = img_0.copy()
        
        # _, img = cv.threshold(img, 120, 255, cv.THRESH_BINARY)
        
        # nonzeros0 = cv.findNonZero(img[:, :, 0])
        # nonzeros1 = cv.findNonZero(img[:, :, 1])
        # nonzeros2 = cv.findNonZero(img[:, :, 2])
             
        # for x, y in nonzeros:
        #     img[x, y, 1] = 255
        
        # # img[75:425, :] = img_0[75:425, :]
        
        # cv.imwrite("mnew.png", img)
        # cv.imshow("result", img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        pass

    def find_template(self, template: CommonTemplate):
        self.templates[template]
        # cv.matchTemplate()
        return ...
    
    def find_product(self):
        pass
    
    def find_interface_element(self, element: InterfaceElement, region):
        if not isinstance(element, InterfaceElement):
            raise TypeError(f"expected InterfaceElement type, got \"{type(element)}\" instead")
        
        try:    
            return self._interface_elements_methods[element]()
        except KeyError:
            raise ValueError("unknown interface element")
    
    def _find_marketplace_window(self):
        logger.info("Нашёл!")
        return "lol"
    
    def _find_seller_in_trade_window(self):
        pass
    
    def _find_not_enough_money_window(self):
        pass
    
    def _find_confirm_button(self):
        pass
    
    def _find_cancel_button(self):
        pass
    
    def _find_okay_button(self):
        pass
    
    def _find_buy_button(self):
        pass
    
    def _find_product_name_in_confirm_window(self):
        pass
    
    def _find_price_in_confirm_window(self):
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