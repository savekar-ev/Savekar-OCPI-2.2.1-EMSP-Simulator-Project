
import sys
import requests
import yaml

def load_config():
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config.yaml: {e}")
        return {}

def main():
    if len(sys.argv) < 2:
        print("Usage: python stop_session.py <session_id>")
        print("Example: python stop_session.py 12345")
        return

    session_id = sys.argv[1]
    
    config = load_config()
    port = config.get("port", 8000)
    host = config.get("host", "127.0.0.1")
    
    # The UI endpoint that triggers the CPO client stop_session
    url = f"http://{host}:{port}/ui/actions/sessions/stop"
    
    print(f"Connecting to simulator at {url}...")
    
    try:
        response = requests.post(url, json={"session_id": session_id})
        if response.status_code == 200:
            print("Response:", response.json())
        else:
            print(f"Error: Received status code {response.status_code}")
            print("Body:", response.text)
    except Exception as e:
        print(f"Failed to connect to simulator: {e}")
        print("Make sure the simulator is running (python run.py)")

if __name__ == "__main__":
    main()
