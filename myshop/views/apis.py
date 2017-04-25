# coding: utf-8
import json
import time
from flask import Blueprint, redirect, session, url_for, jsonify, request
from flask_login import login_required, current_user
from ..models import Product, Color, Address, Order, OrderColor
from ..forms import AddressForm
from ..ext import db

apis = Blueprint('apis', __name__)


@apis.route('/search_product/', methods=['POST'])
def search_product():
    """搜索商品"""
    product_name = request.form.get('name', '')
    if product_name:
        like_regex = u'%{0}%'.format(product_name)
        products = Product.query.filter(Product.name.like(like_regex)).all()
        product_ids = [product.id for product in products]
        if products:
            return redirect(url_for('main.result', product_ids=json.dumps(product_ids)))
        else:
            return redirect(request.headers.get('Referer'))
    return redirect(request.headers.get('Referer'))


@apis.route('/address_info/<int:address_id>/')
@login_required
def address_info(address_id):
    """得到地址信息"""
    address = Address.query.get(address_id)
    return jsonify({
        'name': address.name,
        'phone_number': address.phone_number,
        'province': address.province,
        'city': address.city,
        'region': address.region,
        'detail_address': address.detail_address,
        'postcode': address.postcode
    })


@apis.route('/remove_address/', methods=['POST'])
@login_required
def remove_address():
    """删除地址信息"""
    address_id = json.loads(request.data).get('address_id')
    address = Address.query.get(int(address_id))
    db.session.delete(address)
    db.session.commit()
    return 'remove address success'


