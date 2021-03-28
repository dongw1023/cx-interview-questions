import pytest
from shopping_basket.basket_pricer.basket_pricer import BasketPricer


def mock_func(products, **kwargs):
    return 1.99 * 0.25 * 2


_catalogue = {"product_1": 1.99}
_basket = {"product_1": 2}
_offers = {
    "product_1": {
        "name": "25% discount",
        "rule": "$discount% discount",
        "kwargs": {"discount": 25},
        "func": mock_func,
    }
}


class TestBasketPricer:
    @pytest.mark.parametrize(
        "basket, catalogue, expected",
        [(_basket, _catalogue, 3.98)],
    )
    def test_calculate_sub_total_price(self, basket, catalogue, expected):

        basket_pricer = BasketPricer(basket, catalogue, {})
        assert basket_pricer.calculate_sub_total_price() == expected

    @pytest.mark.parametrize(
        "basket, catalogue, offers, expected",
        [
            (
                _basket,
                _catalogue,
                _offers,
                {
                    _offers.get("product_1").get("name"): {
                        "offer": _offers.get("product_1"),
                        "products": ["product_1", "product_1"],
                    }
                },
            )
        ],
    )
    def test_products_by_offer(self, basket, catalogue, offers, expected):
        basket_pricer = BasketPricer(basket, catalogue, offers)
        assert basket_pricer.products_by_offer() == expected

    @pytest.mark.parametrize(
        "basket, catalogue, offers, expected",
        [
            (
                _basket,
                _catalogue,
                _offers,
                1.99 * 2 * 0.25,
            )
        ],
    )
    def test_calculate_discount(self, basket, catalogue, offers, expected):

        basket_pricer = BasketPricer(_basket, _catalogue, _offers)
        discount = basket_pricer.calculate_discount()
        assert discount == expected
