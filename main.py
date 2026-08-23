from app.email.fetch import fetch_emails
from etl.transform import transform
from etl.loader import loader

res = fetch_emails()
dataframe = transform(res)



print("Total rows:", len(dataframe))
print("Unique slugs:", dataframe['slug'].nunique())

# loader(dataframe)