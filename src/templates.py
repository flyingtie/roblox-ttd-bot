from enum import StrEnum


class Template(StrEnum):
    pass


class CommonTemplate(Template):
    MARKETPLACE = "marketplace"


class ProductTemplate(Template):
    TEST_PRODUCT = "test_product"