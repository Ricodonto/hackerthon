import os, re
from dotenv import load_dotenv
load_dotenv('.env')

import openai

# def main():
#     user_input = input("Enter prompt, e.g What book should I read to learn javascript ")
#     user_input = user_input + ", and MAKE SURE TO TELL ME THE ISBN CODES, DESCRIPTIONS AND AVERAGE RATINGS OF EACH BOOK and don't recommend series"
#     ai(user_input)
#     details = cleanup()
#     print(details)



def ai(prompt):
    check = True
    while check == True:
        message = []
        if len(message) == 0:
            check = False
            openai.api_key = os.getenv("OPENAI_API_KEY")

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                # Figure out whether you wanna give the assistant a role
                
                # Change if giving it starts not giving isbn
                temperature = 0.0,
                messages=[{"role":"system", "content":"do not contain a series of books"},
                    {"role":"system", "content":"only contain the title, isbn, descrition, author and ratings for each book and use colons"},
                    {"role": "user", "content": prompt}])
            message.append(completion.choices[0].message.content)
    
    
    file = open("response.txt", "w")
    file.write(message[0])
    file.close()

def cleanup():
    with open("response.txt", "r") as file:
        lines = file.readlines()
        print("Response Loaded")
    titles = []
    for line in lines:
        line = line.rstrip()
        if matches := re.search(r"Title: (.+)$", line, re.IGNORECASE):
            title = matches.group(1)
            titledict = {}
            titledict = title
            titles.append(titledict)

    # Sample output is [{'title': 'Eloquent JavaScript: A Modern Introduction to Programming'}, {'title': 'JavaScript: The Good Parts'}, {'title': "You Don't Know JS"}, {'title': 'JavaScript: The Definitive Guide'}, {'title': 'Head First JavaScript Programming'}]

    authors = []
    for line in lines:
        line = line.rstrip()

        if matches := re.search(r"Author: (.+)$", line, re.IGNORECASE):
            author = matches.group(1)
            authors.append(author)


    isbns = []
    for line in lines:
        line = line.rstrip()

        if matches := re.search(r"ISBN: ([0-9\-]+)$", line, re.IGNORECASE):
            isbn = matches.group(1)
            isbn = isbn.replace("-", "")
            isbns.append(isbn)

    if len(isbns) == 0:
        for line in lines:
            line = line.rstrip()

            if matches := re.search(r"ISBN(-)?(13)?: (.+)$", line, re.IGNORECASE):
                isbn = matches.group(1)
                isbns.append(isbn)


    ratings = []
    for line in lines:
        line = line.rstrip()

        if matches := re.search(r"Ratings: ([0-9./]+)$", line, re.IGNORECASE):
            rating = matches.group(1)
            ratings.append(rating)


    descriptions = []
    for line in lines:
        line = line.rstrip()

        if matches := re.search(r"Description: (.+)$", line, re.IGNORECASE):
            description = matches.group(1)
            descriptions.append(description)

    images = []
    for isbn in isbns:
        imageurl = f"https://covers.openlibrary.org/b/isbn/{isbn}.jpg"
        images.append(imageurl)

    details = {"title":titles, "author":authors, "isbn":isbns, "ratings":ratings, "description":descriptions, "images":images}
    return details



if __name__ == '__main__':
    ai("cooking books")
    print(cleanup())
    #main()