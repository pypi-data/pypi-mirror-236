import time
import logging
from commutauto.exceptions import RetryException

logger = logging.getLogger(__name__)

def exponential_backoff(max_retries=5, base_delay=1, max_delay=16):
    def decorator(func):
        def retry_func(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warn(e)
                    print(f"Attempt {retries + 1}/{max_retries} - {e}")
                    retries += 1
                    delay = min(base_delay * (2 ** retries), max_delay)
                    time.sleep(delay)
            raise RetryException("Exponential backoff max retries exceeded")
        return retry_func
    return decorator

def retry_handling_decorator(func):
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RetryException as e:
            logger.warn(e)
        return None
    return decorator
