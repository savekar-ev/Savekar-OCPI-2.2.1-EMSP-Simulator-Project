import time
from app.client.cpo_client import cpo_client
from app.state import state
from app.config import config

def test_fetch_tariffs():
    print("Fetching all tariffs...")
    # 1. Configure CPO URL (Must point to valid CPO, NOT this simulator)
    # This URL should point to the CPO implementation you want to test.
    # WARNING: Do NOT use localhost:8000, as that is likely THIS EMSP simulator.
    config._config["cpo_url"] = "http://localhost:3000" 
    
    # 2. Token setup (Simulates result of credentials handshake)
    # In a real scenario, this token is obtained via the credentials exchange.
    # We hardcode it here only for manual testing purposes.
    if not state.emsp_token_to_cpo:
        state.emsp_token_to_cpo = "TEST_TOKEN_CPO" 

    print(f"Targeting CPO: {config.cpo_url}")

    tariffs = cpo_client.get_tariffs()
    if tariffs is not None:
        print(f"Success! Count: {len(tariffs)}")
        for t in tariffs:
             print(f" - ID: {t.get('id')}")
    else:
        print("Failed to fetch tariffs (Check if CPO is running and URL is correct)")

    print("\nFetching specific tariff (TARIFF_AC_1)...")
    tariff = cpo_client.get_tariff("TARIFF_AC_1")
    if tariff:
        print(f"Success! Tariff: {tariff.get('id')}")
    else:
        print("Failed to fetch specific tariff")

if __name__ == "__main__":
    test_fetch_tariffs()
