from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, ValidationError
from wtforms.fields.simple import PasswordField
from wtforms.validators import Required, Email, EqualTo

class LocationForm(FlaskForm):
    street = StringField('Name of your street', validators=[Required()])
    house_number = StringField('Your house number', validators=[Required()])
    phone_number = StringField('Your mobile number', validators=[Required()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    username = StringField('Your username')
    email = StringField('Your email address', validators=[Email()])
    password = PasswordField('Enter your password')
    submit = SubmitField('Submit')