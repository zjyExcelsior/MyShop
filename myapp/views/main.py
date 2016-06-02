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
            address = Address.query.filter(Address.id == address_form.address_id.data).first()
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
        user = User.query.filter(User.id == current_user.id).first()
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
def cart():
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
    address = Address.query.filter(Address.id == address_id).first()
    return jsonify({
        'name': address.name,
        'phone_number': address.phone_number,
        'province': address.province,
        'city': address.city,
        'region': address.region,
        'detail_address': address.detail_address,
        'postcode': address.postcode
    })
