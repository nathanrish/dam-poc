import redis
import json
import sys

def main():
    print("Worker started. Listening on 'media_jobs'...")
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        while True:
            # blpop blocks until an item is available
            # returns a tuple (queue_name, data)
            queue, message = r.blpop('media_jobs')
            
            if message:
                try:
                    job_data = json.loads(message)
                    print(f"Received job: {job_data}")
                except json.JSONDecodeError:
                    print(f"Received non-JSON message: {message}")
                    
    except KeyboardInterrupt:
        print("\nWorker stopped.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
