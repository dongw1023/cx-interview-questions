import pytest
from shopping_basket.basket_pricer.speical_offers import SpecialOffers


class TestOffer:
    @pytest.mark.parametrize(
        "product, rule_template, kwargs, expected",
        [
            (
                {"name": "product_1", "price": 1.99},
                "buy $buy get $free free",
                {"buy": 2, "free": 1},
                {
                    "rule": "buy $buy get $free free",
                    "name": "buy 2 get 1 free",
                    "kwargs": {"buy": 2, "free": 1},
                },
            ),
            (
                {"name": "product_2", "price": 3.99},
                "$discount% discount",
                {"discount": 25},
                {
                    "rule": "$discount% discount",
                    "name": "25% discount",
                    "kwargs": {"discount": 25},
                },
            ),
        ],
    )
    def test_add_offer(self, product, rule_template, kwargs, expected):

        offers = SpecialOffers()
        products_offers = offers.add_offer(product, rule_template, **kwargs)
        assert products_offers[product.get("name")]["rule"] == expected["rule"]
        assert products_offers[product.get("name")]["name"] == expected["name"]
        assert products_offers[product.get("name")]["kwargs"] == expected["kwargs"]
