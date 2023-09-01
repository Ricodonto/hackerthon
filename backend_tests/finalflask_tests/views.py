from flask import Blueprint, render_template,redirect, request
import openai

openai.api_key = "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"


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", name = "Rico")
    
@views.route("/ask")
def ask():
    check = True
    while check == True:
        message = []
        if len(message) == 0:
            check = False
            openai.api_key = "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"

            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Give me 3 ideas for apps I could build with openai apis "}])
            message.append(completion.choices[0].message.content)

    return message[0]
