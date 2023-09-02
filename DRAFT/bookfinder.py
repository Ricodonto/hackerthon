from flask import Blueprint, render_template, request
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
        #result["prompt"] is the question the user asked
        prompt = result["prompt"]
        #Creating response dicitonary
        response = {}
        #adding question and answer of the user
        response["prompt"] = prompt
        #ai(prompt) is the answers gpt gave and the "result" is the key
        response["result"] = ai(prompt)

        # count = 0
        # for dict in response["result"]:
        #     count = count + 1
        #     keyname = "book" + str(count)
        #     response[keyname] = dict
        
        return render_template('response.html', response=response)
    
    return render_template('landing_page.html', form=form)
