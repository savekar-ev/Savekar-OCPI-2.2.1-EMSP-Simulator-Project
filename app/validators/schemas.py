from typing import List, Optional, Any
from pydantic import BaseModel, Field

# Common
class DisplayText(BaseModel):
    language: str
    text: str

class BusinessDetails(BaseModel):
    name: str
    website: Optional[str] = None
    logo: Optional[dict] = None

class Role(BaseModel):
    role: str
    party_id: str
    country_code: str
    business_details: BusinessDetails

# Credentials
class Credentials(BaseModel):
    token: str
    url: str
    roles: List[Role]

# Version
class Version(BaseModel):
    version: str
    url: str

class VersionDetails(BaseModel):
    version: str
    endpoints: List[dict]

# Location / EVSE / Connector (Simplified for internal usage)
class Connector(BaseModel):
    id: str
    standard: str
    format: str
    power_type: str
    max_voltage: int
    max_amperage: int
    last_updated: str

class EVSE(BaseModel):
    uid: str
    status: str
    connectors: List[Connector]
    last_updated: str

class Location(BaseModel):
    country_code: str
    party_id: str
    id: str
    publish: bool
    evses: List[EVSE]
    last_updated: str

# Session
class Session(BaseModel):
    country_code: str
    party_id: str
    id: str
    start_date_time: str
    end_date_time: Optional[str] = None
    kwh: float
    cdr_token: dict
    auth_method: str
    location_id: str
    evse_uid: str
    status: str
    last_updated: str
    currency: str
    total_cost: Optional[dict] = None

# CDR
class CDR(BaseModel):
    country_code: str
    party_id: str
    id: str
    start_date_time: str
    end_date_time: str
    cdr_token: dict
    auth_method: str
    location_id: str
    evse_uid: str
    currency: str
    tariffs: Optional[List[dict]] = None
    charging_periods: List[dict]
    total_cost: dict
    total_energy: float
    total_time: float
    last_updated: str
