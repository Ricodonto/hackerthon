from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = "test"

@app.route("/")
def page():
    return render_template("page.html")

if __name__ == '__main__':
    app.run(debug=True)