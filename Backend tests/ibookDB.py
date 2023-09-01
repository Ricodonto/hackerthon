import panda as pd

#Load the datasetinto a dataframe
df = pd.read_csv("books.csv")

#Set and keep the required columns
df = df[['title', 'authors', 'num_pages', 'isbn']]

#Rename the columns to match your specified names
df = df.rename(columns={'title':'Title','authors':'Authors','num_pages':'Number of pages','isbn':'ISBN'})

df.to_csv("ibookDB.csv",index=False)