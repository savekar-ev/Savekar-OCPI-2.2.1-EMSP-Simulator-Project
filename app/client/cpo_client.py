import requests
from app.config import config
from app.state import state
from app.validators.validate import validate_payload
from app.log_utils import get_logger
from typing import Optional, Dict, Any

logger = get_logger("cpo-client")

class CPOClient:
    def __init__(self):
        # We rely on state or specific args for tokens to allow dynamic switching if needed
        pass

    @property
    def headers(self):
        token = state.emsp_token_to_cpo
        if not token:
            logger.warning("No EMSP Token found", direction="EMSP->CPO", module="client")
        return {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }

    def _validate_response(self, response: requests.Response, module: str):
        """
        Validates OCPI response envelop and optionally data schema.
        """
        try:
            data = response.json()
        except Exception:
            logger.error(f"Invalid JSON response", direction="CPO->EMSP", module=module, context=f"Body={response.text[:100]}")
            return False, "Invalid JSON"

        # Check OCPI Envelop
        if "status_code" not in data or "timestamp" not in data:
            logger.error(f"Invalid OCPI Envelop", direction="CPO->EMSP", module=module, context=f"Data={data}")
            return False, "Missing OCPI Envelop fields"

        if data["status_code"] != 1000:
             logger.warning(f"OCPI Error", direction="CPO->EMSP", module=module, context=f"Code={data['status_code']} | Msg={data.get('status_message')}")
             return False, f"OCPI Error {data['status_code']}"

        return True, "OK"

    def get_versions(self):
        url = f"{state.cpo_url}/ocpi/versions"
        try:
            logger.info(f"GET {url}", direction="EMSP->CPO", module="versions")
            res = requests.get(url, headers=self.headers, timeout=10)
            logger.info(f"Response {res.status_code}", direction="CPO->EMSP", module="versions")
            return res.json()
        except Exception as e:
            logger.error(f"Failed to get versions", direction="EMSP->CPO", module="versions", context=str(e))
            return None

    def post_credentials(self):
        url = f"{state.cpo_url}/ocpi/cpo/2.2.1/credentials"
        
        base_url = f"http://{config._config.get('host', '127.0.0.1')}:{config._config.get('port', 8000)}/ocpi/emsp/2.2.1"
        payload = {
            "token": state.cpo_token_to_emsp, # The token they should use
            "url": base_url,
            "roles": [{
                "role": "EMSP",
                "party_id": "EXA",
                "country_code": "US",
                "business_details": config.business_details
            }]
        }
        
        # AUTH FIX: Use bootstrap token for handshake, NOT the standard headers
        bootstrap_headers = {
            "Authorization": f"Token {state.bootstrap_token}",
            "Content-Type": "application/json"
        }
        
        try:
            logger.info(f"POST Credentials", direction="EMSP->CPO", module="credentials", context=f"TokenForCPO={state.cpo_token_to_emsp} | Auth=Bootstrap")
            res = requests.post(url, json=payload, headers=bootstrap_headers, timeout=10)
            
            if res.status_code == 200:
                data = res.json()
                if data.get("status_code") == 1000 and "data" in data:
                    cred_data = data["data"]
                    new_token = cred_data.get("token")
                    if new_token:
                        state.emsp_token_to_cpo = new_token
                        logger.info(f"Handshake successful", direction="CPO->EMSP", module="credentials", context=f"NewToken={new_token[:4]}***")
                    return True
            logger.error(f"Credentials exchange failed", direction="CPO->EMSP", module="credentials", context=f"Status={res.status_code} | Body={res.text}")
            return False
        except Exception as e:
            logger.error(f"Credentials exchange failed", direction="EMSP->CPO", module="credentials", context=str(e))
            return False

    def get_locations(self):
        url = f"{state.cpo_url}/ocpi/cpo/2.2.1/locations"
        try:
            logger.info(f"GET Locations", direction="EMSP->CPO", module="locations")
            res = requests.get(url, headers=self.headers, timeout=10)
            valid, msg = self._validate_response(res, "locations")
            if valid:
                count = len(res.json().get('data', []))
                logger.info(f"Locations fetched", direction="CPO->EMSP", module="locations", context=f"Count={count}")
                return res.json()['data']
            else:
                 return None
        except Exception as e:
            logger.error(f"Failed to get locations", direction="EMSP->CPO", module="locations", context=str(e))
            return None

    def start_session(self, location_id: str, evse_uid: str, token_uid: str):
        url = f"{state.cpo_url}/ocpi/cpo/2.2.1/sessions"
        payload = {
            "location_id": location_id,
            "evse_uid": evse_uid,
        }
        
        logger.warning("Attempting POST /sessions (User specified)", direction="EMSP->CPO", module="sessions")
        
        try:
             res = requests.post(url, json=payload, headers=self.headers, timeout=10)
             logger.info(f"Start Session Response {res.status_code}", direction="CPO->EMSP", module="sessions")
             return res.json()
        except Exception as e:
            logger.error(f"Failed to start session", direction="EMSP->CPO", module="sessions", context=str(e))
            return None

    def stop_session(self, session_id: str):
        # PATCH /sessions/{id}
        url = f"{state.cpo_url}/ocpi/cpo/2.2.1/sessions/{session_id}"
        payload = {"status": "COMPLETED"} # Example
        try:
             res = requests.patch(url, json=payload, headers=self.headers, timeout=10)
             logger.info(f"Stop Session Response {res.status_code}", direction="CPO->EMSP", module="sessions")
             return res.json()
        except Exception as e:
            logger.error(f"Failed to stop session", direction="EMSP->CPO", module="sessions", context=str(e))
            return None

    def get_tariffs(self):
        url = f"{state.cpo_url}/ocpi/cpo/2.2.1/tariffs"
        try:
            logger.info(f"GET {url}", direction="EMSP->CPO", module="tariffs")
            res = requests.get(url, headers=self.headers, timeout=10)
            valid, msg = self._validate_response(res, "tariffs")
            if valid:
                data = res.json().get('data', [])
                count = len(data)
                logger.info(f"Tariffs fetched", direction="CPO->EMSP", module="tariffs", context=f"Count={count}")
                return data
            else:
                 return None
        except Exception as e:
            logger.error(f"Failed to get tariffs", direction="EMSP->CPO", module="tariffs", context=str(e))
            return None

    def get_tariff(self, tariff_id: str):
        url = f"{state.cpo_url}/ocpi/cpo/2.2.1/tariffs/{tariff_id}"
        try:
            logger.info(f"GET {url}", direction="EMSP->CPO", module="tariffs")
            res = requests.get(url, headers=self.headers, timeout=10)
            valid, msg = self._validate_response(res, "tariffs")
            if valid:
                data = res.json().get('data')
                logger.info(f"Tariff fetched", direction="CPO->EMSP", module="tariffs", context=f"TariffID={tariff_id}")
                return data
            else:
                 return None
        except Exception as e:
            logger.error(f"Failed to get tariff", direction="EMSP->CPO", module="tariffs", context=str(e))
            return None

cpo_client = CPOClient()
