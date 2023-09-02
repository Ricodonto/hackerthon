import os
from dotenv import load_dotenv

load_dotenv(".env")

from flask import Flask,render_template,request
from form import PromptForm
from test import ai

app = Flask(__name__)
<<<<<<< HEAD
app.config['SECRET_KEY'] = os.getenv("CONFIG_KEY")
app.register_blueprint(bookfinder, url_prefix="/")

=======
app.config['SECRET_KEY'] = 'shazzy'

@app.route('/')
def home():
    return "HOME PAGE"

@app.route('/about')
def about():
    
    return render_template('about.html')



@app.route('/prompt',methods= ['GET', 'POST'])
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
>>>>>>> 507aeeb8d525c0f1489e1836f25b39c90709ffc4

if __name__ == "__main__":
    app.run(debug=True,port=5000)