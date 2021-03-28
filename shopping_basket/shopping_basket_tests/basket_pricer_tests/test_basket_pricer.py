import pytest
from shopping_basket.basket_pricer.basket_pricer import BasketPricer

_catalogue = {
    "Baked Beans": 0.99,
    "Biscuits": 1.20,
    "Sardines": 1.89,
    "Shampoo (Small)": 2.00,
    "Shampoo (Medium)": 2.50,
    "Shampoo (Large)": 3.50,
}
_basket = {"Baked Beans": 4, "Biscuits": 1}
_offers = {
    "Baked Beans": {
        "name": "buy 2 get 1 free",
        "rule": "buy $buy get $free free",
        "kwargs": {"buy": 2, "free": 1},
    },
    "Sardines": {
        "name": "25% discount",
        "rule": "$discount% discount",
        "kwargs": {"discount": 25},
    },
}


class TestBasketPricer:
    @pytest.mark.parametrize(
        "basket, catalogue, expected",
        [(_basket, _catalogue, 4 * 0.99 + 1.20), ({}, _catalogue, 0)],
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
                    _offers.get("Baked Beans").get("name"): {
                        "offer": _offers.get("Baked Beans"),
                        "products": [
                            {
                                "name": "Baked Beans",
                                "price": _catalogue.get("Baked Beans"),
                            }
                            for _ in range(_basket.get("Baked Beans"))
                        ],
                    }
                },
            )
        ],
    )
    def test_products_by_offer(self, basket, catalogue, offers, expected):
        basket_pricer = BasketPricer(basket, catalogue, offers)
        assert basket_pricer.products_by_offer() == expected

    @pytest.mark.parametrize(
        "basket, catalogue, offers",
        [(_basket, _catalogue, _offers), ([], [], [])],
    )
    def test_calculate_discount(self, basket, catalogue, offers):
        def mock_func(products, **kwargs):
            return 1.99

        for offer in offers:
            offers[offer]["func"] = mock_func

        basket_pricer = BasketPricer(_basket, _catalogue, _offers)
        discount = basket_pricer.calculate_discount()
        assert discount == 1.99

    @pytest.mark.parametrize(
        "basket, catalogue, offers, product",
        [(_basket, _catalogue, _offers, "Baked Beans")],
    )
    def test_is_product_in_basket(self, basket, catalogue, offers, product):
        basket_pricer = BasketPricer(_basket, _catalogue, _offers)
        assert basket_pricer.is_product_in_basket(product)

    @pytest.mark.parametrize(
        "basket, catalogue, offers, product",
        [(_basket, _catalogue, _offers, ""), (_basket, _catalogue, _offers, None)],
    )
    def test_is_product_in_basket_fail(self, basket, catalogue, offers, product):
        basket_pricer = BasketPricer(_basket, _catalogue, _offers)
        assert basket_pricer.is_product_in_basket(product) == False

    def test_summary(self, monkeypatch):
        def mock_calculate_sub_total_price(self=None):
            return 10.99

        def mock_calculate_discount(self=None):
            return 2.99

        monkeypatch.setattr(
            BasketPricer, "calculate_sub_total_price", mock_calculate_sub_total_price
        )
        monkeypatch.setattr(BasketPricer, "calculate_discount", mock_calculate_discount)
        basket_pricer = BasketPricer(_basket, _catalogue, _offers)
        sub_total, discount, total = basket_pricer.summary()

        assert sub_total == mock_calculate_sub_total_price()
        assert discount == mock_calculate_discount()
        assert total == sub_total - discount
