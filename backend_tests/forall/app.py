from flask import Flask
from efind import efind

#initializes the website
app = Flask(__name__)
#Setting a secret key

#Generate random string and replace 'test'
app.config['SECRET_KEY'] = 'shazzy'

app.register_blueprint(efind, url_prefix="/app")

if __name__ == "__main__":
    #You can add the specific port by adding the argument port=0000
    #Set custom port if necessary
    app.run(debug=True,port=8000)