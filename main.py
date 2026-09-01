import logging
import time
from app.email.fetch import fetch_emails
from etl.transform import transform
from etl.loader import loader
from etl.database import fetch_max_id

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


logger.info("Starting pipeline")

while True:
    try:
        maximum_email_id=fetch_max_id()
        res = fetch_emails(maximum_email_id)
        if not res:
            logger.info("No New records")
        else:
            dataframe = transform(res)
            loader(dataframe)
            logger.info("Pipeline completed")
    except Exception as e :
        logger.error("Exception in main : \n")
        logger.error(e)
    finally:
        logger.info("Going to sleep at : %s",time.strftime("%H:%M:%S"))
        time.sleep(3600)


