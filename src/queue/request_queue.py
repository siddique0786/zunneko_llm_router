import redis
from rq import Queue
from src.settings import settings

# Redis connection
redis_conn = redis.from_url(settings.REDIS_URL)

# Main queue
request_queue = Queue("llm_requests", connection=redis_conn)
