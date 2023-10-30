import os
import re
from dotenv import load_dotenv
from flask import request
load_dotenv('.env')

import openai
from datetime import datetime

def ai(prompt ):
    check = True
    while check == True:
        message = []
        if len(message) == 0:
            check = False
            openai.api_key = os.getenv("OPENAI_API_KEY")

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.1,
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
    # record_recommendation(details)
    return details


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
        


if __name__ == '__main__':
    # For testing purposes
    # ai("cooking books")
    # print(cleanup())
    # print(response_organizer(response))
    cleanup()

