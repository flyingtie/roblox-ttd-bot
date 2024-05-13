from bot.templates import ImgsDirsTemplates


class Bot:
    def __init__(self, products_to_purchase: list[tuple[str, int]]):
        self.products_to_purchase = products_to_purchase

    def run(self):
        pass
