import json
from shopping_basket.basket_pricer.speical_offers import SpecialOffers


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

        return sub_total

    def calculate_discount(self):
        discount = 0
        products_by_offer = self.products_by_offer()

        for offer_name in products_by_offer:
            offer = products_by_offer.get(offer_name).get("offer")
            products = products_by_offer.get(offer_name).get("products")
            rule_func = offer.get("func")
            discount += rule_func(
                self._catalogue,
                products,
                **offer.get("kwargs"),
            )

        return discount

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

            if offer.get("name") not in products_by_offer:

                products_by_offer[offer.get("name")] = {
                    "offer": offer,
                    "products": [product_name] * product_count,
                }
            else:
                products_by_offer[offer.get("name")]["products"] += [
                    product_name
                ] * product_count

        return products_by_offer


if __name__ == "__main__":
    with open("data/basket_2.json") as f:
        basket = json.loads(f.read())
    with open("data/catalogue.json") as f:
        catalogue = json.loads(f.read())
    with open("data/special_offers.json") as f:
        special_offers = json.loads(f.read())

    for product in special_offers:
        so = SpecialOffers()
        special_offers[product]["func"] = so.get_rule_func(
            special_offers.get(product).get("rule")
        )

    basket_pricer = BasketPricer(basket, catalogue, special_offers)
    sub_total = basket_pricer.calculate_sub_total_price()
    discount = basket_pricer.calculate_discount()
    total = sub_total - discount

    print(
        f"""
    sub - total: £{sub_total}
    discount: £{discount}
    total: £{total}
    """
    )
