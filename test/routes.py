import json
from flask import Blueprint, redirect, render_template, request, url_for
from forms import PromptForm
from forms import DeleteForm
from chatgpt import ai, cleanup, clear_history_file
from flask import jsonify

import os
from pathlib import Path

routes = Blueprint(__name__,"route")

@routes.route("/", methods=['GET', 'POST'])
def landing():
    form = PromptForm()
    if form.is_submitted():
        result = request.form
        response = {}
        # Ensuring that the user sumbitted a filled in response and returning an error message if they havent
        if result["prompt"] == "":
            return render_template("landing_page.html", form=form, errormsg="Fill in the prompt")
        
        forwd_prompt = str(result["prompt"])
        response["prompt"] = forwd_prompt
        response = ai(forwd_prompt)
        array_response = cleanup()
        array_response["prompt"] = result["prompt"]

        # Deleting the response text file that was generated
        if os.path.isfile("response.txt"):
            os.remove("response.txt")

        # return array_response
        return render_template("book_table.html", details=array_response)

    return render_template("landing_page.html", form=form)


@routes.route("/about")
def about():
    return render_template("about.html")

@routes.route("/history", methods=['GET', 'POST'])
def history():
    # Read the recommendation history from the JSON file
    try:
        with open("recommendation_history.json", "r") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    form = DeleteForm()
    if form.is_submitted() and form.validate_on_submit():
        with open("recommendation_history.json", "w") as file:
            json.dump([], file)  # Just write the empty list, no need to assign the result to a variable
        return redirect(url_for("routes.history"))

    # Render the HTML template and pass the history data to it
    return render_template("history.html", history=history, form=form)
