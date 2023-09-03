import os
from dotenv import load_dotenv
load_dotenv(".env")


from flask import Flask, render_template
from routes import routes


app = Flask(__name__)
app.register_blueprint(routes, url_prefix="/")
app.config['SECRET_KEY'] = os.getenv("CONFIG_KEY")

if __name__ == '__main__':
    app.run(debug=True)