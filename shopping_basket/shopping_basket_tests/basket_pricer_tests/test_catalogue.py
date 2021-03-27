import pytest
from random import uniform
from shopping_basket.basket_pricer.catalogue import Catalogue
from shopping_basket.basket_pricer.product import Product
from shopping_basket.basket_pricer.catalogue_exceptions import (
    ProductAlreadyExistException,
    ProductNotValidException,
)

product_list = [Product(f"product_{i}", uniform(1, 10)) for i in range(5)]


class TestCatalogue:
    @pytest.mark.parametrize("product", [None, "product", 3.99])
    def test_add_product_not_valid_value(self, product):
        catalogue = Catalogue()
        with pytest.raises(ProductNotValidException):
            catalogue.add_product(product)

    @pytest.mark.parametrize("product", [Product("product_1", 1.99)])
    def test_add_product_already_exist(self, product):
        catalogue = Catalogue()
        catalogue.add_product(product)
        with pytest.raises(ProductAlreadyExistException):
            catalogue.add_product(product)

    @pytest.mark.parametrize(
        "products, count", [(product_list, len(product_list)), ([], 0)]
    )
    def test_get_count(self, products, count):
        catalogue = Catalogue()
        for product in products:
            catalogue.add_product(product)
        assert count == catalogue.get_count()
