import os
import re
from dotenv import load_dotenv
from flask import request
load_dotenv('.env')
from AI.forms import PromptForm

import openai
import json
from datetime import datetime
import atexit

def ai(prompt):
    check = True
    while check == True:
        message = []
        if len(message) == 0:
            check = False
            openai.api_key = os.getenv("OPENAI_API_KEY")

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.0,
                messages=[
                    {"role":"system", "content":"do not contain a series of books"},
                    {"role":"system", "content":"only contain the title, isbn, description, author, and ratings for each book and use colons"},
                    {"role": "user", "content": prompt}
                ]
            )
            
            message.append(completion.choices[0].message.content)
    
    # Generating a file that contains GPT-3.5 Turbo's formatted results labeled response.txt
    file = open("response.txt", "w")
    file.write(message[0])
    file.close()

def cleanup():
    # Opening the generated file
    with open("response.txt", "r") as file:
        # Creating a list containing each line of the response.txt file
        lines = file.readlines()
        print("Response Loaded")
    titles = []
    authors = []
    isbns = []
    ratings = []
    descriptions = []
    images = []
    current_recommendation = {}

    for line in lines:
        line = line.rstrip()
        if matches := re.search(r"Title: (.+)$", line, re.IGNORECASE):
            current_recommendation["title"] = matches.group(1)
        elif matches := re.search(r"Author: (.+)$", line, re.IGNORECASE):
            current_recommendation["author"] = matches.group(1)
        elif matches := re.search(r"ISBN: ([0-9\-]+)$", line, re.IGNORECASE):
            isbn = matches.group(1)
            isbn = isbn.replace("-", "")
            current_recommendation["isbn"] = isbn
        elif matches := re.search(r"Ratings: ([0-9./]+)$", line, re.IGNORECASE):
            current_recommendation["ratings"] = matches.group(1)
        elif matches := re.search(r"Description: (.+)$", line, re.IGNORECASE):
            current_recommendation["description"] = matches.group(1)
        elif line.strip() == "":
            # An empty line indicates the end of a recommendation
            titles.append(current_recommendation.get("title", ""))
            authors.append(current_recommendation.get("author", ""))
            isbns.append(current_recommendation.get("isbn", ""))
            ratings.append(current_recommendation.get("ratings", ""))
            descriptions.append(current_recommendation.get("description", ""))
            images.append(f"https://covers.openlibrary.org/b/isbn/{current_recommendation.get('isbn', '')}-M.jpg")
            current_recommendation = {}

    # Returning an array containing the lists of required data
    details = {
        "title": titles,
        "author": authors,
        "isbn": isbns,
        "ratings": ratings,
        "description": descriptions,
        "images": images
    }
    record_recommendation(details)
    return details

def record_recommendation(details):
    history = []

    # Load existing history from the JSON file, if any
    try:
        with open("recommendation_history.json", "r") as file:
            history = json.load(file)
    except FileNotFoundError:
        pass
    
    form = PromptForm()
    if form.is_submitted():
        result = request.form
        user_prompt = result["prompt"]
    
    recommendation_entry = {
        "user_prompt": user_prompt,
        "recommendation": details}


    # Append the new recommendation to the history
    history.append(recommendation_entry)

    # Write the updated history back to the JSON file
    with open("recommendation_history.json", "w") as file:
        # Serialize the data to JSON (convert non-serializable lists to regular lists)
        serialized_history = []
        for recommendation in history:
            serialized_recommendation = {
                "user_prompt": recommendation["user_prompt"],
                "recommendation": {
                    "title": recommendation["recommendation"]["title"],
                    "author": recommendation["recommendation"]["author"],
                    "isbn": recommendation["recommendation"]["isbn"],
                    "ratings": recommendation["recommendation"]["ratings"],
                    "description": recommendation["recommendation"]["description"],
                    "images": recommendation["recommendation"]["images"]
                }
            }
            serialized_history.append(serialized_recommendation)
        json.dump(serialized_history, file, indent=4)

def clear_history_file():
    with open("recommendation_history.json", "w") as file:
        json.dump([], file)

response = {
"author": [
"Harper Lee",
"George Orwell",
"F. Scott Fitzgerald",
"Jane Austen"
],
"description": [
"Set in the 1930s, this classic novel by Harper Lee explores themes of racial injustice and the loss of innocence through the eyes of Scout Finch.",
"George Orwell's dystopian novel depicts a totalitarian society where individualism is suppressed and government surveillance is pervasive.",
"F. Scott Fitzgerald's masterpiece delves into the decadence and disillusionment of the Jazz Age, as seen through the eyes of Jay Gatsby.",
"Jane Austen's beloved novel follows the spirited Elizabeth Bennet as she navigates societal expectations, love, and the complexities of class."
],
"images": [
"https://covers.openlibrary.org/b/isbn/9780060935467-M.jpg",
"https://covers.openlibrary.org/b/isbn/9780451524935-M.jpg",
"https://covers.openlibrary.org/b/isbn/9780743273565-M.jpg",
"https://covers.openlibrary.org/b/isbn/9780141439518-M.jpg"
],
"isbn": [
"9780060935467",
"9780451524935",
"9780743273565",
"9780141439518"
],
"ratings": [
"4.27/5",
"4.17/5",
"3.91/5",
"4.26/5"
],
"title": [
"To Kill a Mockingbird",
"1984",
"The Great Gatsby",
"Pride and Prejudice"
]
}

def response_organizer(response):
    books = []
    for seq in range(len(response['title'])):
        book = {}
        book['author'] = response['author'][seq]
        book['description'] = response['description'][seq]
        book['image'] = response['images'][seq]
        book['isbn'] = response['isbn'][seq]
        book['rating'] = response['ratings'][seq] 
        book['title'] = response['title'][seq]
        books.append(book)
    return books
        
# Register the cleanup function to run on exit
atexit.register(clear_history_file)

if __name__ == '__main__':
    # For testing purposes
    # ai("cooking books")
    # print(cleanup())
    print(response_organizer(response))

