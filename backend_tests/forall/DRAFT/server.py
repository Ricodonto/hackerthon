from flask import Flask,render_template,request
from form import PromptForm

app = Flask(__name__)
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
        return render_template('response.html',result=result)
    
    return render_template('landing_page.html', form=form)

if __name__ == "__main__":
    app.run()