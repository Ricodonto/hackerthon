import json, re
from flask import Blueprint, redirect, render_template, request, session
from chatgpt import ai, cleanup, response_organizer
from openlibrary import *
from flask import jsonify

import os
from supabase_py import create_client
import bcrypt

import os

routes = Blueprint(__name__,"route")

#Route for main page
@routes.route("/", methods=['GET', 'POST'])
def landing():
    username: str = request.form['username']
    # # Check whether there is a signed in username in session
    # if 'username' not in list(session.keys()):
    #     # return redirect('/signup')
    #     return jsonify({"error": "Not Logged In"}), 400
    #     # username = request.form['username']
    
    # load the landing page if no form is being submitted
    if request.method == 'GET':
        print(2)
        return {}, 200
    
    if request.method == 'POST':
        print(3)
        # get the prompt from the form submitted
        prompt: str = request.form['prompt']

        # Check if the prompt was empty and raise an error if necessary
        if len(prompt) == 0:
            print(4)
            error = True
            error_message = "Enter a prompt"
            return jsonify({"error": error_message}), 400
        
        # load the supabase url and the key
        print(5)
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        client = create_client(supabase_url=url, supabase_key=key)

        # get the current user's id and to insert an entry into the prompt table
        print(6)
        # userid = client.table("Users").select("id").eq('username',session['username']).execute()
        userid = client.table("Users").select("id").eq('username',username).execute()
        userid = userid['data'][0]['id']
        data = client.table("Prompts").insert({"prompt_asked": prompt, "userID": userid}).execute()
        print(data)
        promptid = data['data'][0]['id']
        session['prompt'] = promptid

        # Prompt GPT for recommendations
        print(7)
        response = ai(prompt)
        
        # Creating a log entry of the raw response from GPT
        print(8)
        with open('response.txt', 'r') as file:
            dict_lines = {'response':[]}
            for line in file:
                dict_lines['response'].append(line)
            client.table("Logs").insert({"raw_response": json.dumps(dict_lines), "user_id": userid,'prompt_id': promptid}, ).execute()


        # Cleaning up the response from GPT
        print(9)
        response = cleanup()

        # Deleting the file created to temporarily hold the response
        print(11)
        if os.path.isfile("response.txt"):
            os.remove("response.txt")
        response = response_organizer(response)
        print(response)
        session['response'] = 'response'
        
        # Adding an entry of the usable response to the response table
        print(10)
        for book in response:
            client.table("Responses").insert({"prompt_id": promptid, 
                                              "book_title": book['title'],
                                              "isbn":book['isbn'],
                                              "author":book['author'],
                                              "description":book['description'],
                                              "rating":book['rating'],
                                              "image":book['image']}).execute()
        print(response)
        return response

@routes.route("/currently_reading", methods=['POST'])
def current_list():
    error = False
    error_message = ""
    
    # olusr = request.form['olusr']
    username = str(request.form['username'])
    olusr = str(request.form['olusr'])
    
    if len(olusr) <= 0:
        error_message = "Enter an OpenLibrary Username"
        return jsonify({"error": error_message}), 400
    
    print(2)
    try:
        titles = currently_reading(olusr)
        if len(titles) == 0:
            error_message = "List is Empty"
            return jsonify({"error": error_message}), 400
    except KeyError:
        print(3)
        error_message = "Enter an existing OpenLibrary User"
        return jsonify({"error": error_message}), 400
    
    print(4)
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(supabase_url=url, supabase_key=key)
    
    print(5)
    data = client.table("Users").select("id").eq('username', username).execute()
    userid = data['data'][0]['id']
    data = client.table("Prompts").insert({"prompt_asked": 'Currently Reading List', "userID": userid,}).execute()
    promptid = data['data'][0]['id']

    print(6)
    olai(titles)
    
    print(7)
    with open('response.txt', 'r') as file:
        dict_lines = {'response':[]}
        for line in file:
            dict_lines['response'].append(line)
        client.table("Logs").insert({"raw_response": json.dumps(dict_lines), "user_id": userid,'prompt_id': promptid}, ).execute()

    print(8)
    response = cleanup()

    # Deleting the file created to temporarily hold the response
    print(9)
    if os.path.isfile("response.txt"):
        os.remove("response.txt")
    response = response_organizer(response)
    print(response)
    session['response'] = 'response'
    
    # Adding an entry of the usable response to the response table
    print(10)
    for book in response:
        client.table("Responses").insert({"prompt_id": promptid, 
                                          "book_title": book['title'],
                                          "isbn":book['isbn'],
                                          "author":book['author'],
                                          "description":book['description'],
                                          "rating":book['rating'],
                                          "image":book['image']}).execute()
    print(11)
    return response
    
