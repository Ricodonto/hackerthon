import os
from dotenv import load_dotenv
load_dotenv(".env")


import openai

def ai(prompt):
    check = True
    while check == True:
        message = []
        if len(message) == 0:
            check = False
            ###  REMOVE THE API KEY FROM HERE!
            openai.api_key = "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"

            # Make the gpt ask the user questions on what on they want
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            message.append(completion.choices[0].message.content)
    return message[0]

if __name__ == '__main__':
    print(ai("how are you?"))