from fastapi.testclient import TestClient
from app.main import app
from app.state import state
import unittest

client = TestClient(app)

class TestSessionsCDRs(unittest.TestCase):
    
    def test_post_cdr(self):
        payload = {
            "country_code": "US",
            "party_id": "CPO",
            "id": "CDR123",
            "start_date_time": "2026-01-01T12:00:00Z",
            "end_date_time": "2026-01-01T13:00:00Z",
            "cdr_token": {
                "uid": "TOKEN1",
                "type": "RFID",
                "contract_id": "C1"
            },
            "auth_method": "AUTH_REQUEST",
            "currency": "USD",
            "total_cost": {
                "excl_vat": 10.00,
                "incl_vat": 11.00
            },
            "total_energy": 15.5,
            "total_time": 1.0
        }
        
        response = client.post("/ocpi/emsp/2.2.1/cdrs", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status_code"], 1000)
        
        self.assertIn("CDR123", state.cdrs)

if __name__ == '__main__':
    unittest.main()