@routes.route("/want_to_read", methods=['POST'])
def want_list():
    error = False
    error_message = ""
    
    # olusr = request.form['olusr']
    olusr:  str = request.form['olusr']
    username:  str = request.form['username']
    
    print(1)
    if len(olusr) <= 0:
        error_message = "Enter an OpenLibrary Username"
        return jsonify({"error": error_message}), 400
    
    print(2)
    try:
        titles = want_to_read(olusr)
        if len(titles) == 0:
            error_message = "List is Empty"
            return jsonify({"error": error_message}), 400
    except KeyError:
        print(3)
        error_message = "Enter an existing OpenLibrary User"
        return jsonify({"error": error_message}), 400
    
    print(4)
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(supabase_url=url, supabase_key=key)
    
    print(5)
    data = client.table("Users").select("id").eq('username',username).execute()
    userid = data['data'][0]['id']
    data = client.table("Prompts").insert({"prompt_asked": 'Want to Read List', "userID": userid,}).execute()
    promptid = data['data'][0]['id']

    print(6)
    olai(titles)
    
    print(7)
    with open('response.txt', 'r') as file:
        dict_lines = {'response':[]}
        for line in file:
            dict_lines['response'].append(line)
        client.table("Logs").insert({"raw_response": json.dumps(dict_lines), "user_id": userid,'prompt_id': promptid}, ).execute()

    print(8)
    response = cleanup()

    # Deleting the file created to temporarily hold the response
    print(9)
    if os.path.isfile("response.txt"):
        os.remove("response.txt")
    response = response_organizer(response)
    print(response)
    session['response'] = 'response'
    
    # Adding an entry of the usable response to the response table
    print(10)
    for book in response:
        client.table("Responses").insert({"prompt_id": promptid, 
                                          "book_title": book['title'],
                                          "isbn":book['isbn'],
                                          "author":book['author'],
                                          "description":book['description'],
                                          "rating":book['rating'],
                                          "image":book['image']}).execute()
    print(11)
    print(response)
    return response

@routes.route("/already_read", methods=['POST'])
def already_list():
    error = False
    error_message = ""
    
    # olusr = request.form['olusr']
    olusr:  str = request.form['olusr']
    username:  str = request.form['username']
    
    print(1)
    if len(olusr) <= 0:
        error_message = "Enter an OpenLibrary Username"
        return jsonify({"error": error_message}), 400
    
    print(2)
    try:
        titles = already_read(olusr)
        if len(titles) == 0:
            error_message = "List is Empty"
            return jsonify({"error": error_message}), 400
    except KeyError:
        print(3)
        error_message = "Enter an existing OpenLibrary User"
        return jsonify({"error": error_message}), 400
    
    print(4)
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(supabase_url=url, supabase_key=key)
    
    print(5)
    data = client.table("Users").select("id").eq('username',username).execute()
    userid = data['data'][0]['id']
    data = client.table("Prompts").insert({"prompt_asked": 'Already Read List', "userID": userid,}).execute()
    promptid = data['data'][0]['id']

    print(6)
    olai(titles)
    
    print(7)
    with open('response.txt', 'r') as file:
        dict_lines = {'response':[]}
        for line in file:
            dict_lines['response'].append(line)
        client.table("Logs").insert({"raw_response": json.dumps(dict_lines), "user_id": userid,'prompt_id': promptid}, ).execute()

    print(8)
    response = cleanup()

    # Deleting the file created to temporarily hold the response
    print(9)
    if os.path.isfile("response.txt"):
        os.remove("response.txt")
    response = response_organizer(response)
    print(response)
    session['response'] = 'response'
    
    # Adding an entry of the usable response to the response table
    print(10)
    for book in response:
        client.table("Responses").insert({"prompt_id": promptid, 
                                          "book_title": book['title'],
                                          "isbn":book['isbn'],
                                          "author":book['author'],
                                          "description":book['description'],
                                          "rating":book['rating'],
                                          "image":book['image']}).execute()
    print(11)
    return response


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
        
        # If username is invalid return error
        print(-7)
        print(username)
        # regular expression check to ensure the username only contains word characters
        if re.search(r"^[\w]+$", username):
            print("Valid")

        else:
            error = True
            error_message = "Username is invalid"
            return jsonify({'error':error_message}), 400            

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

