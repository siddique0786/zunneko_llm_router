import json
import numpy as np
from redis import Redis
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

redis_client = Redis(host="localhost", port=6379, decode_responses=True)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

SEMANTIC_THRESHOLD = 0.75


class CacheManager:

    def get_exact(self, prompt: str):
        return redis_client.get(f"exact:{prompt}")

    def set_exact(self, prompt: str, response: str):
        redis_client.set(f"exact:{prompt}", response, ex=3600)

    # -------- Semantic Cache -------- #

    def store_semantic(self, prompt: str, response: str):
        embedding = model.encode(prompt).tolist()

        data = {
            "prompt": prompt,
            "embedding": embedding,
            "response": response
        }

        redis_client.rpush("semantic_cache", json.dumps(data))

    def search_semantic(self, prompt: str):

        cached_items = redis_client.lrange("semantic_cache", 0, -1)

        if not cached_items:
            return None

        query_embedding = model.encode(prompt)

        for item in cached_items:
            data = json.loads(item)

            stored_embedding = np.array(data["embedding"]).reshape(1, -1)
            similarity = cosine_similarity(
                [query_embedding], stored_embedding
            )[0][0]

            
        print(f"[Cache] Semantic similarity score: {similarity}")

        if similarity > SEMANTIC_THRESHOLD:
            print("[Cache] Semantic cache hit")
            return data["response"]

        return None
