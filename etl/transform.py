import pandas as pd

def transform(records):
    df=pd.DataFrame.from_dict(records)
    df=df[['email_id','model','timestamp','status','incident_id']]
    print(df.dtypes)