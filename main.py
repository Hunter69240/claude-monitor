from app.email.fetch import fetch_emails
from etl.transform import transform

res=fetch_emails()
dataframe=transform(res)
# print(len(res))