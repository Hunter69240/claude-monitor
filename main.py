import logging

from app.email.fetch import fetch_emails
from etl.transform import transform
from etl.loader import loader


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


logger.info("Starting pipeline")

res = fetch_emails()
dataframe = transform(res)
loader(dataframe)

logger.info("Pipeline completed")