# Route for about
@routes.route("/about")
def about():
    if "username" not in session:
        return redirect('/login')
    return render_template("about.html")



# Route for history
@routes.route("/history", methods=['GET', 'POST', 'DELETE'])
def history():
    
    username:  str = request.form['username']
    # # Checking if username is in the current session
    # if 'username' not in list(session.keys()):
    #     return redirect('/signup')
    #     # return jsonify({"error": "Not Logged In"}), 400
    #     # username = request.form['username']    
    # # if "username" not in session:
    # #     return redirect('/login')
    # if len(request.form['username']) <= 0:
    #     # return redirect('/login')
    #     return jsonify({"error": "Not Logged In"}), 400
    # username = request.form['username']
    
    # Checking if the user wishes to view their history
    if request.method == 'GET':
        print(2)
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        client = create_client(supabase_url=url, supabase_key=key)

        print(3)
        # Getting the user's id and past prompt ids'
        data = client.table("Users").select("id").eq('username',username).execute()
        userID = data['data'][0]['id']
        data = client.table('Prompts').select('id', 'prompt_asked').eq('userID', str(userID)).execute()
        history = data['data']
        
        print(4)
        print(history)
        for item in range(len(history)):
            data = client.table('Responses').select('book_title', 'isbn', 'author', 'description', 'rating', 'image').eq('prompt_id', str(history[item]['id'])).execute()

            # Checking whether past prompt id had an empty prompt
            if len(data['data']) == 0:
                pass
            else:
                # Appending the response data to their respoective prompt id
                history[item]['response'] = []
                for book in range(len(data['data'])):
                    history[item]['response'].append(data['data'][book])

        print(history)
        return history

    # if someone sends a POST request they will delete the history, allow specific history to be deleted

# @routes.route('/del_all_history', methods=['DELETE'])
# def rm_all_history():
#     url = os.environ.get("SUPABASE_URL")
#     key = os.environ.get("SUPABASE_KEY")
#     client = create_client(url, key)

#     data = client.table("Users").select("id").eq('username',session['username']).execute()
#     userID = data['data'][0]['id']
#     data = client.table('Prompts').select('id', 'prompt_asked').eq('userID', str(userID)).execute()
#     prompts = data['data']

#     print()

# @routes.route('/del_prompt_history', methods=['GET'])
# def rm_prompt():
#     url = os.environ.get("SUPABASE_URL")
#     key = os.environ.get("SUPABASE_KEY")
#     client = create_client(url, key)

#     # prompt_id = request.form['prompt_id']
#     prompt_id = 13

#     data = client.table("Prompts").select('id').eq("id", str(prompt_id)).execute()
#     data.raise_for_status
#     # try:
#     #     client.table("Responses").delete().eq("prompt_id", str(prompt_id)).execute()
#     # zexcept JSONDecodeError:
#     #     try:
#     #         client.table("Prompts").delete().eq("id", str(prompt_id)).execute()
#     #     except JSONDecodeError:
#     #         client.table("Prompts").select('id').eq("id", str(prompt_id)).execute()
#     #         print('done')
#     #         return {}, 200