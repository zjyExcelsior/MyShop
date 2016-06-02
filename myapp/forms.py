# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms.validators import ValidationError
from .models import User


class LoginForm(Form):
    username = StringField('useranme', validators=[Required(), Length(1, 10)])
    password = PasswordField('password', validators=[Required()])
    submit = SubmitField(u'登陆')

    def validate_username(self, field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户不存在')


class RegistrationForm(Form):
    username = StringField('useranme', validators=[Required(), Length(1, 10)])
    password = PasswordField('password', validators=[Required(), EqualTo(
        'password2', message=u'再次输入的密码不一致')])
    password2 = PasswordField('password2', validators=[Required()])
    submit = SubmitField(u'注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已存在')

class UserInfoForm(Form):
    username = StringField('username', validators=[Required(), Length(1, 10)])
    password = PasswordField('password', validators=[EqualTo(
        'password2', message=u'再次输入的密码不一致')])
    password2 = PasswordField('password2')
    submit = SubmitField(u'保存')

class AddressForm(Form):
    name = StringField('name', validators=[Required()])
    phone_number = StringField('phone_number')
    province = StringField('province')
    city = StringField('city')
    region = StringField('region')
    detail_address = StringField('detail_address')
    postcode = StringField('postcode')
    submit = SubmitField(u'保存')
    address_id = StringField('address_id')
