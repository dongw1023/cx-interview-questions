import pytest
from shopping_basket.basket_pricer.product import Product
from shopping_basket.basket_pricer.offers import (
    Offers,
    RULE_TYPE_BUY_X_GET_Y_FREE,
    RULE_TYPE_DISCOUNT,
)


class TestOffer:
    @pytest.mark.parametrize(
        "product, rule, kwargs, expected",
        [
            (
                Product("product_1", 1.99),
                RULE_TYPE_BUY_X_GET_Y_FREE,
                {"buy": 2, "free": 1},
                "buy 2 get 1 free",
            ),
            (
                Product("product_1", 1.99),
                RULE_TYPE_DISCOUNT,
                {"discount": 25},
                "25% discount",
            ),
        ],
    )
    def test_add_offer(self, product, rule, kwargs, expected):

        offers = Offers()
        products_offers = offers.add_offer(product, rule, **kwargs)

        assert products_offers[product.name] == expected
