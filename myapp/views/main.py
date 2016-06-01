# coding: utf-8
from flask import render_template, Blueprint, redirect, flash, session
from flask_login import login_required
from flask import url_for
from ..forms import UserInfoForm
from ..models import User, Role, Product, Color
from .. import db
from ..utils.helpers import get_time

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
    user_form = UserInfoForm()
    if user_form.validate_on_submit():
        user = User.query.filter(User.id == user_id).first()
        if user_form.username.data:
            user.username = user_form.username.data
            user_form.username.data = ''
        if user_form.password.data:
            user.password = user_form.password.data
            user_form.password.data = ''
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.user', user_id=user_id))
    if user_form.username.errors:
        flash(user_form.username.errors[0])
    elif user_form.password.errors:
        flash(user_form.password.errors[0])
    time_now = get_time()
    return render_template('user.html', user_form=user_form, time_now=time_now)


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
    products_others = [product for product in products if product.id != product_id]
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
