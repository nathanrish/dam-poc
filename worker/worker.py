import sys
import os
import json
import time
import redis

# Add backend directory to path to import db and models
# Assuming worker/ is one level down from root, and backend/ is also one level down from root
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from db import SessionLocal
from models import Asset

def process_asset(asset_id):
    """
    Simulate asset processing and update status to READY.
    """
    print(f"Processing asset: {asset_id}")
    # Simulate work
    time.sleep(5) 
    
    try:
        db = SessionLocal()
        # asset_id in Redis might be string, UUID in DB
        # SQLAlchemy handles string-to-UUID conversion usually if strictly typed, but good to be careful.
        # However, payload comes from JSON as string.
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if asset:
            asset.status = "READY"
            db.commit()
            print(f"Asset {asset_id} status updated to READY.")
        else:
            print(f"Asset {asset_id} not found in database.")
        db.close()
    except Exception as e:
        print(f"Error updating asset status: {e}")

    print(f"Finished processing asset: {asset_id}")

def main():
    print("Worker started. Listening on 'asset_processing_queue'...")
    try:
        # Connect to Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        while True:
            # blpop blocks until an item is available
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
