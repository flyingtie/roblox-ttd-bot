from pydantic import BaseModel

from src.enums import Product


class ProductForPurchase(BaseModel):
    name: Product
    max_price: int


prods_to_purch = (
    (Product.HYPER_UPGRADED_TITAN_SPEAKERMAN, 9_999_999_999),
    (Product.DJ_TV_MAN, 999_999_999),
    (Product.SPEAKER_REPAIR_DRONE, 4000)
)

products_for_purchase = {
    product[0]: ProductForPurchase(
        name=product[0], 
        max_price=product[1]
    ) for product in prods_to_purch
}