from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

class PromptForm(FlaskForm):
    prompt = StringField("PROMPT")
    submit = SubmitField()