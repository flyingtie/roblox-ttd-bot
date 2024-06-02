from typing import Iterable

from src.products_for_purchase import ProductForPurchase
from src.enums import Product

# class Product: 
#     name: str
#     price: int
    
#     def __init__(self, name: str, price: int):
#         self.name = name
#         self.price = price
        
class PurchaseManager:
    def __init__(self, products_for_purchase: dict[Product, ProductForPurchase]):
        self.products_for_purchase = products_for_purchase
        
    def make_purchase_decision(self, product_name: Product, price: int) -> bool:
        product = self.products_for_purchase[product_name]
        if product.max_price >= price:
            return True
        return False