@apis.route('/add_products/')
@login_required
def add_products():
    # 无印良品风U型抱枕
    product_baozhen = Product('无印良品风U型抱枕', '懒人抱枕 办公室必备', '67.70',
                              '材质：外部（针织棉100%），内部套（95%聚酯纤维，5%氨纶）\n颜色：黑灰、深灰白、浅灰白、粉灰\n粒子：0.5mm级别进口粒子（无味无声触感细腻）\n扣子：日本NIFCO卡扣')
    color_baozhen1 = Color("深灰白", "#dddce4", url_for(
        'static', filename='image/goods/baozhen#dddce4.png'), 1, product_baozhen)
    color_baozhen2 = Color("粉灰", "#f6e4e4", url_for(
        'static', filename='image/goods/baozhen#f6e4e4.png'), 2, product_baozhen)
    color_baozhen3 = Color("浅灰白", "#eeeef4", url_for(
        'static', filename='image/goods/baozhen#eeeef4.png'), 3, product_baozhen)
    color_baozhen4 = Color("黑灰", "#e1e1e1", url_for(
        'static', filename='image/goods/baozhen#e1e1e1.png'), 4, product_baozhen)
    # 黑猫Tiimo美臀坐垫
    product_zuodian = Product('黑猫Tiimo美臀坐垫', '柔软治愈 美臀不再费力', '52.25',
                              '尺寸：42cm＊42cm\n规格：单件\n材质：毛绒面料，填充（珍珠棉）\n特点：柔软治愈，表面细腻，手感软滑透气，不掉毛，还有美臀功效；长时间不会变形')
    color_zuodian1 = Color("木炭黑", "#1e353f", url_for(
        'static', filename='image/goods/zuodian#1e353f.png'), 1, product_zuodian)
    # 日式原木木片篮子圆形面包篮
    product_mbl = Product('日式原木木片篮子圆形面包篮', '原木木片 自然生态', '16.00',
                          '尺寸：19.5cm＊8cm\n材质：天然杉木\n产品贴士：本产品为手工编织，细节处难免不完美，材质原因可能造成表面及边缘有毛刺，介意请慎拍')
    color_mbl1 = Color("本木色", "#c1925b", url_for(
        'static', filename='image/goods/mbl#c1925b.png'), 1, product_mbl)
    # 日式单耳陶瓷碗
    product_wan = Product('日式单耳陶瓷碗', '亚光磨砂釉面 质感温润', '26.00',
                          '尺寸：13cm＊6cm\n规格：单件\n材质：陶瓷\n工艺：亚光色釉\n特点：简单的经典色，表面的磨砂质感，手感和质感温润')
    color_wan1 = Color("黑色", "#35343a", url_for(
        'static', filename='image/goods/wan#35343a.png'), 1, product_wan)
    color_wan2 = Color("白色", "#f5f6f6", url_for(
        'static', filename='image/goods/wan#f5f6f6.png'), 1, product_wan)
    # 超声波负离子香薰机
    product_xxj = Product('超声波负离子香薰机', '润物无声 品质保障', '195.00',
                          '尺寸：16.8cm＊13cm\n规格：单件\n材质：防腐PP材料\n特点：采用超声波雾化技术，细腻雾化；自然芳香，保湿空气，还可以做小夜灯\n产品贴士：切勿加入水温高于40℃的水；机器每使用3～5次，建议清洗；长时间不使用请切断电源并清洁后存放；再次使用可能有雾气变小的现象，可先将水槽清洗后再用')
    color_xxj1 = Color("白色", "#f5f6f6", url_for(
        'static', filename='image/goods/xxj#f5f6f6.png'), 1, product_xxj)
    # 组合式木质盖子收纳盒
    product_snh = Product('组合式木质盖子收纳盒', '原木木片 自然生态', '38.00',
                          '尺寸：25.5cm＊10cm\n规格：单件\n材质：橡胶木/PP塑料\n特点：清新淡雅，质感好，便利整洁；收纳日常杂物，既美观又实用')
    color_snh1 = Color("本白色", "#ffdbb7", url_for(
        'static', filename='image/goods/snh#ffdbb7.png'), 1, product_snh)
    # 创意木质手工皂盒
    product_zaohe = Product('创意木质手工皂盒', '木质本色 朴实自然', '9.90',
                            '尺寸：10cm＊10cm\n规格：单件\n材质：木\n特点：木制本色，外层刷透明光漆，朴实自然，底部有漏水孔')
    color_zaohe1 = Color("本木色", "#eac090", url_for(
        'static', filename='image/goods/zaohe#eac090.png'), 1, product_zaohe)
    # 手工编制藤编收纳筐
    product_snk = Product('手工编制藤编收纳筐', '田园风情 匠人之心', '32.00',
                          '尺寸：25.5cm＊10cm\n规格：单件\n材质：橡胶木/PP塑料\n特点：清新淡雅，质感好，便利整洁；收纳日常杂物，既美观又实用')
    color_snk1 = Color("藤木色", "#957454", url_for(
        'static', filename='image/goods/snk#957454.png'), 1, product_snk)
    # 创意实木小勺子
    product_shaozi = Product('创意实木小勺子', '精致可爱 安全健康', '4.80',
                             '尺寸：13.5cm＊2.5cm\n规格：单件\n材质：楠木/杉木\n特点：精致可爱的日系方形小勺，原木材质安全健康；多色可选，满足不同使用需求\n产品贴士：本产品为木质，抹油保养可延长宝贝使用寿命，建议定期涂抹食用油保养')
    color_shaozi1 = Color("楠木黑色线", "#5d2a18", url_for(
        'static', filename='image/goods/shaozi#5d2a18.png'), 1, product_shaozi)
    color_shaozi2 = Color("楠木卡其色线", "#69301c", url_for(
        'static', filename='image/goods/shaozi#69301c.png'), 1, product_shaozi)
    color_shaozi3 = Color("杉木卡其色线", "#ecd1b4", url_for(
        'static', filename='image/goods/shaozi#ecd1b4.png'), 1, product_shaozi)
    color_shaozi4 = Color("杉木黑色线", "#edd3b7", url_for(
        'static', filename='image/goods/shaozi#edd3b7.png'), 1, product_shaozi)
    # 添加所有商品
    db.session.add_all([product_baozhen, color_baozhen1, color_baozhen2, color_baozhen3, color_baozhen4,
                        product_zuodian, color_zuodian1,
                        product_mbl, color_mbl1,
                        product_wan, color_wan1, color_wan2,
                        product_xxj, color_xxj1,
                        product_snh, color_snh1,
                        product_zaohe, color_zaohe1,
                        product_snk, color_snk1,
                        product_shaozi, color_shaozi1, color_shaozi2, color_shaozi3, color_shaozi4])
    db.session.commit()
    return 'add products success'


