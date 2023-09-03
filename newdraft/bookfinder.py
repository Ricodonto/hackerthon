from flask import Blueprint, render_template, request
from form import PromptForm
from test import ai

bookfinder = Blueprint(__name__, 'bookfinder')

@bookfinder.route('/about')
def about():
    
    return render_template('about.html')