import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from main.core.logging import logger
from main.db.session import SessionLocal

max_tries = 60 * 2  # 2 minutes
wait_seconds = 5


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    db = SessionLocal()
    try:
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
