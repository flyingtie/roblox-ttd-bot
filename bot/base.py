from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float

class Page(BaseModel):
    def __init__(self):
        pass

class Marketplace(BaseModel):
    def __init__(self):
        pass
