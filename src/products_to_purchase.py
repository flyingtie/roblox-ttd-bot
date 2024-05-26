from pydantic import BaseModel

from src.templates import ProductTemplate

# TODO: Сменить нахрен енумчик на другой
class ProductToPurchase(BaseModel):
    name: ProductTemplate
    max_price: int


products_to_purchase = (
    (ProductTemplate.TEST_PRODUCT, 1234),
)