# coding: utf-8
import json
from flask import (render_template, Blueprint, redirect, flash, session,
                   current_app, url_for, jsonify, request)
from flask_login import login_required, current_user
from sqlalchemy import desc
from ..forms import UserInfoForm, AddressForm
from ..models import User, Role, Product, Color, Address, Order, OrderColor
from ..ext import db
from ..utils.helpers import get_time_bucket, get_products_in_cart

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
    time_now = get_time_bucket()
    user_form = UserInfoForm()
    address_form = AddressForm()
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
@login_required
def orderconfirm(user_id):
    '''
    确认订单
    '''
    if 'color_keys' in request.args:
        color_keys = json.loads(request.args.get('color_keys'))
        products_selected = get_products_in_cart(color_keys)
        session['products_selected'] = products_selected
    address_form = AddressForm()
    addresses = current_user.addresses.order_by(desc(Address.id)).all()
    return render_template('orderConfirm.html', addresses=addresses, address_form=address_form, products=session.get('products_selected', {}))


@main.route('/payconfirm/', methods=['GET', 'POST'])
@login_required
def payconfirm():
    '''
    确认支付
    '''
    return render_template('payConfirm.html')


@main.route('/paysuccess/')
@login_required
def paysuccess():
    '''
    支付成功
    '''
    return render_template('paySuccess.html')
