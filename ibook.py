import pandas as pd

# Load the dataset into a DataFrame
df = pd.read_csv("books.csv")

# Select and keep only the desired columns
df = df[['title', 'authors', 'num_pages', 'isbn']]

# Rename the columns to match your specified names
df = df.rename(columns={'title': 'Title', 'authors': 'Author', 'num_pages': 'Number of Pages', 'isbn': 'ISBN'})

# Save the cleaned dataset to a new CSV file
df.to_csv("cleaned_books.csv", index=False)