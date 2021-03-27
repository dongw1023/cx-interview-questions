from shopping_basket.basket_pricer.product import Product
from shopping_basket.basket_pricer.catalogue_exceptions import (
    ProductAlreadyExistException,
    ProductNotValidException,
)


class Catalogue:
    def __init__(self):
        # store all products
        self._catalogue = {}

    def add_product(self, product=None):
        """
        Add a product to current catalogue
        :param product: The product which will be added to the catalogue
        :type product: Product
        :return: The new catalogue
        :rtype: dict
        """
        if not product or not isinstance(product, Product):
            raise ProductNotValidException(
                f"Found product {type(product)}, Expect type Product!"
            )

        if product.name in self._catalogue:
            raise ProductAlreadyExistException(
                f"The product {product.name} is already exist!"
            )

        self._catalogue[product.name] = product
        return self._catalogue

    def get_count(self):
        """
        Count of products
        :return:
        :rtype:
        """
        return len(self._catalogue)
