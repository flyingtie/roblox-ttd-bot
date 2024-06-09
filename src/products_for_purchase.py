from pydantic import BaseModel

from src.enums import Product


class ProductForPurchase(BaseModel):
    name: Product
    max_price: int


prods_to_purch = (
    (Product.HYPER_UPGRADED_TITAN_SPEAKERMAN, 0),
    (Product.DJ_TV_MAN, 0),
    (Product.SPEAKER_REPAIR_DRONE, 0),
    (Product.ENGINEER_CAMERAMAN, 0),
    (Product.SPIDER_TV, 0)
)

products_for_purchase = {
    product[0]: ProductForPurchase(
        name=product[0], 
        max_price=product[1]
    ) for product in prods_to_purch
}