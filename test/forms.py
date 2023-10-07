from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class PromptForm(FlaskForm):
    prompt = StringField("For example: What books should I read if I want to learn javascript")
    submit = SubmitField("Search")

