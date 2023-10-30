import json, re
from flask import Blueprint, redirect, render_template, request, session
from chatgpt import ai, cleanup, response_organizer
from openlibrary import *
from flask import jsonify

import os
from supabase import create_client
import bcrypt

from simplejson.errors import JSONDecodeError

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
        userid = userid.data[0]['id']
        data = client.table("Prompts").insert({"prompt_asked": prompt, "userID": userid}).execute()
        print(data)
        promptid = data.data[0]['id']
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
        output = {'prompt_id': promptid, 'prompt_asked':prompt, 'response':response}
        return output
    else:
        print(2)
        return {}, 200

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
    userid = data.data[0]['id']
    data = client.table("Prompts").insert({"prompt_asked": 'Currently Reading List', "userID": userid,}).execute()
    promptid = data.data[0]['id']

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

    output = {'prompt_id': promptid, 'prompt_asked':'Already Read List', 'response':response}
    return output
    
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
    userid = data.data[0]['id']
    data = client.table("Prompts").insert({"prompt_asked": 'Want to Read List', "userID": userid,}).execute()
    promptid = data.data[0]['id']

    print(6)
    print(titles)
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

    output = {'prompt_id': promptid, 'prompt_asked':'Want to Read List', 'response':response}
    return output

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
    userid = data.data[0]['id']
    data = client.table("Prompts").insert({"prompt_asked": 'Already Read List', "userID": userid,}).execute()
    promptid = data.data[0]['id']

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
    output = {'prompt_id': promptid, 'prompt_asked':'Already Read List', 'response':response}
    return output


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
        client = create_client(supabase_url=url, supabase_key=key)

        print(6)
        user_exist_response = client.table('Users').select('username').eq('username', username).execute()

        # If user exists return error
        print(7)
        if len(user_exist_response.data) > 0:
            print(8)
            error = True
            error_message = "User Already Exists"
            # return render_template("signup.html", error=error, error_message=error_message)
            return jsonify({"error": error_message}), 400
        
        # If username is invalid return error
        print(-7)
        print(username)
        # regular expression check to ensure the username only contains word characters
        if re.search(r"[\w]+", username):
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
        data = client.table("Users").insert({"username": username, "hashed_password": hashed_password}).execute()
        print(data.data)
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
        if (len(response.data) <= 0):
            print(7)
            # Set error to true
            error = True
            error_message = "Invalid Credentials"
            # return render_template("login.html", error=error, error_message=error_message)
            return jsonify({"error": error_message}), 400

        # Compare hashed passwords
        print(8)
        hashed_password = response.data[0]['hashed_password']
        hashed_password_bytes = hashed_password.encode()
        is_same = bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password_bytes)

        print(is_same)

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
@routes.route("/history", methods=['GET', 'POST'])
def history(usr=''):
    if len(usr) > 0:
        username = usr
    else:
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
        userID = data.data[0]['id']
        data = client.table('Prompts').select('id', 'prompt_asked').eq('userID', str(userID)).execute()
        history = data.data
        
        print(4)
        print(history)
        for item in range(len(history)):
            data = client.table('Responses').select('book_title', 'isbn', 'author', 'description', 'rating', 'image').eq('prompt_id', str(history[item]['id'])).execute()
            # Checking whether past prompt id had an empty prompt
            if len(data.data) == 0:
                pass
            else:
                # Appending the response data to their respoective prompt id
                history[item]['response'] = []
                for book in range(len(data.data)):
                    history[item]['response'].append(data.data[book])

        print(5)
        print(history)
        print(6)
        return history

    # if someone sends a POST request they will delete the history, allow specific history to be deleted

# Route to delete all of the user's history
@routes.route('/del_all_history', methods=['DELETE'])
def rm_all_history():
    error = False
    error_message = ""
    
    username:  str = request.form['username']

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(url, key)

    data = client.table("Users").select("id").eq('username',username).execute()
    user_id = data.data[0]['id']
    print(user_id)
    data = client.table('Prompts').select('id').eq('userID', str(user_id)).execute()
    prompts = []
    for prompt in data.data:
        prompts.append(str(prompt['id']))
    

    print(prompts)

    client.table("Feedback").delete().in_("prompt_id", prompts).execute()
    client.table("Logs").delete().in_("prompt_id", prompts).execute()
    client.table("Responses").delete().in_("prompt_id", prompts).execute()
    client.table("Prompts").delete().in_("id", prompts).execute()
                    #For testing purposes
    print('done')
    request.method = 'GET'                    
    return history(username)


