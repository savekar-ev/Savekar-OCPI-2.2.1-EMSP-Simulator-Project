from app.client.cpo_client import cpo_client
cpo_client.post_credentials()

from app.client.cpo_client import cpo_client

cpo_client.start_session(
    location_id="1",
    evse_uid="5",
    token_uid="TEST_USER_001",
)

from app.client.cpo_client import cpo_client
# 1. Fetch ALL Tariffs
# GET /ocpi/cpo/2.2.1/tariffs
tariffs = cpo_client.get_tariffs()
print(f"Tariffs: {tariffs}")

tariff = cpo_client.get_tariff("2")
print(f"Tariff: {tariff}")
