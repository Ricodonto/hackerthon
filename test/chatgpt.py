import os
from dotenv import load_dotenv
load_dotenv('.env')

import openai

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
                messages=[
                    {"role": "user", "content": prompt}])
            message.append(completion.choices[0].message.content)
    return message[0]

if __name__ == '__main__':
    print(ai("how are you?"))