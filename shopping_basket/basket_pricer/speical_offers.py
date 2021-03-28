from string import Template


class SpecialOffers:
    def __init__(self):

        self._default_rules = ["buy $buy get $free free", "$discount% discount"]
        self._rules = {name: Template(name) for name in self._default_rules}
        self._rules_func = {
            "buy $buy get $free free": self.rule_buy_x_get_y_free,
            "$discount% discount": self.rule_discount,
        }
        self._offers = {}

    def add_rule(self, rule_template):
        """
        Add a rule to the offer, such as buy x get y free
        :param rule_template: The template for the rule
        :type rule_template: str
        :return: All rules
        :rtype: dict
        """
        self._rules[rule_template] = Template(rule_template)
        return self._rules

    def get_rule_func(self, rule_template):
        """
        Get the funcution to calculate the offer
        :param rule_template: The rule template
        :type rule_template:  str
        :return: The function
        :rtype: func
        """
        return self._rules_func.get(rule_template)

    def add_offer(self, product, rule_template, **kwargs):
        """
        Add an offer to a product
        :param product: The product with the offer
        :type product: str
        :param rule_template: The template for the rule
        :type rule_template: str
        :param kwargs: Parameters for the rule, such as {discount:25}, {buy: 2, free:1}
        :type kwargs:
        :return: All offers
        :rtype: dict
        """

        self._offers[product] = {
            "rule": rule_template,
            "name": self._rules[rule_template].substitute(kwargs),
            "func": self.get_rule_func(rule_template),
            "kwargs": kwargs,
        }
        return self._offers

    def get_offers(self):
        """
        Get available offers
        :return: All offers
        :rtype: dict
        """
        return self._offers

    def rule_discount(self, catalogue, products, **kwargs):
        """
        Get discount for products
        :param products: The products with the offer rule
        :type products: list
        :param kwargs: {discount: 25}
        :type kwargs: dict
        :return: total discount
        :rtype: float
        """
        total = 0
        for product in products:
            total += catalogue.get(product) * (kwargs.get("discount") / 100)
        return total

    def rule_buy_x_get_y_free(self, catalogue, products, **kwargs):
        """
        Get free products' price
        :param products: The products
        :type products: list
        :param kwargs: {buy: 2, free: 1}
        :type kwargs: dict
        :return: total discount
        :rtype: float
        """
        total = 0
        buy = kwargs.get("buy")
        free = kwargs.get("free")

        buy_index = 0
        for i in range(len(products)):
            if buy_index == buy:
                for j in range(i, i + free):
                    product = products[j]
                    total += catalogue.get(product)
                buy_index = 0
            else:
                buy_index += 1

            i += free

        return total
