from flask import Blueprint, render_template,redirect, request

#"forms" here is the name of the signup class python file, For the signup form, used to create the signup form
from forms import Promptform
from test import ai

efind = Blueprint(__name__, 'efind')

#End of sing up form
# Change from signup to ho
@efind.route('/', methods=['GET', 'POST'])
def landingpage():
    #Create a form object
    form = Promptform()
    if form.is_submitted():
        #This is a regular dictionary in python
        result = request.form
        # Remove the submit key
        # Put the prompt value into the ai funciton
        # Add a key called response with the value being the response  = ai(result['prompt'])
        # put the response into the below render template funciton
        return render_template('response.html', result=result)

    return render_template('landingpage.html', form=form)
