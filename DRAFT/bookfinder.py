from flask import Blueprint, render_template,redirect, request
from form import PromptForm
from test import ai

bookfinder = Blueprint(__name__, 'bookfinder')


@bookfinder.route('/about')
def about():
    
    return render_template('about.html')



@bookfinder.route('/',methods= ['GET', 'POST'])
def prompt_entry():
    form = PromptForm()
    if form.is_submitted():
        result = request.form
        prompt = result["prompt"]
        response = {}
        response["prompt"] = prompt
        response["result"] = ai(prompt)
        
        return render_template('response.html', result=response)
    
    return render_template('landing_page.html', form=form)
