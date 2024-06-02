import cv2 as cv
import numpy as np
import re

from tesserocr import PyTessBaseAPI
from loguru import logger
from cv2.typing import MatLike
from PIL import ImageGrab
from typing import Union, Generator

from src.exceptions import UnsupportedScreenResolution, PriceValidationError
from src.products_for_purchase import ProductForPurchase
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
    
    def __init__(self, products_for_purchase: dict[Product, ProductForPurchase]):  
        self.products_for_purchase = products_for_purchase
        self.product_templates = dict()
        self.templates = dict()
    
    def load_product_templates(self):
        for product_name in self.products_for_purchase:
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
        img = ImageGrab.grab(all_screens=True)

        if img.size != (1920, 1080):
            raise UnsupportedScreenResolution
        
        self.screenshot = self._pil_image_to_np(img)

    def find_marketplace(self) -> bool:
        screenshot = self.screenshot
        if self._find_template(
            screenshot, 
            self.templates[CommonTemplate.MARKETPLACE][216:254, 770:1218], 
            val=0.99
        ) is None:
            return False
        return True

    def search_products(self) -> Generator[tuple[Product, tuple[tuple[int, int], tuple[int, int]]], None, None]:
        for product in self.products_for_purchase:
            prod_templ = self.product_templates[product]
            region = self._find_template(self.screenshot, prod_templ, 0.99)
            if region is None:
                continue
            yield product, region

    def get_product_price(
            self, 
            top_left: tuple[int, int], 
            bottom_right: tuple[int, int]
    ) -> Union[int, None]:
        """Returns the product price from the product region 

        Parameters:
            top_left: y and x coordinates of the top left corner of the product region.
            bottom_right: y and x coordinates of the bottom right corner of the product region.
        
        """

        price_region_image = self.screenshot[
            bottom_right[0] - 1:bottom_right[0] + 135,
            top_left[1] - 1:bottom_right[1] 
        ]

        if config.show_debug_pics:
            cv.imshow("price region image", price_region_image)
            cv.waitKey(0)

        template = self.templates[CommonTemplate.GEM]
        if (gem_region := self._find_template(price_region_image, template, val=0.96)) is None:
            logger.debug("Gem not found")
            return None
        
        top_left_gem, bottom_right_gem = gem_region
        price_image = price_region_image[
            top_left_gem[0] - 1:bottom_right_gem[0],
            :top_left_gem[1]
        ]
        
        if config.show_debug_pics:
            cv.imshow("price_image", price_image)
            cv.waitKey(0)

        if (price := self._get_price_from_image(price_image)) is None:
            logger.debug("OCR returned None")
            return None      
        return price
    
    def _get_price_from_image(self, img: MatLike) -> Union[int, None]:
        """Returns the price from the image"""

        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        img = cv.copyMakeBorder(img, 20, 20, 20, 20, cv.BORDER_CONSTANT, value=(255, 255, 255))
        img = self.resize_image(img, 0.5)

        if config.show_debug_pics:
            cv.imshow("processed price image", img)
            cv.waitKey(0)
        
        img = self._np_to_pil_image(img)
        
        str_price = self._get_text_from_image(
            img, 
            psm=7, 
            char_whitelist="1234567890.kmb"
        )

        logger.debug(f"recognized price: '{str_price}'")

        try:
            return self._validate_price(str_price)
        except PriceValidationError as e:
            logger.debug(e)
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
        template: MatLike,
        val: float
    ) -> Union[tuple[tuple[int, int], tuple[int, int]], None]:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

        y_templ, x_templ = template.shape
        
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(res)

        
        top_left = (max_loc[1], max_loc[0])
        bottom_right = (top_left[0] + y_templ - 1, top_left[1] + x_templ - 1)
        
        if config.show_debug_pics:
            cv.imshow(
                "detected template", 
                img[
                    top_left[0] - 1:bottom_right[0], 
                    top_left[1] - 1:bottom_right[1]
                ]
            )
            cv.waitKey(0)

        if max_val < val:
            return None
        
        return top_left, bottom_right
    
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
            raise PriceValidationError(f"could not convert '{price}' to an integer")
        
        price = float(match_groups.group(1))
    
        match match_groups.group(2):
            case "k":
                price *= 1000
            case "m":
                price *= 1_000_000
            case "b":
                price *= 1_000_000_000
        
        logger.debug(f"integer price: {price}")
        return int(price)