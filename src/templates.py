from enum import StrEnum, auto


class Template(StrEnum):
    pass


class CommonTemplate(Template):
    MARKETPLACE = auto()


class ProductTemplate(Template):
    TEST_PRODUCT = auto()