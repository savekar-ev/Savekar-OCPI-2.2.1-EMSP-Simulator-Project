from fastapi import APIRouter
from app.config import config

router = APIRouter()

@router.get("/ocpi/versions")
async def get_versions():
    # Return available versions
    return {
        "status_code": 1000,
        "status_message": "Success",
        "timestamp": "2026-01-01T00:00:00Z", # In real app, use datetime.utcnow()
        "data": [
            {
                "version": "2.2.1",
                "url": f"http://{config._config.get('host', '127.0.0.1')}:{config._config.get('port', 8000)}/ocpi/emsp/2.2.1"
            }
        ]
    }

@router.get("/ocpi/emsp/2.2.1")
async def get_version_details():
    base_url = f"http://{config._config.get('host', '127.0.0.1')}:{config._config.get('port', 8000)}/ocpi/emsp/2.2.1"
    
    return {
        "status_code": 1000,
        "status_message": "Success",
        "timestamp": "2026-01-01T00:00:00Z",
        "data": {
            "version": "2.2.1",
            "endpoints": [
                {
                    "identifier": "credentials",
                    "role": "SENDER",
                    "url": f"{base_url}/credentials"
                },
                {
                    "identifier": "locations",
                    "role": "RECEIVER",
                    "url": f"{base_url}/locations"
                },
                {
                    "identifier": "cdrs",
                    "role": "RECEIVER",
                    "url": f"{base_url}/cdrs"
                }
            ]
        }
    }
