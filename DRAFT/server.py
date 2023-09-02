import os
from dotenv import load_dotenv

load_dotenv(".env")

from flask import Flask,render_template,request
from form import PromptForm
from test import ai
from bookfinder import bookfinder

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("CONFIG_KEY")
app.register_blueprint(bookfinder, url_prefix="/")


if __name__ == "__main__":
    app.run(debug=True,port=5000)