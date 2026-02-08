from rq import SimpleWorker
from src.queue.request_queue import redis_conn

listen = ["llm_requests"]

if __name__ == "__main__":
    worker = SimpleWorker(listen, connection=redis_conn)
    worker.work()







# from rq import Worker
# from src.queue.request_queue import redis_conn

# listen = ["llm_requests"]

# if __name__ == "__main__":
#     worker = Worker(listen, connection=redis_conn)
#     worker.work()
