from functions.validation import Validation
from utils.response_utils import ResponseUtils
from database.product_dao import ProductDao


class ProductController(object):

    #---------------------------------------------------------------------------
    # Get Products
    #---------------------------------------------------------------------------
    def getProducts(self, token):
        user, exception = Validation.validateToken(token)
        if (exception != None):
            return ResponseUtils.returnError(exception)

        # TODO: add pagination
        productDao = ProductDao()
        products, exception = productDao.getProducts(user)
        if (exception != None):
            return ResponseUtils.returnError(exception)
        else:
            return ResponseUtils.returnSuccess(products)

    #---------------------------------------------------------------------------
    # Update product with new quantity and price
    #---------------------------------------------------------------------------
    def updateProductQuantityAndOriginalPrice(self, token, products):
        user, exception = Validation.validateToken(token)
        if (exception != None):
            return ResponseUtils.returnError(exception)

        productDao = ProductDao()
        for product in products:
            exception = productDao.updateQuantityAndOrginalPrice(user, product['id'],
                            product['quantity'], product['original_price'])
            if (exception != None):
                return ResponseUtils.returnError(exception)

        return ResponseUtils.returnSuccess(None)

    #---------------------------------------------------------------------------
    # Search Product by name, seller sku, shop sku, brand and model
    #---------------------------------------------------------------------------
    def searchProduct(self, token, searchKey):
        user, exception = Validation.validateToken(token)
        if (exception != None):
            return ResponseUtils.returnError(exception)

        productDao = ProductDao()
        result, exception = productDao.searchProduct(user, searchKey)
        if exception != None:
            return ResponseUtils.returnError(exception)
        else:
            return ResponseUtils.returnSuccess(result)

    #---------------------------------------------------------------------------
    # Get top selling products
    #---------------------------------------------------------------------------
    def getTopSellingProducts(self, token):
        user, exception = Validation.validateToken(token)
        if (exception != None):
            return ResponseUtils.returnError(exception)

        productDao = ProductDao()
        result, exception = productDao.getTopSellingProducts(user)
        if exception != None:
            return ResponseUtils.returnError(exception)
        else:
            return ResponseUtils.returnSuccess(result)








