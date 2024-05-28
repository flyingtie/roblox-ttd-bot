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
    NOT_FOUND = auto()
    IN_TRADE = auto()
    
class CommonTemplate(StrEnum):
    MARKETPLACE = auto()
    IN_TRADE = auto()
    CONFIRM_PURCHASE = auto()
    NOT_ENOUGH_MONEY = auto()
    NOT_FOUND = auto()

class Product(StrEnum):
    HYPER_UPGRADED_TITAN_SPEAKERMAN = auto()
    DJ_TV_MAN = auto()
    # SPEAKER_REPAIR_DRONE = auto()
    # SPIDER_TV = auto()


