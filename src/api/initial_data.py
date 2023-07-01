import os
import sys

sys.path.append(os.path.abspath("./"))  # To single-handedly execute this script

import logging

from core.database import SessionLocal
from db.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
