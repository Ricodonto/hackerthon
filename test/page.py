from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = "test"

@app.route("/")
def page():
    return render_template("page.html")

@app.route("/base")
def base():
    return render_template("base_template.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/landing")
def landing():
    return render_template("landing_page.html")

@app.route("/response")
def response():
    return render_template("response.html")

if __name__ == '__main__':
    app.run(debug=True)