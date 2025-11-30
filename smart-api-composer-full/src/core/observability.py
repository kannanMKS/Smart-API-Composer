import logging
import time
from contextlib import contextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger("smart_api_composer")

@contextmanager
def timed_span(name: str):
    start = time.time()
    logger.info(f"START {name}")
    try:
        yield
    finally:
        duration = (time.time() - start) * 1000
        logger.info(f"END {name} ({duration:.1f} ms)")
