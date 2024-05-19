from pydantic import BaseModel


class ProductToPurchase(BaseModel):
    name: str
    max_price: int


products_data = (
    ("test_name", 123),
    ("test_name2", 777)
)