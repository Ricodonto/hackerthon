from flask import Blueprint, render_template,redirect, request

#"forms" here is the name of the signup class python file, For the signup form, used to create the signup form
from forms import SignUpForm
efind = Blueprint(__name__, 'efind')

@efind.route('/')
def home():
    return 'Homepage'

@efind.route('/prompt')
def prompt():
    return 'Prompt Page'


#To use unique ids added to the url you can use rules in the routes , the <prompt_id>
#You can specify the datatype by adding <datatype:rule> e.g <intg:prompt_id> 
#It then acts like a variable in python 
#I don't know why you can't use string
@efind.route('/prompt/<string:prompt_id>')
def prompt_page(prompt_id):
    return 'This is the ' + str(prompt_id)

#Render template allows you to load html files
#It also allows you to pass variable(s) that can be used to manipulate the html
@efind.route('/rendertmp')
def rendered():
    #Lists and other values used to generate this webage should be entered while defining it
    people = [{'name': 'nathan', 'height': 'tall'},
        {'name': 'christopher', 'height': 'short'}]
    return render_template('index.html', name='Rico', tall=True, people=people)



#Template inheritance in jinja and flask
@efind.route('/inheritance')
def inherited():
    #When inheriting you put the name of the non-base html file
    return render_template('inheritance.html')

#Signup form, unfinished
@efind.route('/sign')
def sign():
    #Create a form object
    form = SignUpForm()
    return render_template('signup.html', form=form)

#End of sing up form
@efind.route('/signup', methods=['GET', 'POST'])
def singup():
    #Create a form object
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)

    return render_template('signup.html', form=form)
