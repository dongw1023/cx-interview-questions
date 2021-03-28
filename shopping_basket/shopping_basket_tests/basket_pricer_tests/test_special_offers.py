import pytest
from shopping_basket.basket_pricer.speical_offers import SpecialOffers


class TestOffer:
    def get_instance(self):
        return SpecialOffers()

    @pytest.mark.parametrize(
        "rule_template", ["buy $buy get $free free", "$discount% discount"]
    )
    def test_get_rule_func(self, rule_template):
        special_offer = self.get_instance()
        assert callable(special_offer.get_rule_func(rule_template))

    @pytest.mark.parametrize("rule_template", [None, "", "no rule template"])
    def test_get_rule_func_fail(self, rule_template):
        special_offer = self.get_instance()
        with pytest.raises(NotImplementedError):
            special_offer.get_rule_func(rule_template)

    @pytest.mark.parametrize(
        "products, discount, expected",
        [([{"name": "Biscuits", "price": 1.20}], 25, 1.20 * 0.25), ([], 25, 0)],
    )
    def test_rule_discount(self, products, discount, expected):
        special_offer = self.get_instance()
        _discount = special_offer.rule_discount(products, discount=discount)
        assert _discount == expected

    @pytest.mark.parametrize(
        "products, buy, free, expected",
        [
            (
                [{"name": "Biscuits", "price": 1.20} for _ in range(2)],
                2,
                1,
                0,
            ),
            (
                [{"name": "Biscuits", "price": 1.20} for _ in range(3)],
                2,
                1,
                1.20,
            ),
            (
                [{"name": "Biscuits", "price": 1.20} for _ in range(6)],
                2,
                1,
                1.20 * 2,
            ),
            ([], 2, 1, 0),
        ],
    )
    def test_rule_buy_x_get_y_free(self, products, buy, free, expected):
        special_offer = self.get_instance()
        _discount = special_offer.rule_buy_x_get_y_free(products, buy=buy, free=free)
        assert _discount == expected
