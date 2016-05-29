# coding: utf-8
from . import db
from flask_login import UserMixin
from . import login_manager
from . import admin
from flask_admin.contrib.sqla import ModelView


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<Role id=%r, name=%r>' % (self.id, self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref=db.backref('users',
                                                      cascade='all, delete-orphan'))

    def __repr__(self):
        return '<User id=%r, username=%r>' % (self.id, self.username)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone_number = db.Column(db.String(11))
    province = db.Column(db.String(64))
    city = db.Column(db.String(64))
    region = db.Column(db.String(64))
    detail_address = db.Column(db.String(64))
    postcode = db.Column(db.String(6))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('addresses',
                                                      cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Address id=%r, name=%r>' % (self.id, self.name)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    price = db.Column(db.String(8))
    colors = db.Column(db.String(64))
    detail = db.Column(db.Text)
    amount = db.Column(db.Integer)
    img_url = db.Column(db.String(64))

    def __repr__(self):
        return '<Product id=%r, name=%r>' % (self.id, self.name)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer)
    order_time = db.Column(db.Integer)
    total = db.Column(db.String(10))
    state = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('orders',
                                                      cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Order id=%s, order_number=%s>' % (self.id, self.order_number)


class OrderProduct(db.Model):
    __tablename__ = 'orders_products'
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
    amount = db.Column(db.Integer)
    order = db.relationship('Order', backref='products')
    product = db.relationship('Product', backref='orders')

    def __repr__(self):
        return '<OrderProduct order_id=%r, product_id=%r, amount=%r>' % (self.order_id, self.product_id, self.amount)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Address, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(OrderProduct, db.session))
