# coding: utf-8
from flask import render_template, Blueprint, redirect, flash, session, current_app
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
        if user_form.username.data != user.username:
            user_others = User.query.filter(
                User.username == user_form.username.data).first()
            if user_others:
                flash('该用户名已存在')
                return redirect(url_for('.user', user_id=current_user.id))
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


@main.route('/products/result/<product_ids>/')
def result(product_ids):
    '''
    搜索结果
    '''
    product_ids = json.loads(product_ids)
    products = Product.query.filter(Product.id.in_(
        product_ids)).all() if product_ids else []
    return render_template('searchresults.html', products=products)


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
