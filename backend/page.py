import os
from dotenv import load_dotenv
load_dotenv()


from flask import Flask
from routes import routes
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(routes, url_prefix="/")
app.config['SECRET_KEY'] = os.getenv("CONFIG_KEY")
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')