from pydantic import BaseModel


class ProductToPurchase(BaseModel):
    name: str
    max_price: int

class ProductsToPurchase(BaseModel):
    products: list[ProductToPurchase]