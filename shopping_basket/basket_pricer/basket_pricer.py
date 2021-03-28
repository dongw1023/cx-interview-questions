class BasketPricer:
    def __init__(self, basket, catalogue, offers):
        self._basket = basket
        self._catalogue = catalogue
        self._offers = offers

    def calculate_sub_total_price(self):
        """
        Total price without any offers
        :return: Total price
        :rtype: float
        """
        sub_total = 0

        for product_name in self._basket:
            sub_total += self._catalogue.get(product_name) * self._basket.get(
                product_name
            )

        return round(sub_total, 2)

    def calculate_discount(self):
        """
        Calculate the discount for the products
        :return:
        :rtype:
        """
        discount = 0
        products_by_offer = self.products_by_offer()

        for offer_name in products_by_offer:
            offer = products_by_offer.get(offer_name).get("offer")
            products = products_by_offer.get(offer_name).get("products")
            rule_func = offer.get("func")
            discount += rule_func(
                products,
                **offer.get("kwargs"),
            )

        return round(discount, 2)

    def is_product_in_basket(self, product):
        """
        Check if the product is in the backet
        :param product: The product
        :type product: dict
        :return: True if it is in the basket
        :rtype: bool
        """
        return product in self._basket

    def products_by_offer(self):
        """
        Group products by offers, for example:
        {
            "25% discount": {
                "offer": offer,
                "products": [product1, ...]
            }
        }
        :return: Products dictionary with offers as key
        :rtype: dict
        """
        products_by_offer = {}

        for product_name in self._offers:
            if not self.is_product_in_basket(product_name):
                continue

            offer = self._offers[product_name]
            product_count = self._basket[product_name]
            product_price = self._catalogue[product_name]

            if offer.get("name") not in products_by_offer:

                products_by_offer[offer.get("name")] = {
                    "offer": offer,
                    "products": [{"name": product_name, "price": product_price}]
                    * product_count,
                }
            else:
                products_by_offer[offer.get("name")]["products"] += [
                    {"name": product_name, "price": product_price}
                ] * product_count

        return products_by_offer

    def output_summary(self, basket=None):
        """
        Output summary information, such as sub-total, discount, total
        :param basket: The basket needs to be calculate
        :type basket: dict
        :return: Summary information
        :rtype: str
        """

        sub_total, discount, total = self.summary(basket)

        return f"sub-total: £{sub_total}\ndiscount: £{discount}\ntotal: £{total}"

    def summary(self, basket=None):
        """
        Get sub-total, discount, total for the basket
        :param basket: The basket which will be calculated
        :type basket: dict
        :return: sub_total, discount, total
        :rtype: tuple
        """
        if basket:
            self._basket = basket
        sub_total = self.calculate_sub_total_price()
        discount = self.calculate_discount()
        total = sub_total - discount

        if total < 0:
            raise ValueError("The total should not be a negative value!")

        return sub_total, discount, total
