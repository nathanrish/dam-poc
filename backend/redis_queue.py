import os
import redis
import json

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Initialize Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def enqueue_asset_processing(asset_id: str):
    """
    Pushes a job to the Redis queue for asset processing.
    """
    job = {
        "asset_id": str(asset_id)
    }
    payload = json.dumps(job)
    redis_client.rpush("asset_processing_queue", payload)