# Route for deleting a specific prompt
@routes.route('/del_prompt_history', methods=['DELETE'])
def rm_prompt():
    print(1)
    prompt_id: str = request.form['prompt_id']
    username:  str = request.form['username']
    
    print(prompt_id)
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(url, key)


    print(2)
    print(3)
    client.table("Feedback").delete().eq("prompt_id", str(prompt_id)).execute()
    print(4)
    client.table("Logs").delete().eq("prompt_id", str(prompt_id)).execute()
    print(5)
    client.table("Responses").delete().eq("prompt_id", str(prompt_id)).execute()
    print(6)
    client.table("Prompts").delete().eq("id", str(prompt_id)).execute()
                    # For testing purposes
    print(7)
    request.method = 'GET'
    return history(username)
    

@routes.route('/profile/changeusr', methods=['POST'])
def change_username():
    error = False
    error_message = ""

    old_username: str = request.form['old_username']
    new_username: str = request.form['new_username']
    
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(supabase_url=url, supabase_key=key)

    # Check if the username already exists
    data = client.table("Users").select('username', 'id').eq('username', str(new_username)).execute()
    print(data.data)
    if len(data.data) > 0:
        error = True
        error_message = 'Username already taken'

        return jsonify({"error": error_message}), 400
    elif re.search(r"[\W]+", new_username):
        error = True
        error_message = 'Username invalid'

        return jsonify({"error": error_message}), 400
    elif len(new_username) <= 0:
        error = True
        error_message = 'Enter a new username'

        return jsonify({"error": error_message}), 400
    else:
        data = client.table("Users").update({'username': str(new_username)}).eq('username', str(old_username)).execute()
        print(data.data[0]['username'])

    data = client.table("Users").select('username','id').eq('username', str(new_username)).execute()
    
    return data.data[0]


@routes.route('/profile/changepwd', methods=['POST'])
def change_password():
    error = False
    error_message = ""

    username: str = request.form['username']
    old_password: str = request.form['old_password']
    new_password: str = request.form['new_password']
    confirm_new: str = request.form['confirm_new']


    if len(new_password) == 0 or len(old_password) == 0:
        error = True
        error_message = "Empty Password field"

        return {"error": error_message}, 400

    if new_password != confirm_new:
        error = True
        error_message = "Passwords do not match"

        return {"error": error_message}, 400
    

    print(2)
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(supabase_url=url, supabase_key=key)

    print(3)
    data = client.table("Users").select('id', 'hashed_password').eq('username', str(username)).execute()
    user_id = data.data[0]['id']
    hashed_password = data.data[0]['hashed_password']
    old_password_bytes = old_password.encode()
    
    print(4)
    is_same = bcrypt.checkpw(old_password_bytes, hashed_password.encode())

    if is_same:
        print(5)
        new_password_bytes = new_password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=15)
        new_hash = bcrypt.hashpw(new_password_bytes, salt)
        new_hash = new_hash.decode()
        
        print(6)
        client.table("Users").update({'hashed_password':new_hash}).eq('id', str(user_id)).execute()
        return {'response': f"New password is {new_password}"}, 200
    else:
        error = True
        error_message = "Original Password is incorrect"

        return {"error": error_message}, 400

@routes.route('/feedback/good', methods=['POST'])
def good_feedback():
    prompt_id: str = request.form['prompt_id']
    username: str = request.form['username']

    print(1)
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(supabase_url=url, supabase_key=key)

    print(2)
    data = client.table("Users").select('id').eq('username', str(username)).execute()
    user_id = data.data[0]['id']

    print(3)
    data = client.table("Logs").select('id').eq('prompt_id', str(prompt_id)).execute()
    log_id = data.data[0]['id']

    print(4)
    data = client.table("Feedback").insert({"prompt_id": str(prompt_id), "user_id": str(user_id), 'log_id':str(log_id), 'opinion': 'Yes'}).execute()
    
    return data.data, 200

@routes.route('/feedback/bad', methods=['POST'])
def bad_feedback():
    prompt_id: str = request.form['prompt_id']
    username: str = request.form['username']

    print(1)
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    client = create_client(supabase_url=url, supabase_key=key)

    print(2)
    data = client.table("Users").select('id').eq('username', str(username)).execute()
    user_id = data.data[0]['id']

    print(3)
    data = client.table("Logs").select('id').eq('prompt_id', str(prompt_id)).execute()
    log_id = data.data[0]['id']

    print(4)
    data = client.table("Feedback").insert({"prompt_id": str(prompt_id), "user_id": str(user_id), 'log_id':str(log_id), 'opinion': 'No'}).execute()
    
    return data.data, 200

@routes.route('/emailing', methods=['POST'])
def emailing():
    # receiver is an email
    receiver: str = request.form['reciever'] # This is  a string, if many they are separated by commas
    prompt_asked: str = request.form['prompt_asked'] # is a string
    responses: str = request.form['responses'] # is a list
    username: str = request.form['username']
    
    

    return [], 200
    print()


