import time
import random


class RetryHandler:

    def __init__(self, max_retries=3, base_delay=0.5, max_delay=5):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def execute(self, func, *args, **kwargs):
        """
        Retry wrapper for normal (non-streaming) calls
        """

        last_exception = None

        for attempt in range(1, self.max_retries + 1):

            try:
                return func(*args, **kwargs)

            except Exception as e:
                last_exception = e

                if attempt == self.max_retries:
                    raise e

                delay = self._calculate_delay(attempt)
                print(f"[Retry] Attempt {attempt} failed → retrying in {delay:.2f}s")

                time.sleep(delay)

        raise last_exception

    def _calculate_delay(self, attempt):
        """
        Exponential backoff + jitter
        """
        delay = min(self.base_delay * (2 ** (attempt - 1)), self.max_delay)
        jitter = random.uniform(0, 0.3)

        return delay + jitter
