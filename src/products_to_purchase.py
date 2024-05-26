from pydantic import BaseModel

from src.enums import Product


class ProductToPurchase(BaseModel):
    name: Product
    max_price: int


prod_to_purch = (
    (Product.TEST_PRODUCT, 1234),
)

products_to_purchase = {
    product[0]: ProductToPurchase(
        name=product[0], 
        max_price=product[1]
    ) for product in prod_to_purch
}