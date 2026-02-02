from fastapi.testclient import TestClient
from app.main import app
from app.config import config
from app.state import state
import unittest
from unittest.mock import patch, MagicMock

client = TestClient(app)

class TestCredentials(unittest.TestCase):
    
    def setUp(self):
        # Reset state
        state.cpo_token_to_emsp = config.initial_cpo_token_to_emsp
        state.emsp_token_to_cpo = config.initial_emsp_token_to_cpo

    def test_get_versions(self):
        response = client.get("/ocpi/versions")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status_code"], 1000)
        self.assertTrue(len(data["data"]) > 0)
        self.assertEqual(data["data"][0]["version"], "2.2.1")

    def test_post_credentials_server(self):
        # CPO calls US
        payload = {
            "token": "NEW-CPO-TOKEN-123", # Token they use to call us? No, token we use to call them.
            "url": "http://cpo.example.com",
            "roles": [{
                "role": "CPO",
                "party_id": "CPO",
                "country_code": "US",
                "business_details": {"name": "Test CPO"}
            }]
        }
        headers = {"Authorization": f"Token {config.bootstrap_token}"}
        
        response = client.post("/ocpi/emsp/2.2.1/credentials", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status_code"], 1000)
        self.assertIn("token", data["data"])
        
        # Verify state updated
        self.assertEqual(state.emsp_token_to_cpo, "NEW-CPO-TOKEN-123")

    @patch('app.client.cpo_client.requests.post')
    def test_post_credentials_client(self, mock_post):
        from app.client.cpo_client import cpo_client
        
        # Mock CPO response
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "status_code": 1000,
            "data": {
                "token": "TOKEN-FROM-CPO-FOR-EMSP",
                "url": "...",
                "roles": []
            },
            "timestamp": "..."
        }
        mock_post.return_value = mock_resp
        
        success = cpo_client.post_credentials()
        self.assertTrue(success)
        self.assertEqual(state.emsp_token_to_cpo, "TOKEN-FROM-CPO-FOR-EMSP")
        
        # Verify call args to ensure bootstrap token was used
        call_args = mock_post.call_args
        headers = call_args[1]['headers']
        self.assertEqual(headers['Authorization'], f"Token {config.bootstrap_token}")

if __name__ == '__main__':
    unittest.main()
