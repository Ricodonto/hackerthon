import openai

def ai(p):
    pp = [p]
    message = [{"title":"Eloquent JavaScript: A Modern Introduction to Programming", "author":"Marijn Haverbeke", "isbn":"9781593275846", "rating":"4.5/5" },
     {"title":"Eloquent JavaScript: A Modern Introduction to Programming", "author":"Marijn Haverbeke", "isbn":"9781593275846", "rating":"4.5/5" },
     {"title":"Eloquent JavaScript: A Modern Introduction to Programming", "author":"Marijn Haverbeke", "isbn":"9781593275846", "rating":"4.5/5" },
     ]
    
    return message
if __name__ == '__main__':
    print(ai("how are you?"))