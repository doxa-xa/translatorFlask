from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, SelectField, EmailField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from email_validator import validate_email
from translator.models import User
class LoginForm(FlaskForm):
    user_name = StringField(label='Потребителско име:', validators=[Length(min=4, max=12), DataRequired()])
    password = PasswordField(label='Парола:', validators=[Length(min=8), DataRequired()])
    submit = SubmitField(label='Влез')

class RegisterForm(FlaskForm):
    user_name = StringField(label='Потребителско име:', validators=[Length(min=4, max=12), DataRequired()])
    password = PasswordField(label='Парола:', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Повтори Паролата:', validators=[EqualTo('password'), DataRequired()])
    email = EmailField(label='Имейл:', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Регистрирай')

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Потребителят съществува моля изберете друго име.')
        
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Имейл адреса вече съществува, да не би да имате регистрация вече?')

class UploadForm(FlaskForm):
    subtitle = FileField(label='Избери файл за превод:')
    submit = SubmitField(label='Качи')

class DownloadForm(FlaskForm):
    language = SelectField(label='Избери език:', choices=[('bg','Български'),('rus','Руски')])
    submit = SubmitField(label='Свали')