@apis.route('/modify_order_state/', methods=['POST'])
@login_required
def modify_order_state():
    """修改订单状态"""
    order_id = session.get(
        'order_id', '') if not request.data else request.data
    if order_id:
        order = Order.query.get(order_id)
        if order.state == u'等待支付':
            order.state = u'已发货'
        elif order.state == u'已发货':
            order.state = u'交易成功'
        if session.get('order_id', ''):
            session.pop('order_id', None)
        db.session.add(order)
        db.session.commit()
    return 'modify the state of order success'


@apis.route('/cancel_order/', methods=['POST'])
@login_required
def cancel_order():
    """关闭订单"""
    order_id = request.data
    order = Order.query.get(order_id)
    order.state = u'已关闭'
    db.session.add(order)
    db.session.commit()
    return 'cancel order success'


@apis.route('/add_to_cart/', methods=['POST'])
def add_to_cart():
    """添加商品到购物车"""
    color_id = json.loads(request.data).get('color_id')
    color = Color.query.get(int(color_id))
    if color.amount > 0:
        color.amount -= 1
    db.session.add(color)
    db.session.commit()
    color_key = 'color_%s' % color.id
    if color_key in session:
        session[color_key]['amount'] += 1
        session[color_key]['timestamp'] = int(time.time())
        session.modified = True
    else:
        session[color_key] = {'amount': 1, 'timestamp': int(time.time())}
        if 'product_amount' not in session:
            session['product_amount'] = 1
        else:
            session['product_amount'] += 1
    return 'add products to cart successfully.'


@apis.route('/remove_from_cart/', methods=['POST'])
def remove_from_cart():
    """将商品从购物车中移除"""
    color_key = request.data
    color_id = color_key.split('_')[-1]
    color = Color.query.get(int(color_id))
    color_amount = session.get(color_key).get('amount', 0)
    color.amount += color_amount
    db.session.add(color)
    db.session.commit()
    session.pop(color_key, None)
    if session['product_amount'] != 0:
        session['product_amount'] -= 1
    return 'remove success'


@apis.route('/add_orders/', methods=['POST'])
@login_required
def add_orders():
    """添加新订单"""
    results = json.loads(request.data)
    order_new = Order(int(time.time()), results.get('total'),
                      '等待支付', current_user.id, results.get('address_id'))
    db.session.add(order_new)
    for color_key, amount in results.get('colors').items():
        color_id = color_key.split('_')[-1]
        color = Color.query.get(color_id)
        order_color = OrderColor(amount=amount)
        order_color.order = order_new
        order_color.color = color
        db.session.add(order_color)
        session.pop(color_key, None)
        if session['product_amount'] != 0:
            session['product_amount'] -= 1
    db.session.flush()
    order_new.order_number = 'order%s' % order_new.id
    session['order_id'] = order_new.id  # 把order的id加入session中
    db.session.commit()
    return 'add new orders success'


@apis.route('/deal_with_addresses/', methods=['POST'])
@login_required
def deal_with_addresses():
    address_form = AddressForm()
    if address_form.validate_on_submit():
        if not address_form.address_id.data:
            address = Address(address_form.name.data, address_form.phone_number.data,
                              address_form.province.data, address_form.city.data,
                              address_form.region.data, address_form.detail_address.data,
                              address_form.postcode.data, current_user.id)
        else:
            address = Address.query.get(int(address_form.address_id.data))
            if address_form.name.data and address_form.name.data != address.name:
                address.name = address_form.name.data
            if address_form.phone_number.data and address_form.phone_number.data != address.phone_number:
                address.phone_number = address_form.phone_number.data
            if address_form.province.data and address_form.province.data != address.province:
                address.province = address_form.province.data
            if address_form.city.data and address_form.city.data != address.city:
                address.city = address_form.city.data
            if address_form.region.data and address_form.region.data != address.region:
                address.region = address_form.region.data
            if address_form.detail_address.data and address_form.detail_address.data != address.detail_address:
                address.detail_address = address_form.detail_address.data
            if address_form.postcode.data and address_form.postcode.data != address.postcode:
                address.postcode = address_form.postcode.data
        db.session.add(address)
        db.session.commit()
        return redirect(request.headers.get('referer'))
