from flask import Flask
from efind import efind

#initializes the website
app = Flask(__name__)
#Setting a secret key
app.config['SECRET_KEY'] = 'test'

app.register_blueprint(efind, url_prefix="/")

if __name__ == "__main__":
    #You can add the specific port by adding the argument port=0000
    app.run(debug=True)