import pandas as pd
import time

df = pd.DataFrame({
    "timestamp": [
        "Mar 27, 11:04 UTC",
        "Mar 27, 11:21 UTC",
        "Mar 27, 12:09 UTC",
        "Mar 28, 13:01 UTC",
        "Mar 31, 21:01 UTC"
    ]
})


year=time.localtime().tm_year

print(df[['timestamp']].dtypes)

df['timestamp']=df['timestamp'].str.replace(",",f" {year}",n=1)


df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date



print(df)
