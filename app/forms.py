from flask_wtf import FlaskForm   
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField  
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  
from app.models import User  


def check_unique_username(form, field):
    if User.query.filter_by(username=field.data).count() != 0:
        raise ValidationError('ユーザー名「 {} 」はすでに使用されています。'.format(field.data))

def check_unique_email(form, field):
    if User.query.filter_by(email=field.data).count() != 0:
        raise ValidationError('メールアドレス「 {} 」はすでに登録されています。'.format(field.data))

def exists_email(form, field):
    if User.query.filter_by(email=field.data).count() == 0:
        raise ValidationError('メールアドレスが間違っています。正しいメールアドレスを入力してください。')


class SignupForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), check_unique_username])
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message='有効なメールアドレスを入力してください。'), check_unique_email])
    password = PasswordField('パスワード', validators=[DataRequired(), Length(min=8, max=15, message='有効なパスワードを入力してください。')])
    submit = SubmitField('登録する')


class RequestResetForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), exists_email])
    submit = SubmitField('パスワード再設定のメールを送る')
  
  
class ResetPasswordForm(FlaskForm):
    password = PasswordField('パスワード', validators=[DataRequired()])
    confirm_password = PasswordField('確認用', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('パスワードを再設定する')

