import logging
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S UTC",
)
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S UTC",
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S UTC",
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# # Create a console handler and set its level to WARNING
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.WARNING)

# # Create a formatter and add it to the handler
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# console_handler.setFormatter(formatter)


def d(i: int) -> None:
    """debug"""
    log.info("***" + str(i) + "***")


def current_utc_date_int() -> int:
    return int(datetime.now(timezone.utc).timestamp())
