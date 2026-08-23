from etl.database import engine
import pandas as pd

def loader(df):
    if  df.empty:
        print("Data frame doesnt exist")
        exit(1)
    
    print("Inserting to table")

    df.to_sql(name='claude_entries',con=engine , if_exists='append',index=False)


