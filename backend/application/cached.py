#from main import cache
from .models import Product,Category,User
from flask import current_app as app
from flask_caching import Cache
cache = Cache(app,config={'CACHE_TYPE': 'redis'})
@cache.memoize(5)
def get_product():
    product = Product.query.all()
    return product

@cache.memoize(5)
def get_category():
    category = Category.query.all()
    return category

@cache.memoize(5)
def get_managers():
    manager = User.query.filter_by(role='Manager')
    return manager