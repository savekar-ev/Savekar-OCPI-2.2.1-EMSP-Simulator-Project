from fastapi.testclient import TestClient
from app.main import app
from app.state import state
import unittest
from unittest.mock import patch

client = TestClient(app)

class TestLocations(unittest.TestCase):
    
    def test_patch_location_evse(self):
        # CPO pushes EVSE update
        location_id = "LOC1"
        evse_uid = "EVSE1"
        
        payload = {
            "uid": evse_uid,
            "status": "CHARGING",
            "connectors": [{
                "id": "1",
                "standard": "IEC_62196_T2",
                "format": "CABLE",
                "power_type": "AC_3_PHASE",
                "max_voltage": 400,
                "max_amperage": 32,
                "last_updated": "2026-01-01T12:00:00Z"
            }],
            "last_updated": "2026-01-01T12:00:00Z"
        }
        
        response = client.patch(f"/ocpi/emsp/2.2.1/locations/{location_id}/{evse_uid}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status_code"], 1000)
        
        # Check state
        self.assertIn(location_id, state.locations)
        self.assertIn(evse_uid, state.locations[location_id]["evses"])
        self.assertEqual(state.locations[location_id]["evses"][evse_uid]["status"], "CHARGING")

    def test_patch_location_evse_invalid(self):
        # Invalid status enum
        location_id = "LOC1"
        evse_uid = "EVSE1"
        
        payload = {
            "uid": evse_uid,
            "status": "INVALID_STATUS", # Error
            "connectors": [],
            "last_updated": "2026-01-01T12:00:00Z"
        }
        
        response = client.patch(f"/ocpi/emsp/2.2.1/locations/{location_id}/{evse_uid}", json=payload)
        # Should return strict error HTTP 400
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertNotEqual(data["status_code"], 1000)
        self.assertIn("Schema validation failed", data["status_message"])

if __name__ == '__main__':
    unittest.main()
