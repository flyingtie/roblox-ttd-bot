from typing import Iterable

from src.products_to_purchase import ProductToPurchase


# class Product: 
#     name: str
#     price: int
    
#     def __init__(self, name: str, price: int):
#         self.name = name
#         self.price = price
        
class PurchaseManager:
    def __init__(self, products_to_purchase: Iterable[ProductToPurchase]):
        self.products_to_purchase = products_to_purchase