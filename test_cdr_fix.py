import requests
import datetime

def test_cdr_schema_fix():
    url = "http://127.0.0.1:8000/ocpi/emsp/2.2.1/cdrs"
    # Note: Authorization might be needed depending on middleware, but we'll try without or with dummy
    headers = {"Authorization": "Token TEST_TOKEN", "Content-Type": "application/json"}
    
    # Valid payload according to NEW schema (auth_id, no cdr_token)
    payload_valid = {
        "country_code": "US",
        "party_id": "EXA",
        "id": "CDR_TEST_001",
        "start_date_time": "2023-10-27T10:00:00Z",
        "end_date_time": "2023-10-27T11:00:00Z",
        "auth_id": "AUTH_001",         # NEW FIELD
        "auth_method": "AUTH_REQUEST",
        "currency": "USD",
        "total_cost": 1.11,
        "total_energy": 15.5,
        "total_time": 60.0
    }

    print("Sending Valid CDR (New Schema)...")
    try:
        resp = requests.post(url, json=payload_valid, headers=headers)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        if resp.status_code == 200:
             print("SUCCESS: Valid CDR accepted.")
        else:
             print("FAILURE: Valid CDR rejected.")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_cdr_schema_fix()
