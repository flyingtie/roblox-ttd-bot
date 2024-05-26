from enum import Enum, StrEnum, auto


class InterfaceElement(Enum):
    pass

class Button(InterfaceElement):
    CANCEL = auto()
    CONFIRM = auto()
    BUY = auto()
    OKAY = auto()

class Window(InterfaceElement):
    MARKETPLACE = auto()
    NOT_ENOUGH_MONEY = auto()
    SELLER_IN_TRADE = auto()
    
class Template(StrEnum):
    pass
    
class CommonTemplate(Template):
    MARKETPLACE = auto()

class Product(StrEnum):
    TEST_PRODUCT = auto()
