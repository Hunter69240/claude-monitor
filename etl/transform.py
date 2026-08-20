import pandas as pd
import time

year=time.localtime().tm_year
def transform(records):
    df=pd.DataFrame.from_dict(records)
    df=df[['email_id','model','timestamp','status','incident_id']]

    #Convert timestamp from str to timestamp type
    df['timestamp']=df['timestamp'].str.replace(",",f" {year}",n=1)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    print(df)