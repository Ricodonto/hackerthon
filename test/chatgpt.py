import os
from dotenv import load_dotenv
load_dotenv('.env')
def ai(prompt):
    m = prompt 
    messages = [{"title":"SQL Cookbook", "Author":"Anthony Molinaro","isbn":"0596009763", "reviews":"4.4/5", "description":"This book offers a collection of practical recipes for solving various SQL problems and challenges. It covers a wide range of topics, including database design, querying data, optimizing performance, and troubleshooting common issues"},
                {"title":"SQL Cookbook", "Author":"Anthony Molinaro","isbn":"0596009763", "reviews":"4.4/5", "description":"This book offers a collection of practical recipes for solving various SQL problems and challenges. It covers a wide range of topics, including database design, querying data, optimizing performance, and troubleshooting common issues"},
                {"title":"SQL Cookbook", "Author":"Anthony Molinaro","isbn":"0596009763", "reviews":"4.4/5", "description":"This book offers a collection of practical recipes for solving various SQL problems and challenges. It covers a wide range of topics, including database design, querying data, optimizing performance, and troubleshooting common issues"}]
    return messages

if __name__ == '__main__':
    print(ai("how are you?"))