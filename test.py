import pandas as pd

df = pd.DataFrame({
    "email_id": [b"24592", b"24598", b"24602", b"24609"],
    "model": [[], ["Opus 4.6"], ["Opus 4.6", "Sonnet 4.6"], ["Opus 4.6"]],
    "status": ["", "", "Identified", "Monitoring"]
})

print(df)
print(df.dtypes)

print("AFTER")

df['email_id']=df['email_id'].str.decode("utf-8")
df['email_id']=df['email_id'].astype(int)
print(df.dtypes)