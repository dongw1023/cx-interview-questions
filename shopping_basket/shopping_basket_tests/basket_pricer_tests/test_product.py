from shopping_basket.basket_pricer.product import Product


class TestProduct:
    def test_product(self):
        product = Product("product_1", 1.99)
        assert product.name == "product_1"
        assert product.price == 1.99
