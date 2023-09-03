from flask import Blueprint, render_template, request
from forms import PromptForm
from chatgpt import ai

routes = Blueprint(__name__,"route")

@routes.route("/", methods=['GET', 'POST'])
def landing():
    form = PromptForm()
    if form.is_submitted():
        result = request.form
        response = {}
        response["prompt"] = result["prompt"]
        response["response"] = ai(result["prompt"])

        return render_template("response.html", response=response)

    return render_template("landing_page.html", form=form)

@routes.route("/base")
def base():
    return render_template("base_template.html")

@routes.route("/about")
def about():
    return render_template("about.html")


@routes.route("/response")
def response():
    return render_template("response.html")