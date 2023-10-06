import json
from flask import Blueprint, render_template, request
from forms import PromptForm
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

from flask import render_template

@routes.route("/history")
def history():
    # Read the recommendation history from the JSON file
    try:
        with open("recommendation_history.json", "r") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    # Render the HTML template and pass the history data to it
    return render_template("history.html", history=history)
    
    
@routes.route("/delhistory")
def delhistory():
    with open("recommendation_history.json", "w") as file:
        deleted = json.dump([], file)
    return render_template("delhistory.html",deleted=deleted)