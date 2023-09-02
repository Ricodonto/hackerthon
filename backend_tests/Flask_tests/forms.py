from flask_wtf import FlaskForm

#Look into WTForms
from wtforms import StringField, PasswordField, SubmitField

#it uses a class
class SignUpForm(FlaskForm):
    #The thing in the brackets of stringfield is the label the user will see
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Enter")