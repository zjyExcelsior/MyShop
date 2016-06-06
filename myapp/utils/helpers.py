# coding: utf-8
import datetime
from flask import session
from ..models import Color


def get_time():
    '''返回上午/下午/晚上'''
    now = datetime.datetime.now()
    hour = int(now.strftime('%H'))
    if hour >= 6 and hour < 12:
        return u'上午'
    elif hour >= 12 and hour < 19:
        return u'下午'
    else:
        return u'晚上'

def get_products_in_cart(color_key_list):
    '''返回在购物车中的商品'''
    products_in_cart = {}
    for key in color_key_list:
        color_id = key.split('_')[-1]
        color = Color.query.get(int(color_id))
        products_in_cart[key] = {"amount": session.get(key).get("amount"), "img_url": color.img_url, "name": color.product.name,
                              "color_name": color.name, "price": color.product.price, "timestamp": session.get(key).get("timestamp")}
    return products_in_cart


if __name__ == '__main__':
    print get_time()
