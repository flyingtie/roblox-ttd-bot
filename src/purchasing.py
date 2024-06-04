from typing import Iterable
from loguru import logger

from src.products_for_purchase import ProductForPurchase
from src.enums import Product

        
class PurchaseManager:
    def __init__(self, products_for_purchase: dict[Product, ProductForPurchase]):
        self.products_for_purchase = products_for_purchase
        
    def make_purchase_decision(self, product_name: Product, price: int) -> bool:
        product = self.products_for_purchase[product_name]
        if product.max_price >= price:
            logger.info(f"Решил купить {product_name} за {price}")
            return True
        logger.info(f"Решил не покупать {product_name} за {price}")
        return False