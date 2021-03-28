class SpecialOffers:
    def __init__(self):

        self._default_rules = ["buy $buy get $free free", "$discount% discount"]
        self._rules_func = {
            "buy $buy get $free free": self.rule_buy_x_get_y_free,
            "$discount% discount": self.rule_discount,
        }

    def get_rule_func(self, rule_template):
        """
        Get the funcution to calculate the offer
        :param rule_template: The rule template
        :type rule_template:  str
        :return: The function
        :rtype: func
        """
        if rule_template not in self._rules_func:
            raise NotImplementedError(
                f"The rule template {rule_template} is not implemented!"
            )
        return self._rules_func.get(rule_template)

    def rule_discount(self, products, **kwargs):
        """
        Get discount for products
        :param products: The products
        :type products: list
        :param kwargs: {discount: 25}
        :type kwargs: dict
        :return: total discount
        :rtype: float
        """
        total = 0
        for product in products:
            total += product.get("price") * (kwargs.get("discount") / 100)
        return total

    def rule_buy_x_get_y_free(self, products, **kwargs):
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
                    total += product.get("price")
                buy_index = 0
            else:
                buy_index += 1

            i += free

        return total
