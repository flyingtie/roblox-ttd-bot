from pydantic import BaseModel

from src.templates import ProductTemplate


class ProductToPurchase(BaseModel):
    name: ProductTemplate
    max_price: int


products_to_purchase = (
    (ProductTemplate.TEST_PRODUCT, 1234),
)