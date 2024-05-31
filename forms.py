##WTforms
from flask_wtf import FlaskForm
#Stringfield is just a form input Box
from wtforms import StringField, SubmitField, EmailField, SelectField, IntegerField, PasswordField
#Validating input either filled or filled input type
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField
#Creating a form class and can be used by calling in a specific function
#We inherited FlaskForm

class LoginForm(FlaskForm):
    matric_no = IntegerField('Matric_No', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class PaymentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[DataRequired()])
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    #Form for input Box and validator
    #DataRequired validator Pops up when you dont input any value Required
    surname = StringField("Surname", validators=[DataRequired()])
    lastname = StringField("Lastname", validators=[DataRequired()])
    middlename = StringField("Middlename", validators=[DataRequired()])
    gender_choices = [('male', 'Male'), ('female', 'Female')]
    gender = SelectField('Gender', choices=gender_choices, validators=[DataRequired()])
    matric = IntegerField('Matric_No', validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Submit")
    profile_pic = FileField('Profile')