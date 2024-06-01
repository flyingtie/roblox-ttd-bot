import cv2 as cv
import numpy as np
import re

from tesserocr import PyTessBaseAPI
from loguru import logger
from enum import Enum, auto
from cv2.typing import MatLike
from PIL import ImageGrab
from typing import Union
from pathlib import Path
from matplotlib import pyplot as plt

from src.exceptions import UnsupportedScreenResolution, PriceValidationError
from src.products_to_purchase import ProductToPurchase
from src.config import config
from src.enums import (
    Product, 
    CommonTemplate,
    Window,
    Button
)


class Vision:
    product_templates: dict[Product, MatLike]
    templates: dict[CommonTemplate, MatLike]
    screenshot: MatLike
    
    def __init__(self, products_to_purchase: dict[Product, ProductToPurchase]):  
        self.products_to_purchase = products_to_purchase
        self.product_templates = dict()
        self.templates = dict()
    
    def load_product_templates(self):
        for product_name in self.products_to_purchase:
            path = config.path_to_product_templates.joinpath(product_name + ".png")
            template = cv.imread(str(path))
            if template is None:
                raise FileNotFoundError(path)
            self.product_templates[product_name] = template
    
    def load_templates(self):
        for template_name in CommonTemplate:
            path = config.path_to_templates.joinpath(template_name + ".png")
            template = cv.imread(str(path))
            if template is None:
                raise FileNotFoundError(path)
            self.templates[template_name] = template
    
    def update_screenshot(self):
        img = ImageGrab.grab()
        self.screenshot = self._pil_image_to_np(img)

        if img != (1920, 1080):
            raise UnsupportedScreenResolution

    def test(self):
        # img_temp = self.templates[CommonTemplate.MARKETPLACE]
        # img = cv.imread("templates/tests/test_chars.png", cv.IMREAD_GRAYSCALE)
        # img = img_temp[348:668, 451:1469]
        # img = img_temp[508:535, 1011:1084]
        # img = cv.resize(img, (int(img.shape[1]/1.7), int(img.shape[0]/1.7)), cv.INTER_AREA)
        # img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        # img = cv.copyMakeBorder(img, 20, 20, 0, 0, cv.BORDER_CONSTANT, value=(255, 255, 255))
        # cv.imshow("result", img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        # img_pil = self._np_to_pil_image(img)
        # print(self._get_text_from_image(img_pil))
        pass

    def get_price_from_region(
            self, 
            img: MatLike,
            top_left: tuple[int, int], 
            bottom_right: tuple[int, int]
    ) -> Union[int, None]:
        """Returns the price from the specified region

        Parameters:
            top_left: x and y coordinates of the top left corner of the region.
            bottom_right: x and y coordinates of the bottom right corner of the region.
        """

        img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = self.resize_image(img, 1.7)
        img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        cv.imshow("result", img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        img = self._np_to_pil_image(img)
        
        str_price = self._get_text_from_image(
            img, 
            psm=7, 
            char_whitelist="1234567890.kmb"
        )
        
        try:
            return self._validate_price(str_price)
        except PriceValidationError as e:
            logger.error(e)
            return None

    @staticmethod
    def resize_image(img: MatLike, coeff: float) -> MatLike:
        return cv.resize(
            img, 
            (int(img.shape[1] / coeff), int(img.shape[0] / coeff)),
            cv.INTER_AREA
        )

    @staticmethod
    def _np_to_pil_image(img: MatLike) -> ImageGrab.Image:
        img_cv = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        return ImageGrab.Image.fromarray(img_cv)
    
    @staticmethod
    def _pil_image_to_np(img: ImageGrab.Image) -> MatLike:
        np_img = np.asarray(img)
        return cv.cvtColor(np_img, cv.COLOR_RGB2BGR)

    @staticmethod
    def _find_template(
        img: MatLike, 
        template: MatLike
    ) -> tuple[int, int]:
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, top_left = cv.minMaxLoc(res)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        if 1 != max_val:
            return None
        return (top_left, bottom_right)
    
    @staticmethod
    def _get_text_from_image(
        img: ImageGrab.Image, 
        psm: int, 
        char_whitelist: str = ""
    ) -> str:
        with PyTessBaseAPI(lang="eng") as api:
            api.SetVariable("tessedit_char_whitelist", char_whitelist)
            api.SetPageSegMode(psm)
            api.SetImage(img)
            text: str = api.GetUTF8Text()
        return text.lower().replace(" ", "").replace("\n", "")

    @staticmethod
    def _validate_price(price: str) -> int:
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