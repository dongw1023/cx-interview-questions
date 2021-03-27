class CatalogueException(Exception):
    """
    Catalogue exception
    """

    pass


class ProductNotValidException(CatalogueException):
    """
    Product not valid exception
    """

    pass


class ProductNotFoundException(CatalogueException):
    """
    Product not found in current catalogue
    """

    pass


class ProductAlreadyExistException(CatalogueException):
    """
    Product not exist in current catalogue
    """

    pass
