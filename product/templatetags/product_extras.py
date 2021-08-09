from django import template

register = template.Library()


# def final_price(product):
#     if product.discount.percent:
#         dis = round((product.discount.percent * product.price) / 100)
#         if dis > product.discount.max_discount:
#             return product.price - 50
#         return product.price - dis
#     elif product.discount.amount:
#         return product.price - product.discount.amount


def round_score(score):
    return range(round(score))


def _score(score):
    return range(5 - round(score))


# register.filter('final_price', final_price)
register.filter('round', round_score)
register.filter('round2', _score)
