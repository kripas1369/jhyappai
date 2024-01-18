import datetime
from itertools import product
from math import prod
from django import template

from ecomapp.models import Product, Reviews
register = template.Library()


@register.simple_tag
def rating_number(product_id, rating):
    product = Product.objects.get(id=product_id)
    if rating == 1:
        ratings = Reviews.objects.filter(product=product, rate=1)
        return len(ratings)
    elif rating == 2:
        ratings = Reviews.objects.filter(product=product, rate=2)
        return len(ratings)
    elif rating == 3:
        ratings = Reviews.objects.filter(product=product, rate=3)
        return len(ratings)
    elif rating == 4:
        ratings = Reviews.objects.filter(product=product, rate=4)
        return len(ratings)
    elif rating == 5:
        ratings = Reviews.objects.filter(product=product, rate=5)
        return len(ratings)
