try:
    from queue import enqueue_asset_processing
    print("Success")
except ImportError:
    print("ImportError")
except AttributeError:
    print("AttributeError") # This means imported stdlib queue which lacks enqueue_asset_processing
except Exception as e:
    print(f"Error: {e}")
