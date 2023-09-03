from flask import Blueprint, render_template, request
from forms import PromptForm
from chatgpt import ai, cleanup


import os
from pathlib import Path

routes = Blueprint(__name__,"route")

@routes.route("/", methods=['GET', 'POST'])
def landing():
    form = PromptForm()
    if form.is_submitted():
        result = request.form
        response = {}
        usrprompt = str(result["prompt"])
        forwd_prompt = usrprompt + ", and MAKE SURE TO TELL ME THE ISBN CODES, DESCRIPTIONS AND AVERAGE RATINGS OF EACH BOOK"
        response["prompt"] = usrprompt
        response = ai(forwd_prompt)
        array_response = cleanup()

        if os.path.isfile("response.txt"):
            os.remove("response.txt")


        return array_response

    return render_template("landing_page.html", form=form)

@routes.route("/base")
def base():
    return render_template("base_template.html")

@routes.route("/about")
def about():
    return render_template("about.html")


@routes.route("/response")
def response():
    return render_template("book_table.html")