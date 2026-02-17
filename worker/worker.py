import redis
import json
import sys
import time

def process_asset(asset_id):
    """
    Simulate asset processing.
    In a real application, this would involve image manipulation, video transcoding, etc.
    """
    print(f"Processing asset: {asset_id}")
    # Simulate work
    time.sleep(5) 
    print(f"Finished processing asset: {asset_id}")

def main():
    print("Worker started. Listening on 'asset_processing_queue'...")
    try:
        # Connect to Redis
        # Use localhost for now as directed by existing code, but ideally this should be configurable
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        while True:
            # blpop blocks until an item is available
            # returns a tuple (queue_name, data)
            job = r.blpop('asset_processing_queue')
            
            if job:
                _, message = job
                try:
                    # Parse job JSON
                    job_data = json.loads(message)
                    print(f"Received job: {job_data}")
                    
                    # Extract asset_id
                    asset_id = job_data.get('asset_id')
                    
                    if asset_id:
                        # Call process_asset(asset_id)
                        process_asset(asset_id)
                    else:
                        print("Error: 'asset_id' missing from job data")
                        
                except json.JSONDecodeError:
                    print(f"Received non-JSON message: {message}")
                except Exception as e:
                    print(f"Error processing job: {e}")
                    
    except KeyboardInterrupt:
        print("\nWorker stopped.")
    except Exception as e:
        print(f"Fatal Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
