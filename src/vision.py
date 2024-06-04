import cv2 as cv
import numpy as np
import random
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

    def search_windows(self) -> Union[Window, None]:
        for window in Window:
            if window != Window.CONFIRM_PURCHASE:
                if self._find_template(
                    self.screenshot, 
                    self.templates[window][387 - 1:447, 576 - 1:1343], 
                    0.99
                ) is None:
                    continue
            else:
                if not self.find_confirm_window():
                    continue
            return window
    
    def search_products(self) -> Generator[tuple[Product, tuple[tuple[int, int], tuple[int, int]]], None, None]:
        for product in self.products_for_purchase:
            prod_templ = self.product_templates[product]
            region = self._find_template(self.screenshot, prod_templ, 0.94)
            if region is None:
                logger.debug(f"product {product} not found")
                continue
            logger.debug(f"found product {product}")
            yield product, region

    def find_marketplace(self) -> bool:
        screenshot = self.screenshot
        if self._find_template(
            screenshot, 
            self.templates[CommonTemplate.MARKETPLACE][216 - 1:254, 770 - 1:1218], 
            val=0.99
        ) is None:
            return False
        return True

    def find_confirm_window(self) -> bool:
        screenshot = self.screenshot
        if self._find_template(
            screenshot,
            self.templates[CommonTemplate.CONFIRM_PURCHASE][277 - 1:347, 604 - 1:1315],
            val=0.99
        ) is None:
            return False
        return True
        
    def confirm_purchase(self, product: Product, price: int) -> tuple[bool, int]:
        confirm_text_image = self.screenshot[352 - 1:664, 312 - 1:1607]
        
        text_img = cv.cvtColor(confirm_text_image, cv.COLOR_BGR2GRAY)
        text_img = cv.threshold(text_img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        text_img = cv.copyMakeBorder(text_img, 20, 20, 0, 0, cv.BORDER_CONSTANT, value=(255, 255, 255))
        text_img = self.resize_image(text_img, 0.5)

        if (raw_string := self._get_text_from_image(text_img)) is None:
            return False
        
        if (product_data := self._parse_raw_confirm_text(raw_string)) is None:
            return False
        
        product_name = product.replace("_", "")
        

        return all(
            [
                product_name == product_data[0], 
                str(price)[:-3] == str(product_data[1])[:-3]
            ]
        ), product_data[1]
    
    @staticmethod
    def _parse_raw_confirm_text(raw_text: str) -> Union[tuple[str, int], None]:
        match_groups = re.match(r"^.+?buy([a-z]+?)from.+?for([0-9,.]+)gems.*?$", raw_text)
        
        if not match_groups:
            return None
        
        name_product = match_groups.group(1)

        price = int(re.sub(r"[,.]", "", match_groups.group(2)))

        logger.debug(f"parsed confirm text: {name_product=}, {price=}")
        return name_product, price

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

        template = self.templates[CommonTemplate.GEM]
        if (gem_region := self._find_template(price_region_image, template, val=0.95)) is None:
            logger.debug("Gem not found")
            return None
        
        top_left_gem, bottom_right_gem = gem_region
        price_image = price_region_image[
            top_left_gem[0] - 1:bottom_right_gem[0],
            :top_left_gem[1]
        ]

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
        
        raw_string_price = self._get_text_from_image(
            img, 
            psm=7, 
            char_whitelist="1234567890.kmb"
        )

        if (price := self._validate_price(raw_string_price)) is None:
            logger.debug(f"could not convert '{price}' to an integer")
            return None
        return price

    @staticmethod
    def _np_to_pil_image(img: MatLike) -> ImageGrab.Image:
        img_cv = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        return ImageGrab.Image.fromarray(img_cv)
    
    @staticmethod
    def _pil_image_to_np(img: ImageGrab.Image) -> MatLike:
        np_img = np.asarray(img)
        return cv.cvtColor(np_img, cv.COLOR_RGB2BGR)

    @staticmethod
    def resize_image(img: MatLike, coeff: float) -> MatLike:
        return cv.resize(
            img, 
            (int(img.shape[1] / coeff), int(img.shape[0] / coeff)),
            cv.INTER_AREA
        )

    @staticmethod
    def _find_template(
        image: MatLike, 
        template: MatLike,
        val: float
    ) -> Union[tuple[tuple[int, int], tuple[int, int]], None]:
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

        y_templ, x_templ = template.shape
        
        res = cv.matchTemplate(image, template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv.minMaxLoc(res)

        
        top_left = (max_loc[1], max_loc[0])
        bottom_right = (top_left[0] + y_templ - 1, top_left[1] + x_templ - 1)

        logger.debug(f"found template: {max_val=}, {max_loc=}")

        if max_val <= val:
            return None
        
        if config.show_debug_pics and image.shape == (1080, 1920):
            img = image.copy()

            cv.rectangle(img, top_left[::-1], bottom_right[::-1], color=(203, 192, 255), lineType=cv.FILLED)
            cv.imshow(
                "ttd_bot", 
                img[
                    top_left[0] - 1:bottom_right[0], 
                    top_left[1] - 1:bottom_right[1]
                ]
            )
            cv.waitKey(1)

        return top_left, bottom_right
    
    def _get_text_from_image(
        self,
        img: MatLike, 
        psm: int = 3, 
        char_whitelist: str = ""
    ) -> str:
        img = self._np_to_pil_image(img)

        with PyTessBaseAPI(lang="eng") as api:
            api.SetVariable("tessedit_char_whitelist", char_whitelist)
            api.SetPageSegMode(psm)
            api.SetImage(img)
            raw_text: str = api.GetUTF8Text()

        text = raw_text.lower().replace(" ", "").replace("\n", "")
        logger.debug(f"raw pre-formatted recognized text: '{text}'")
        return text

    @staticmethod
    def _validate_price(price: str) -> Union[int, None]:
        price = price.replace(" ", "").lower()
        
        if price.isdigit():
            return int(price)
        
        match_groups = re.match(r"^(\d+|\d+\.\d+)([kmb])$", price)
        
        if not match_groups:
            return None
        
        price = float(match_groups.group(1))
    
        match match_groups.group(2):
            case "k":
                price *= 1000
            case "m":
                price *= 1_000_000
            case "b":
                price *= 1_000_000_000
        
        logger.debug(f"integer price: {int(price)}")
        return int(price)