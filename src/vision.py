import cv2 as cv
import numpy as np

from PIL import ImageGrab
from typing import Iterable

from src.products_to_purchase import ProductToPurchase
from src.templates import ProductTemplate
from src.config import config

class Vision:    
    def __init__(self):
        self.products_templates = list()
    
    def load_products_templates(self, products_templates: Iterable[ProductToPurchase]):
        for product in products_templates:
            path = config.path_to_products_templates.joinpath(product.name)
            template = cv.imread(str(path))
            self.products_templates.append((product, template))
    
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