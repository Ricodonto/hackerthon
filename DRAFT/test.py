import os
from dotenv import load_dotenv
load_dotenv(".env")


import openai

def ai(p):
    pp = [p]
    message = [{"title":"Eloquent JavaScript: A Modern Introduction to Programming", "author":"Marijn Haverbeke", "isbn":"9781593275846", "rating":"4.5/5" },
     {"title":"Eloquent JavaScript: A Modern Introduction to Programming", "author":"Marijn Haverbeke", "isbn":"9781593275846", "rating":"4.5/5" },
     {"title":"Eloquent JavaScript: A Modern Introduction to Programming", "author":"Marijn Haverbeke", "isbn":"9781593275846", "rating":"4.5/5" },
     ]
    old = [{"prompt":"how are you","response": "Fine, would you need a service?"}]
    
    return message
if __name__ == '__main__':
    print(ai("how are you?"))