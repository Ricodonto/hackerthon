import datetime
import json
from flask import Blueprint, redirect, render_template, request, url_for, session
from forms import PromptForm
from forms import DeleteForm
from chatgpt import ai, cleanup
from flask import jsonify

import os
from supabase_py import create_client, Client
import bcrypt
import jwt

import os
from pathlib import Path

routes = Blueprint(__name__,"route")

@routes.route("/", methods=['GET', 'POST'])
def landing():
    if "username" not in session:
        return redirect('/login')

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

# Route for sign up
@routes.route("/signup", methods=["GET", "POST"])
def signup():
    error = False
    error_message = ""
    print(1)

    if request.method == "GET":
        print(2)
        return render_template("signup.html", error=error, error_message=error_message)
    else:
        # Get username and password
        print(3)
        username: str = request.form['username']
        password: str = request.form['password']

        # Validate details

        # Make sure none of the details are empty
        if len(username) == 0 or len(password) == 0:
            print(4)
            error = True
            error_message = "Invalid Credentials"
            # return render_template("signup.html", error=error, error_message=error_message)
            return jsonify({"error": error_message}), 400

        # Check if user already exists
        
        # Create connection to supabase
        print(5)
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        print(url)
        print(key)  
        client = create_client(supabase_url=url, supabase_key=key)

        print(6)
        user_exist_response = client.table('Users').select('username').eq('username', username).execute()

        # If user exists return error
        print(7)
        if len(user_exist_response['data']) > 0:
            print(8)
            error = True
            error_message = "User Already Exists"
            # return render_template("signup.html", error=error, error_message=error_message)
            return jsonify({"error": error_message}), 400

        # Hash password
        print(9)
        password_bytes = bytes(password, 'utf-8')
        salt = bcrypt.gensalt(rounds=15)
        hashed_password_bytes = bcrypt.hashpw(password_bytes, salt=salt)
        hashed_password = hashed_password_bytes.decode()

        # Store in database
        print(10)
        data, error = client.table("Users").insert({"username": username, "hashed_password": hashed_password}).execute()
        print(data, error)
        print(11)
        session['username'] = username

        return {}, 200

# Route for login
@routes.route("/login", methods=['GET', 'POST'])
def login():
    error = False
    error_message = ""
    print(1)

    # If it is a get request to this route display the login page
    if request.method == "GET":
        print(2)
        return render_template('login.html')
    else:
        print(3)
        # Get user details
        username = request.form['username']
        password = request.form['password']

        print(f"Username is {username} and password is {password}")

        # Fetch user with username
        # Create connection to supabase
        print(4)
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        print(5)
        client = create_client(supabase_url=url, supabase_key=key)

        # select password of user with username
        print(6)
        response = client.table('Users').select('hashed_password').eq('username', username).execute()
        print(response)
        
        # Return an error if nothing was found
        if (len(response['data']) <= 0):
            print(7)
            # Set error to true
            error = True
            error_message = "Invalid Credentials"
            # return render_template("login.html", error=error, error_message=error_message)
            return jsonify({"error": error_message}), 400

        # Compare hashed passwords
        print(8)
        hashed_password = response['data'][0]['hashed_password']
        hashed_password_bytes = hashed_password.encode()
        is_same = bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password_bytes)

        if is_same == True:
            print(9)
            # Create Sesssion
            session['username'] = username

            # Redirect to home page
            # return redirect("/")
            return {}, 200
        else:
            print(10)
            error = True
            error_message = "Invalid Credentials"
            # Show error screen
            # return render_template("login.html", error=error, error_message=error_message)
            return {"error": error_message}, 400

@routes.route("/about")
def about():
    if "username" not in session:
        return redirect('/login')
    return render_template("about.html")

@routes.route("/history", methods=['GET', 'POST'])
def history():
    if "username" not in session:
        return redirect('/login')
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
