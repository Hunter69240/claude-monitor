import pandas as pd
import time

year=time.localtime().tm_year
def transform(records):
    df=pd.DataFrame.from_dict(records)
    df=df[['email_id','model','occurred_at','status','incident_id']]

    #Convert timestamp from str to timestamp type
    df['occurred_at']=df['occurred_at'].str.replace(",",f" {year}",n=1)
    df['occurred_at'] = pd.to_datetime(df['occurred_at'])

    #split models array into multiple rows
    df=df.explode('model',ignore_index=True)

    #Convert email_id from bytes to integer by converting from byte to str and then to int
    df['email_id']=df['email_id'].str.decode("utf-8").astype(int)

    #Replace empty status to NA for querying
    df['status']=df['status'].replace('',pd.NA,regex=True)

    df['slug'] = (df['email_id'].astype(str) + df['model'].astype(str)).where(
    df['model'].notna(),
    df['email_id'].astype(str))
    
    return df