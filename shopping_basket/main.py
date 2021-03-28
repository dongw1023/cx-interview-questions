import json
from basket_pricer.speical_offers import SpecialOffers
from basket_pricer.basket_pricer import BasketPricer


if __name__ == "__main__":
    with open("basket_pricer/data/catalogue.json") as f:
        catalogue = json.loads(f.read())
    with open("basket_pricer/data/special_offers.json") as f:
        special_offers = json.loads(f.read())

    so = SpecialOffers()
    for product in special_offers:
        special_offers[product]["func"] = so.get_rule_func(
            special_offers.get(product).get("rule")
        )

    with open("basket_pricer/data/basket.json") as f:
        basket = json.loads(f.read())

    basket_pricer = BasketPricer(basket, catalogue, special_offers)
    print(basket_pricer.output_summary())
