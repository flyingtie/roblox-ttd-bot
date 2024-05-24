from typing import Iterable

from src.products_to_purchase import ProductToPurchase
from src.templates import ProductTemplate

# class Product: 
#     name: str
#     price: int
    
#     def __init__(self, name: str, price: int):
#         self.name = name
#         self.price = price
        
class PurchaseManager:
    def __init__(self, products_to_purchase: dict[ProductTemplate, ProductToPurchase]):
        self.products_to_purchase = products_to_purchase
        
    def make_purchase_decision(self, product_name: ProductTemplate, price: int) -> bool:
        product = self.products_to_purchase[product_name]
        if product.max_price <= price:
            return True
        return False