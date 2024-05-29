import cv2 as cv
import numpy as np
import re

from loguru import logger
from enum import Enum, auto
from cv2.typing import MatLike
from PIL import ImageGrab
from numpy.typing import NDArray
from typing import Union
from pathlib import Path
from matplotlib import pyplot as plt

from src.exceptions import UnsupportedScreenResolution, PriceValidationError
from src.products_to_purchase import ProductToPurchase
from src.enums import (
    Product, 
    CommonTemplate,
    Window,
    Button
)


class Vision:
    product_templates: dict[Product, MatLike]
    templates: dict[CommonTemplate, MatLike]
    screenshot: NDArray
    
    def __init__(
            self, 
            products_to_purchase: dict[Product, ProductToPurchase],
            path_to_templates: Path,
            path_to_product_templates: Path
        ):

        self.path_to_templates = path_to_templates
        self.path_to_product_templates = path_to_product_templates    
        self.products_to_purchase = products_to_purchase
        self.product_templates = dict()
        self.templates = dict()
    
    def load_product_templates(self):
        for product_name in self.products_to_purchase:
            path = self.path_to_product_templates.joinpath(product_name + ".png")
            template = cv.imread(str(path), cv.IMREAD_GRAYSCALE)
            if template is None:
                raise FileNotFoundError(path)
            self.product_templates[product_name] = template
    
    def load_templates(self):
        for template_name in CommonTemplate:
            path = self.path_to_templates.joinpath(template_name + ".png")
            template = cv.imread(str(path), cv.IMREAD_GRAYSCALE)
            if template is None:
                raise FileNotFoundError(path)
            self.templates[template_name] = template
    
    def update_screenshot(self):
        img = ImageGrab.grab()
        self.screenshot = np.array(img, dtype=np.uint8)
        
        if self.screenshot.size != (1920, 1080):
            raise UnsupportedScreenResolution

    @staticmethod
    def _find_template(img: Union[MatLike, NDArray], template: Union[MatLike, NDArray]) -> tuple:
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, top_left = cv.minMaxLoc(res)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        if 1 != max_val:
            return None
        return (top_left, bottom_right)
    
    @staticmethod
    def get_text_from_image(img) -> str:
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