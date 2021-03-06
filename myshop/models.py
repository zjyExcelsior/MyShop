# coding: utf-8
import hashlib
from .ext import db, login_manager, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from .utils.helpers import timestamp_to_datetime


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role id=%s, name=%s>' % (self.id, self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref=db.backref('users',
                                                      cascade='all, delete-orphan'))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, _password):
        self.password_hash = hashlib.md5(_password).hexdigest()

    def verify_password(self, password):
        return self.password_hash == hashlib.md5(password).hexdigest()

    def __repr__(self):
        return '<User id=%s, username=%s>' % (self.id, self.username)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone_number = db.Column(db.String(11))
    province = db.Column(db.String(64))
    city = db.Column(db.String(64))
    region = db.Column(db.String(64))
    detail_address = db.Column(db.String(128))
    postcode = db.Column(db.String(6))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('addresses',
                                                      cascade='all, delete-orphan',
                                                      lazy='dynamic'))

    def __init__(self, name, phone_number, province, city, region, detail_address, postcode, user_id):
        self.name = name
        self.phone_number = phone_number
        self.province = province
        self.city = city
        self.region = region
        self.detail_address = detail_address
        self.postcode = postcode
        self.user_id = user_id

    def __repr__(self):
        return '<Address id=%s, name=%s>' % (self.id, self.name)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    price = db.Column(db.String(8))
    detail = db.Column(db.Text)

    def __init__(self, name, description, price, detail):
        self.name = name
        self.description = description
        self.price = price
        self.detail = detail

    @property
    def detail_lines(self):
        return self.detail.splitlines()

    def __repr__(self):
        return '<Product id=%s, name=%s>' % (self.id, self.name)


class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    color = db.Column(db.String(10))
    img_url = db.Column(db.String(128))
    amount = db.Column(db.Integer, default=0)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product', backref=db.backref('colors',
                                                            cascade='all, delete-orphan'))

    def __init__(self, name, color, img_url, amount, product):
        self.name = name
        self.color = color
        self.img_url = img_url
        self.amount = amount
        self.product = product

    def __repr__(self):
        return '<Color id=%s, product_id=%s, color=%s>' % (self.id, self.product_id, self.color)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(64))
    order_time = db.Column(db.Integer)
    total = db.Column(db.String(10))
    state = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
    user = db.relationship('User', backref=db.backref('orders',
                                                      cascade='all, delete-orphan',
                                                      lazy='dynamic'))
    addresses = db.relationship('Address',
                                backref=db.backref('orders'))  # 当地址不存在的时候，不删除该订单

    def __init__(self, order_time, total, state, user_id, address_id):
        self.order_time = order_time
        self.total = total
        self.state = state
        self.user_id = user_id
        self.address_id = address_id

    @property
    def order_date(self):
        return timestamp_to_datetime(self.order_time)

    def __repr__(self):
        return '<Order id=%s, order_number=%s>' % (self.id, self.order_number)


class OrderColor(db.Model):
    __tablename__ = 'orders_colors'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'),
                         primary_key=True)
    color_id = db.Column(db.Integer, db.ForeignKey('colors.id'),
                         primary_key=True)
    amount = db.Column(db.Integer)
    order = db.relationship('Order', backref=db.backref('colors',
                                                        cascade='all, delete-orphan'))
    color = db.relationship('Color', backref=db.backref('orders',
                                                        cascade='all, delete-orphan'))

    def __repr__(self):
        return '<OrderColor order_id=%s, color_id=%s, amount=%s>' % (self.order_id, self.color_id, self.amount)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Color, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(OrderColor, db.session))
