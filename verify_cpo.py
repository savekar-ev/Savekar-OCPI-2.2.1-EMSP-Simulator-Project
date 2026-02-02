from app.client.cpo_client import cpo_client
from app.config import config
import time

def run_validation():
    print("===== OCPI TEST SUMMARY =====")
    
    # 1. Credentials
    print("Credentials Handshake: ", end="", flush=True)
    try:
        success = cpo_client.post_credentials()
        print("PASS" if success else "FAIL")
    except Exception:
        print("ERROR")

    # 2. Get Locations
    print("GET Locations: ", end="", flush=True)
    try:
        locs = cpo_client.get_locations()
        if locs is not None:
            print(f"PASS ({len(locs)} items)")
        else:
            print("FAIL")
    except Exception:
        print("ERROR")

    # 3. Session Start
    print("POST Session: ", end="", flush=True)
    # Just a dry run with dummy data if not configured
    print("SKIPPED (Requires specific Loc/EVSE)")
    
    # 4. Session Stop
    print("PATCH Session: ", end="", flush=True)
    print("SKIPPED")
    
    print("POST CDR: NOT RUN (Listener only)")
    print("============================")
    
    if config.logging_config.get("log_to_file"):
        print(f"Detailed logs available at: {config.logging_config.get('file_path')}")

if __name__ == "__main__":
    run_validation()
