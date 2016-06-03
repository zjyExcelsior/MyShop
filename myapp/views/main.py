# coding: utf-8
from flask import render_template, Blueprint, redirect, flash, session
from flask_login import login_required, current_user
from flask import url_for, jsonify, request
from ..forms import UserInfoForm, AddressForm
from ..models import User, Role, Product, Color, Address
from .. import db
from ..utils.helpers import get_time
from sqlalchemy import desc
import json

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
    if request.method == 'POST' and 'address_id' in request.data:
        address_id = json.loads(request.data).get('address_id')
        address = Address.query.get(int(address_id))
        db.session.delete(address)
        db.session.commit()
        return redirect(url_for('.user', user_id=current_user.id))
    user_form.username.data = current_user.username
    addresses = current_user.addresses.order_by(desc(Address.id)).all()
    return render_template('user.html', user_form=user_form, address_form=address_form, time_now=time_now, addresses=addresses)


@main.route('/goodslist/')
def goodslist():
    '''
    所有商品
    '''
    products = Product.query.all()
    return render_template('goodsList.html', products=products)


@main.route('/goods/<int:product_id>/')
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
    return render_template('cart.html')


@main.route('/orderconfirm/')
def orderconfirm():
    '''
    确认订单
    '''
    return render_template('orderConfirm.html')


@main.route('/payconfirm/')
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


@main.route('/address_info/<int:address_id>/')
def address_info(address_id):
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


@main.route('/add_products/')
def add_products():
    # 无印良品风U型抱枕
    product_baozhen = Product(
        name='无印良品风U型抱枕', description='懒人抱枕 办公室必备', price='67.70', detail='哈哈哈')
    color_baozhen1 = Color(color="#dddce4", img_url=url_for(
        'static', filename='image/goods/m1.png'), amount=1, product=product_baozhen)
    color_baozhen2 = Color(color="#f6e4e4", img_url=url_for(
        'static', filename='image/goods/m2.png'), amount=2, product=product_baozhen)
    color_baozhen3 = Color(color="#eeeef4", img_url=url_for(
        'static', filename='image/goods/m3.png'), amount=3, product=product_baozhen)
    color_baozhen4 = Color(color="#e1e1e1", img_url=url_for(
        'static', filename='image/goods/m4.png'), amount=4, product=product_baozhen)
    # 黑猫Tiimo美臀坐垫
    product_zuodian = Product(
        name='黑猫Tiimo美臀坐垫', description='柔软治愈 美臀不再费力', price='52.25', detail='哈哈哈')
    color_zuodian1 = Color(color="#1e353f", img_url=url_for(
        'static', filename='image/goods/m4.png'), amount=1, product=product_zuodian)
    # 日式原木木片篮子圆形面包篮
    product_mbl = Product(name='日式原木木片篮子圆形面包篮',
                          description='原木木片 自然生态', price='16.00', detail='哈哈哈')
    color_mbl1 = Color(color="#c1925b", img_url=url_for(
        'static', filename='image/goods/m5.png'), amount=1, product=product_mbl)
    # 日式单耳陶瓷碗
    product_wan = Product(
        name='日式单耳陶瓷碗', description='亚光磨砂釉面 质感温润', price='26.00', detail='哈哈哈')
    color_wan1 = Color(color="#c1925b", img_url=url_for(
        'static', filename='image/goods/m2.png'), amount=1, product=product_wan)
    color_wan2 = Color(color="#f5f6f6", img_url=url_for(
        'static', filename='image/goods/m2.png'), amount=1, product=product_wan)
    # 超声波负离子香薰机
    product_xxj = Product(
        name='超声波负离子香薰机', description='润物无声 品质保障', price='195.00', detail='哈哈哈')
    color_xxj1 = Color(color="#f5f6f6", img_url=url_for(
        'static', filename='image/goods/m6.png'), amount=1, product=product_xxj)
    # 组合式木质盖子收纳盒
    product_snh = Product(
        name='组合式木质盖子收纳盒', description='原木木片 自然生态', price='38.00', detail='哈哈哈')
    color_snh1 = Color(color="#ffdbb7", img_url=url_for(
        'static', filename='image/goods/m7.png'), amount=1, product=product_snh)
    # 创意木质手工皂盒
    product_zaohe = Product(
        name='创意木质手工皂盒', description='木质本色 朴实自然', price='9.90', detail='哈哈哈')
    color_zaohe1 = Color(color="#eac090", img_url=url_for(
        'static', filename='image/goods/m3.png'), amount=1, product=product_zaohe)
    # 手工编制藤编收纳筐
    product_snk = Product(
        name='手工编制藤编收纳筐', description='田园风情 匠人之心', price='32.00', detail='哈哈哈')
    color_snk1 = Color(color="#957454", img_url=url_for(
        'static', filename='image/goods/m8.png'), amount=1, product=product_snk)
    # 创意实木小勺子
    product_shaozi = Product(
        name='创意实木小勺子', description='精致可爱 安全健康', price='4.80', detail='哈哈哈')
    color_shaozi1 = Color(color="#5d2a18", img_url=url_for(
        'static', filename='image/goods/m9.png'), amount=1, product=product_shaozi)
    color_shaozi2 = Color(color="#ecd1b4", img_url=url_for(
        'static', filename='image/goods/m9.png'), amount=1, product=product_shaozi)
    color_shaozi3 = Color(color="#5d2a18", img_url=url_for(
        'static', filename='image/goods/m9.png'), amount=1, product=product_shaozi)
    color_shaozi4 = Color(color="#ecd1b4", img_url=url_for(
        'static', filename='image/goods/m9.png'), amount=1, product=product_shaozi)
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
