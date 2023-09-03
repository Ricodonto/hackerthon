import os
from dotenv import load_dotenv
load_dotenv('.env')
def ai(prompt):
    m = prompt 
    messages = {"title":["SQL Cookbook","SQL Cookbook","SQL Cookbook"], "author":["Anthony Molinaro","Anthony Molinaro","Anthony Molinaro"],
                "isbn":["0596009763","0596009763","0596009763"], "rating":["4.4/5","4.4/5","4.4/5"], 
                "description":["This book offers a collection of practical recipes for solving various SQL problems and challenges. It covers a wide range of topics, including database design, querying data, optimizing performance, and troubleshooting common issues",
                "This book offers a collection of practical recipes for solving various SQL problems and challenges. It covers a wide range of topics, including database design, querying data, optimizing performance, and troubleshooting common issues",
                "This book offers a collection of practical recipes for solving various SQL problems and challenges. It covers a wide range of topics, including database design, querying data, optimizing performance, and troubleshooting common issues"]}
    colnames=["title","author","rating","description"]
    rows = zip(*[messages[c] for c in colnames])
    return dict(rows=rows,colnames=colnames)

if __name__ == '__main__':
    print(ai("how are you?"))