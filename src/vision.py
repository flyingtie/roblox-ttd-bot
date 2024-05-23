import cv2 as cv
import numpy as np

from cv2.typing import MatLike
from PIL import ImageGrab
from typing import Iterable, Optional

from src.exceptions import UnsupportedScreenResolution
from src.products_to_purchase import ProductToPurchase
from src.templates import ProductTemplate, Template
from src.config import config


class Vision:
    product_templates: list[tuple[ProductToPurchase, MatLike]]
    templates: list[tuple[Template, MatLike]]
    screenshot: Optional[MatLike]
    
    def __init__(self, products_to_purchase: Iterable[ProductToPurchase]):
        self.products_to_purchase = products_to_purchase
        self.product_templates = list()
        self.templates = list()
        self.screenshot = None
    
    def load_templates(self):
        for template_name in Template:
            path = config.path_to_templates.joinpath(template_name)
            template = cv.imread(str(path))
            self.templates.append((template_name, template))
    
    def load_product_templates(self):
        for product in self.products_to_purchase:
            path = config.path_to_products_templates.joinpath(product.name)
            template = cv.imread(str(path), cv.IMREAD_GRAYSCALE)
            self.product_templates.append((product, template))
    
    def update_screenshot(self):
        self.screenshot = ImageGrab.grab()
        
        if self.screenshot.size != (1920, 1080):
            raise UnsupportedScreenResolution("Неподдерживаемое разрешение экрана!")
    
class ImageWorker:
    def __init__(self):
        pass

# image_1 = cv.imread('templates/no_money 1366 768.png')
# img_2 = cv.imread('templates/marketplace 1366 768.png', cv.IMREAD_GRAYSCALE)


# # ret, img = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

# # img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

# cv.imshow("result", img)
# cv.waitKey(0)
# cv.destroyAllWindows()