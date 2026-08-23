from sqlalchemy.dialects.postgresql import insert
from etl.database import engine
import logging
logger = logging.getLogger(__name__)
def insert_on_conflict_nothing(table, conn, keys, data_iter):
    
    data = [dict(zip(keys, row)) for row in data_iter]
   
    stmt = insert(table.table).values(data)

    stmt = stmt.on_conflict_do_nothing(index_elements=['slug']) 

    conn.execute(stmt)
    
def loader(df):
    if  df.empty:
        logger.error("DataFrame is empty")
        exit(1)

    logger.info("Inserting %d rows into table", len(df))
    

    df.to_sql(name='claude_entries',con=engine , if_exists='append',index=False , method=insert_on_conflict_nothing)
    logger.info("Finished inserting rows")

