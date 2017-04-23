# coding: utf-8
import datetime
from flask import session
import time


def get_time_bucket():
    """返回上午/下午/晚上"""
    now = datetime.datetime.now()
    hour = int(now.strftime('%H'))
    if hour >= 6 and hour < 12:
        return u'上午'
    elif hour >= 12 and hour < 19:
        return u'下午'
    else:
        return u'晚上'

def get_products_in_cart(color_key_list):
    """返回在购物车中的商品"""
    from ..models import Color
    products_in_cart = {}
    for key in color_key_list:
        color_id = key.split('_')[-1]
        color = Color.query.get(int(color_id))
        products_in_cart[key] = {"amount": session.get(key).get("amount"), "img_url": color.img_url, "name": color.product.name,
                              "color_name": color.name, "price": color.product.price, "timestamp": session.get(key).get("timestamp")}
    return products_in_cart

def timestamp_to_datetime(timestamp):
    """时间戳 -> 时间字符串
    1461233180 -> '2016-06-06'
    """
    tmp_struct_time = time.localtime(timestamp)
    datetime_str = time.strftime('%Y-%m-%d', tmp_struct_time)
    return datetime_str

if __name__ == '__main__':
    print(get_time_bucket())
    # print(timestamp_to_datetime(int(time.time())))
