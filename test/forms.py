from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class PromptForm(FlaskForm):
    prompt = StringField("Prompt, e.g What books should I read if I wanna learn javascript")
    submit = SubmitField("Enter")
