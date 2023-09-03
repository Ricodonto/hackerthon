from flask import Blueprint, render_template

routes = Blueprint(__name__,"route")

@routes.route("/")
def page():
    return render_template("page.html")

@routes.route("/base")
def base():
    return render_template("base_template.html")

@routes.route("/about")
def about():
    return render_template("about.html")

@routes.route("/landing")
def landing():
    return render_template("landing_page.html")

@routes.route("/response")
def response():
    return render_template("response.html")