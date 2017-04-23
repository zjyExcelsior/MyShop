# coding: utf-8
from myshop import create_app
from myshop.models import Role, User, Address, Product, Color, Order, OrderColor

app = create_app('config')

if __name__ == '__main__':
    app.run(debug=True)
