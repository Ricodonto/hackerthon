import json, requests, sys, openai, os
from dotenv import load_dotenv
load_dotenv('.env')

def currently_reading(olusr):
    response = requests.get(f"https://openlibrary.org/people/{olusr}/books/currently-reading.json")
    json_response = response.json()
    titles = []
    for work in json_response['reading_log_entries']:
        titles.append(work['work']['title'])
    return titles


def want_to_read(olusr):
    response = requests.get(f"https://openlibrary.org/people/{olusr}/books/want-to-read.json")
    json_response = response.json()
    titles = []
    for work in json_response['reading_log_entries']:
        titles.append(work['work']['title'])
    return titles



def already_read(olusr):
    response = requests.get(f"https://openlibrary.org/people/{olusr}/books/already-read.json")
    json_response = response.json()
    titles = []
    for work in json_response['reading_log_entries']:
        titles.append(work['work']['title'])
    return titles

titles = ['The Great Gatsby', 'To Kill a Mockingbird', 'Learning Python']

def olai(titles):
    check = True
    prompt = ''
    for title in titles:
        prompt = prompt + title + ', '
    
    prompt = prompt + 'suggest more books for me to read based on these books'
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

if __name__ == '__main__':
    print(olai(titles))
