from flask_wtf import FlaskForm

#Look into WTForms
from wtforms import StringField,SubmitField #PasswordField

#it uses a class
class Promptform(FlaskForm):
    #The thing in the brackets of stringfield is the label the user will see
    #Change from username to prompt
    username = StringField("Username")
    # password = PasswordField("Password")
    # Change to Enter or something understandable
    submit = SubmitField("Enter")