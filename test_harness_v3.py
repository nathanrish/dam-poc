import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def run_tests():
    print("Starting harness v3 simulation...")
    
    # 1. Health
    print("Test: Health endpoint must respond")
    try:
        r = requests.get(f"{BASE_URL}/health")
        if r.status_code != 200:
            print(f"FAIL: Health check failed: {r.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"FAIL: Health check exception: {e}")
        sys.exit(1)
    print("PASS")

    # 2. Create Asset
    print("Test: Create asset")
    r = requests.post(f"{BASE_URL}/assets")
    if r.status_code != 200:
        print(f"FAIL: Create asset failed: {r.status_code} {r.text}")
        sys.exit(1)
    resp = r.json()
    if "asset_id" not in resp:
        print(f"FAIL: 'asset_id' missing in response: {resp}")
        sys.exit(1)
    asset_id = resp["asset_id"]
    print(f"Asset Created: {asset_id}")
    print("PASS")

    # 3. Verify CREATED
    print("Test: Verify asset initial state is CREATED")
    r = requests.get(f"{BASE_URL}/assets/{asset_id}")
    resp = r.json()
    if resp["status"] != "CREATED":
        print(f"FAIL: Status mismatch. Got {resp['status']}, expected CREATED")
        sys.exit(1)
    print("PASS")

    # 4. Upload File
    print("Test: Upload asset file")
    with open("harness_test_file.txt", "wb") as f:
        f.write(b"Harness test content")

    with open("harness_test_file.txt", "rb") as f:
        files = {"file": f}
        r = requests.post(f"{BASE_URL}/assets/{asset_id}/upload", files=files)
        if r.status_code != 200:
            print(f"FAIL: Upload failed: {r.status_code} {r.text}")
            sys.exit(1)
    print("PASS")

    # 5. Verify UPLOADED
    print("Test: Verify state becomes UPLOADED after upload")
    r = requests.get(f"{BASE_URL}/assets/{asset_id}")
    resp = r.json()
    if resp["status"] != "UPLOADED":
        print(f"FAIL: Status mismatch. Got {resp['status']}, expected UPLOADED")
        sys.exit(1)
    print("PASS")

    # 6. Wait for Worker
    print("Test: Wait for worker processing (10s)")
    time.sleep(10)
    print("PASS")

    # 7. Verify READY
    print("Test: Verify asset reaches READY state")
    r = requests.get(f"{BASE_URL}/assets/{asset_id}")
    resp = r.json()
    if resp["status"] != "READY":
        print(f"FAIL: Status mismatch. Got {resp['status']}, expected READY")
        sys.exit(1)
    print("PASS")
    
    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    run_tests()
