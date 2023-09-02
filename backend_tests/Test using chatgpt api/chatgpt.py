import openai
from api import api_key

openai.api_key = api_key

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Give me 3 ideas for apps I could build with openai apis "}])
resp = completion.choices[0].message.content
print(resp)