from wtforms import StringField, IntegerField, PasswordField, Form
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError, EqualTo

from app.models.user import User


class RegisterForm(Form):

    email = StringField(validators = [DataRequired(),Length(8,64),Email(message='电子邮箱不符规范')])


    password = PasswordField(validators=[DataRequired(message = '密码不能为空'), Length(6, 32)])

    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])


    def validate_email(self, field):
        #如果数据库中有重复email
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        #如果数据库中有重复昵称
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')


class EmailForm(Form):
    email = StringField(validators = [DataRequired(),Length(8,64),Email(message='电子邮箱不符规范')])

class LoginForm(EmailForm):

    password = PasswordField('密码', validators=[DataRequired(message='密码不可以为空，请输入你的密码')])

class ResetPasswordForm(Form):
    password1 = PasswordField('新密码', validators=[
        DataRequired(), Length(6, 20, message='密码长度至少需要在6到20个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(), Length(6, 20)])