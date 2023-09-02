from flask import Blueprint, render_template,redirect, request
import openai
from test import ai

openai.api_key = "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"


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", name = "Rico")
    
@views.route("/ask")
def ask():
    return ai("Hi")
