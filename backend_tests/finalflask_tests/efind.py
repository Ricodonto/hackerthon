from flask import Flask
from efind import efind

#initializes the website
efind = Flask(__name__)

efind.register_blueprint(efind, url_prefix="/")

if __name__ == "__main__":
    #You can add the specific port by adding the argument port=0000
    efind.run(debug=True)