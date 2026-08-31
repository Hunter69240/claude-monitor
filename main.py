import logging

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

maximum_email_id=fetch_max_id()
res = fetch_emails(maximum_email_id)
dataframe = transform(res)
loader(dataframe)

logger.info("Pipeline completed")