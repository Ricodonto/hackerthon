.gitignore - to prevent sensitive data from being pushed to the repository

.github/worflows - contains defined GitHub Action Workflows

/books.csv - dataset of the book details: title, author,ISBN, ISBN-13, language-code, average rating,number of pages,date of publication, publisher from goodreads

/new_books.csv - Modified version of books.csv used to retrieve only the relevant data from it.

/requirements.txt - Used to specify  the exact versions of python packages for our project.

/setUpDatabase.ipynb - Used to load book related data from the csv file, inspects the data and perform data analysis and manipulation.

/tempCodeRunnerFile.python - testing purposes

/tempCodeRunnerFile.python - Sets up a Flask web application with a single route(“/”). When you run the the script it starts a local web server that accesses the homepage.
Generative AI would generate the list of recommended books and their details based on the user’s prompt

/backend/chatgpt.py - It takes the user's prompt and queries the openai api (under the ai() function) it then writes a temporary file called "response.txt" which gives out its messages.
The function cleanup then loads "response.txt" and searches for particular data such as the book title, isbn, rating etc, and returns an easier to work with piece of data"\
This data will be used in the routes.py folder

- It also has the cleanup function that parses through response.txt to format it into an array containing the relevant infromation from the suggestions
- 

/test/routes.py - this is the file that holds the routes of our Service page, where flask would create a web api that would be hosted by a webservice provider

at the landing page, the user would be prompted with a form containing their prompt information that would be sumbmitted to the server (for processing and message generation). forwd_prompt variable is the string that would be submitted to the ai, it has an concatenated string that tells the ai to provide additional information about the books

The forwd prompt is then submitted and the user prompt is stored in a dictionary

The information is then rendered onto a html folder that takes advantage of Jinja

/test/deploy_service.sh - what render runs when building and deploying the flask app

/test/static - contains styling CSS files

/test/forms.py It is the implementation of forms using Flask

/test/templates The folder stores the html pages that would be rendered

/test/templates/about.html It has information about us

/test/templates/base_template.html It has attributes that would be inherited by other html files

/test/templates/book_table.html - This is the html page that would be showed to the user after they submit their prompt, The data at the moment is kept in a table

/test/templates/response.html - Older method of showing the book details to the user

