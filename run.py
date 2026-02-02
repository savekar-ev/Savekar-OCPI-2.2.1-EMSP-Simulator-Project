import uvicorn
import yaml
import os

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    config = load_config()
    uvicorn.run(
        "app.main:app",
        host=config.get("host", "127.0.0.1"),
        port=config.get("port", 8000),
        reload=True,
        log_level=config.get("log_level", "info")
    )
