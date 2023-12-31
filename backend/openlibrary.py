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


def olai(titles):
    print(1)
    check = True
    prompt = ''
    for title in titles:
        prompt = prompt + title + ', '
    
    print(2)
    prompt = prompt + 'suggest more books for me to read based all of these books'
    while check == True:
        message = []
        if len(message) == 0:
            check = False
            openai.api_key = os.getenv("OPENAI_API_KEY")

            print(3)
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.8,
                messages=[
                    {"role":"system", "content":"give me the title, isbn, description, author and ratings for each recommendation and use colons"},
                    # {"role":"system", "content":"only contain the title, isbn, description, author, and ratings for each book and use colons"},
                    {"role": "user", "content": prompt}
                ]
            )
            print(4)
            message.append(completion.choices[0].message.content)
    
    # Generating a file that contains GPT-3.5 Turbo's formatted results labeled response.txt
    print(5)
    file = open("response.txt", "w")
    file.write(message[0])
    file.close()
    print(6)

if __name__ == '__main__':
    usr = 'rollingstones1010'
    try:
        print(currently_reading(usr))
    except KeyError:
        print('Enter an existing OpenLibrary Account')
    # titles = want_to_read(usr)
    # print(olai(titles))
