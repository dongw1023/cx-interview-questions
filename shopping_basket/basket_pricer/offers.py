from string import Template

RULE_TYPE_BUY_X_GET_Y_FREE = 0
RULE_TYPE_DISCOUNT = 1


class Offers:
    def __init__(self):
        self._rules = {
            RULE_TYPE_BUY_X_GET_Y_FREE: Template("buy $buy get $free free"),
            RULE_TYPE_DISCOUNT: Template("$discount% discount"),
        }
        self._offers = {}

    def add_offer(self, product, rule_type, **kwargs):
        """

        :param product:
        :type product:
        :param rule_type:
        :type rule_type:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        self._offers[product.name] = self._rules[rule_type].substitute(kwargs)
        return self._offers
