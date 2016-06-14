# coding: utf-8
from flask import render_template, Blueprint, redirect, flash, session
from flask_login import login_required, current_user
from flask import url_for, jsonify, request
from ..forms import UserInfoForm, AddressForm
from ..models import User, Role, Product, Color, Address, Order, OrderColor
from .. import db
from ..utils.helpers import get_time, get_products_in_cart
from sqlalchemy import desc
import json
import time

main = Blueprint('main', __name__)


@main.route('/')
def index():
    products_hot = Product.query.order_by(Product.id).limit(3)
    return render_template('index.html', products_hot=products_hot)


@main.route('/user/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def user(user_id):
    '''
    用户个人页
    '''
    time_now = get_time()
    user_form = UserInfoForm()
    address_form = AddressForm()
    if address_form.validate_on_submit():
        if not address_form.address_id.data:
            address = Address(name=address_form.name.data, phone_number=address_form.phone_number.data,
                              province=address_form.province.data, city=address_form.city.data,
                              region=address_form.region.data, detail_address=address_form.detail_address.data,
                              postcode=address_form.postcode.data, user_id=current_user.id)
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
        return redirect(url_for('.user', user_id=current_user.id))
    if user_form.validate_on_submit():
        user = User.query.get(current_user.id)
        user_others = User.query.filter(User.username == user_form.username.data).first()
        if user_others:
            flash('该用户名已存在');
            return redirect(url_for('.user', user_id=current_user.id))
        if user_form.username.data != user.username:
            user.username = user_form.username.data
        if user_form.password.data:
            user.password = user_form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.user', user_id=current_user.id))
    if user_form.username.errors:
        flash(user_form.username.errors[0])
    elif user_form.password.errors:
        flash(user_form.password.errors[0])
    # 修改个人信息的时候，将当前用户名显示在表单中
    user_form.username.data = current_user.username
    addresses = current_user.addresses.order_by(desc(Address.id)).all()
    orders = current_user.orders.order_by(desc(Order.id)).all()
    return render_template('user.html', user_form=user_form, address_form=address_form, time_now=time_now, addresses=addresses, orders=orders)


@main.route('/goodslist/')
def goodslist():
    '''
    所有商品
    '''
    products = Product.query.all()
    return render_template('goodsList.html', products=products)


@main.route('/goods/<int:product_id>/', methods=['GET', 'POST'])
def goods(product_id):
    '''
    商品详情
    '''
    product_detail = Product.query.get(product_id)
    products = Product.query.all()
    products_others = [
        product for product in products if product.id != product_id]
    return render_template('goods.html', product_detail=product_detail, products_others=products_others)


@main.route('/cart/')
@main.route('/cart/<user_id>/')
def cart(user_id=0):
    '''
    购物车
    '''
    color_keys = [key for key in session.keys() if 'color' in key]
    products_in_cart = get_products_in_cart(color_keys)
    return render_template('cart.html', products=products_in_cart)


@main.route('/orderconfirm/<user_id>', methods=['GET', 'POST'])
def orderconfirm(user_id):
    '''
    确认订单
    '''
    if 'color_keys' in request.args:
        color_keys = json.loads(request.args.get('color_keys'))
        products_selected = get_products_in_cart(color_keys)
        session['products_selected'] = products_selected
    address_form = AddressForm()
    if address_form.validate_on_submit():
        if not address_form.address_id.data:
            address = Address(name=address_form.name.data, phone_number=address_form.phone_number.data,
                              province=address_form.province.data, city=address_form.city.data,
                              region=address_form.region.data, detail_address=address_form.detail_address.data,
                              postcode=address_form.postcode.data, user_id=current_user.id)
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
        return redirect(url_for('.orderconfirm', user_id=current_user.id, products=session.get('products_selected', {})))
    addresses = current_user.addresses.order_by(desc(Address.id)).all()
    return render_template('orderConfirm.html', addresses=addresses, address_form=address_form, products=session.get('products_selected', {}))


@main.route('/payconfirm/', methods=['GET', 'POST'])
def payconfirm():
    '''
    确认支付
    '''
    return render_template('payConfirm.html')


@main.route('/paysuccess/')
def paysuccess():
    '''
    支付成功
    '''
    return render_template('paySuccess.html')


@main.route('/address_info/<int:address_id>/')
def address_info(address_id):
    '''得到地址信息'''
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


@main.route('/remove_address/', methods=['POST'])
def remove_address():
    '''删除地址信息'''
    address_id = json.loads(request.data).get('address_id')
    address = Address.query.get(int(address_id))
    db.session.delete(address)
    db.session.commit()
    return 'remove address success'


@main.route('/add_products/')
def add_products():
    # 无印良品风U型抱枕
    product_baozhen = Product(
        name='无印良品风U型抱枕', description='懒人抱枕 办公室必备', price='67.70', detail='材质：外部（针织棉100%），内部套（95%聚酯纤维，5%氨纶）\n颜色：黑灰、深灰白、浅灰白、粉灰\n粒子：0.5mm级别进口粒子（无味无声触感细腻）\n扣子：日本NIFCO卡扣')
    color_baozhen1 = Color(name="深灰白", color="#dddce4", img_url=url_for(
        'static', filename='image/goods/baozhen#dddce4.png'), amount=1, product=product_baozhen)
    color_baozhen2 = Color(name="粉灰", color="#f6e4e4", img_url=url_for(
        'static', filename='image/goods/baozhen#f6e4e4.png'), amount=2, product=product_baozhen)
    color_baozhen3 = Color(name="浅灰白", color="#eeeef4", img_url=url_for(
        'static', filename='image/goods/baozhen#eeeef4.png'), amount=3, product=product_baozhen)
    color_baozhen4 = Color(name="黑灰", color="#e1e1e1", img_url=url_for(
        'static', filename='image/goods/baozhen#e1e1e1.png'), amount=4, product=product_baozhen)
    # 黑猫Tiimo美臀坐垫
    product_zuodian = Product(
        name='黑猫Tiimo美臀坐垫', description='柔软治愈 美臀不再费力', price='52.25', detail='尺寸：42cm＊42cm\n规格：单件\n材质：毛绒面料，填充（珍珠棉）\n特点：柔软治愈，表面细腻，手感软滑透气，不掉毛，还有美臀功效；长时间不会变形')
    color_zuodian1 = Color(name="木炭黑", color="#1e353f", img_url=url_for(
        'static', filename='image/goods/zuodian#1e353f.png'), amount=1, product=product_zuodian)
    # 日式原木木片篮子圆形面包篮
    product_mbl = Product(name='日式原木木片篮子圆形面包篮',
                          description='原木木片 自然生态', price='16.00', detail='尺寸：19.5cm＊8cm\n材质：天然杉木\n产品贴士：本产品为手工编织，细节处难免不完美，材质原因可能造成表面及边缘有毛刺，介意请慎拍')
    color_mbl1 = Color(name="本木色", color="#c1925b", img_url=url_for(
        'static', filename='image/goods/mbl#c1925b.png'), amount=1, product=product_mbl)
    # 日式单耳陶瓷碗
    product_wan = Product(
        name='日式单耳陶瓷碗', description='亚光磨砂釉面 质感温润', price='26.00', detail='尺寸：13cm＊6cm\n规格：单件\n材质：陶瓷\n工艺：亚光色釉\n特点：简单的经典色，表面的磨砂质感，手感和质感温润')
    color_wan1 = Color(name="黑色", color="#35343a", img_url=url_for(
        'static', filename='image/goods/wan#35343a.png'), amount=1, product=product_wan)
    color_wan2 = Color(name="白色", color="#f5f6f6", img_url=url_for(
        'static', filename='image/goods/wan#f5f6f6.png'), amount=1, product=product_wan)
    # 超声波负离子香薰机
    product_xxj = Product(
        name='超声波负离子香薰机', description='润物无声 品质保障', price='195.00', detail='尺寸：16.8cm＊13cm\n规格：单件\n材质：防腐PP材料\n特点：采用超声波雾化技术，细腻雾化；自然芳香，保湿空气，还可以做小夜灯\n产品贴士：切勿加入水温高于40℃的水；机器每使用3～5次，建议清洗；长时间不使用请切断电源并清洁后存放；再次使用可能有雾气变小的现象，可先将水槽清洗后再用')
    color_xxj1 = Color(name="白色", color="#f5f6f6", img_url=url_for(
        'static', filename='image/goods/xxj#f5f6f6.png'), amount=1, product=product_xxj)
    # 组合式木质盖子收纳盒
    product_snh = Product(
        name='组合式木质盖子收纳盒', description='原木木片 自然生态', price='38.00', detail='尺寸：25.5cm＊10cm\n规格：单件\n材质：橡胶木/PP塑料\n特点：清新淡雅，质感好，便利整洁；收纳日常杂物，既美观又实用')
    color_snh1 = Color(name="本白色", color="#ffdbb7", img_url=url_for(
        'static', filename='image/goods/snh#ffdbb7.png'), amount=1, product=product_snh)
    # 创意木质手工皂盒
    product_zaohe = Product(
        name='创意木质手工皂盒', description='木质本色 朴实自然', price='9.90', detail='尺寸：10cm＊10cm\n规格：单件\n材质：木\n特点：木制本色，外层刷透明光漆，朴实自然，底部有漏水孔')
    color_zaohe1 = Color(name="本木色", color="#eac090", img_url=url_for(
        'static', filename='image/goods/zaohe#eac090.png'), amount=1, product=product_zaohe)
    # 手工编制藤编收纳筐
    product_snk = Product(
        name='手工编制藤编收纳筐', description='田园风情 匠人之心', price='32.00', detail='尺寸：25.5cm＊10cm\n规格：单件\n材质：橡胶木/PP塑料\n特点：清新淡雅，质感好，便利整洁；收纳日常杂物，既美观又实用')
    color_snk1 = Color(name="藤木色", color="#957454", img_url=url_for(
        'static', filename='image/goods/snk#957454.png'), amount=1, product=product_snk)
    # 创意实木小勺子
    product_shaozi = Product(
        name='创意实木小勺子', description='精致可爱 安全健康', price='4.80', detail='尺寸：13.5cm＊2.5cm\n规格：单件\n材质：楠木/杉木\n特点：精致可爱的日系方形小勺，原木材质安全健康；多色可选，满足不同使用需求\n产品贴士：本产品为木质，抹油保养可延长宝贝使用寿命，建议定期涂抹食用油保养')
    color_shaozi1 = Color(name="楠木黑色线", color="#5d2a18", img_url=url_for(
        'static', filename='image/goods/shaozi#5d2a18.png'), amount=1, product=product_shaozi)
    color_shaozi2 = Color(name="楠木卡其色线", color="#69301c", img_url=url_for(
        'static', filename='image/goods/shaozi#69301c.png'), amount=1, product=product_shaozi)
    color_shaozi3 = Color(name="杉木卡其色线", color="#ecd1b4", img_url=url_for(
        'static', filename='image/goods/shaozi#ecd1b4.png'), amount=1, product=product_shaozi)
    color_shaozi4 = Color(name="杉木黑色线", color="#edd3b7", img_url=url_for(
        'static', filename='image/goods/shaozi#edd3b7.png'), amount=1, product=product_shaozi)
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


@main.route('/modify_order_state/', methods=['POST'])
def modify_order_state():
    '''修改订单状态'''
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


@main.route('/cancel_order/', methods=['POST'])
def cancel_order():
    '''关闭订单'''
    order_id = request.data
    order = Order.query.get(order_id)
    order.state = u'已关闭'
    db.session.add(order)
    db.session.commit()
    return 'cancel order success'


@main.route('/add_to_cart/', methods=['POST'])
def add_to_cart():
    '''添加商品到购物车'''
    color_id = json.loads(request.data).get('color_id')
    color = Color.query.get(int(color_id))
    color_key = 'color_%s' % color.id
    if color_key in session:
        session[color_key]['amount'] += 1
    else:
        session[color_key] = {'amount': 1, 'timestamp': int(time.time())}
        if 'product_amount' not in session:
            session['product_amount'] = 1
        else:
            session['product_amount'] += 1
    return 'add products to cart successfully.'


@main.route('/remove_from_cart/', methods=['POST'])
def remove_from_cart():
    '''将商品从购物车中移除'''
    color_key = request.data
    session.pop(color_key, None)
    if session['product_amount'] != 0:
        session['product_amount'] -= 1
    return 'remove success'


@main.route('/add_orders/', methods=['POST'])
def add_orders():
    '''添加新订单'''
    results = json.loads(request.data)
    order_new = Order(order_time=int(time.time()), total=results.get(
        'total'), state='等待支付', user_id=current_user.id, address_id=results.get('address_id'))
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
    # 把order的id加入session中
    session['order_id'] = order_new.id
    db.session.commit()
    return 'add new orders success'


@main.route('/test_remove_user/')
def test_remove_user():
    user = User.query.get(3)
    db.session.delete(user)
    db.session.commit()
    return 'yes'


@main.route('/teststatic/')
def teststatic():
    return url_for('static', filename='image/logo.png')


@main.route('/testsql/')
def testsql():
    role = Role.query.filter(Role.id == 1).first()
    if role:
        db.session.delete(role)
        db.session.commit()
        return 'success'
    return 'there is no role'
