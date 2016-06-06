# coding: utf-8
from . import db
from flask_login import UserMixin
from . import login_manager
from . import admin
from flask_admin.contrib.sqla import ModelView
import hashlib
import json


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<Role id=%s, name=%s>' % (self.id, self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref=db.backref('users',
                                                      cascade='all, delete-orphan'))

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
                                                      cascade='all, delete-orphan', lazy='dynamic'))

    def __repr__(self):
        return '<Address id=%s, name=%s>' % (self.id, self.name)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    price = db.Column(db.String(8))
    detail = db.Column(db.Text)

    def __repr__(self):
        return '<Product id=%s, name=%s>' % (self.id, self.name)


class Color(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    name = db.Column(db.String(64))
    color = db.Column(db.String(10))
    img_url = db.Column(db.String(128))
    amount = db.Column(db.Integer, default=0)
    product = db.relationship('Product', backref=db.backref(
        'colors', cascade='all, delete-orphan'))

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
                                                      cascade='all, delete-orphan'))
    addresses = db.relationship('Address', backref=db.backref(
        'orders', cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Order id=%s, order_number=%s>' % (self.id, self.order_number)


class OrderColor(db.Model):
    __tablename__ = 'orders_colors'
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), primary_key=True)
    color_id = db.Column(db.Integer, db.ForeignKey(
        'colors.id'), primary_key=True)
    amount = db.Column(db.Integer)
    order = db.relationship('Order', backref='colors')
    color = db.relationship('Color', backref='orders')

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
