from flask_wtf import FlaskForm   
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField  
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  
from app.models import User  


class RequestResetForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Email()])  
    submit = SubmitField('パスワード再設定のメールを送る')  
  
    def validate_email(self, email):  
        email = User.query.filter_by(email=email.data).first()  
        if email is None:  
            raise ValidationError('メールアドレスが間違っています。正しいメールアドレスを入力してください。')  
  
  
class ResetPasswordForm(FlaskForm):
    password = PasswordField('', validators=[DataRequired()])  
    confirm_password = PasswordField('確認用', validators=[DataRequired(), EqualTo('password')])  
    submit = SubmitField('パスワードを再設定する')