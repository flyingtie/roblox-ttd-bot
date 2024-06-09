from enum import Enum, StrEnum, auto


class Coords(Enum):
    #TODO
    pass

class Window(StrEnum):
    CONFIRM_PURCHASE = auto()
    NOT_ENOUGH_MONEY = auto()
    NOT_FOUND = auto()
    IN_TRADE = auto()
    
class CommonTemplate(StrEnum):
    MARKETPLACE = auto()
    IN_TRADE = auto()
    CONFIRM_PURCHASE = auto()
    NOT_ENOUGH_MONEY = auto()
    NOT_FOUND = auto()
    GEM = auto()

class Product(StrEnum):
    HYPER_UPGRADED_TITAN_SPEAKERMAN = auto()
    DJ_TV_MAN = auto()
    SPEAKER_REPAIR_DRONE = auto()
    ENGINEER_CAMERAMAN = auto()
    SPIDER_TV = auto()