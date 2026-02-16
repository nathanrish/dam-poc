try:
    from task_queue import enqueue_asset_processing
    print("Success")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
