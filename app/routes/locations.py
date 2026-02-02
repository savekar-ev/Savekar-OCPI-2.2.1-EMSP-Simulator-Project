from fastapi import APIRouter, Request, HTTPException, Path, Body
from fastapi.responses import JSONResponse
from app.state import state
from app.validators.validate import validate_payload
from datetime import datetime
from app.log_utils import get_logger

logger = get_logger("ocpi-locations")
router = APIRouter()

from app.config import config

@router.patch("/ocpi/emsp/2.2.1/locations/{location_id}/{evse_uid}")
async def patch_evse(
    request: Request,
    location_id: str = Path(..., max_length=39),
    evse_uid: str = Path(..., max_length=36)
):
    """
    Receive status updates from CPO.
    """
    try:
        payload = await request.json()
    except Exception:
         return {
             "status_code": 2001,
             "status_message": "Invalid JSON",
             "timestamp": datetime.utcnow().isoformat()
        }

    is_valid, errors = validate_payload(payload, "evse_patch")
    
    logger.info(f"Received PATCH payload: {payload}", direction="CPO->EMSP", module="locations", context=f"Path={location_id}/{evse_uid}")

    
    if not is_valid:
        logger.error("Invalid EVSE PATCH payload: connectors not allowed in PATCH", direction="CPO->EMSP", module="locations", context=f"Errors={errors} | Path={location_id}/{evse_uid}")
        return JSONResponse(
            status_code=config.validation_error_http_status,
            content={
                "status_code": 2001,
                "status_message": "Schema validation failed",
                "data": {"errors": errors},
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    # Update State
    if location_id not in state.locations:
        state.locations[location_id] = {"id": location_id, "evses": {}}
    
    if isinstance(state.locations[location_id], dict) and "evses" not in state.locations[location_id]:
        state.locations[location_id]["evses"] = {}
        
    state.locations[location_id]["evses"][evse_uid] = payload
    logger.info(f"Updated EVSE", direction="CPO->EMSP", module="locations", context=f"Path={location_id}/{evse_uid} | Status={payload.get('status')}")

    return {
        "status_code": 1000,
        "status_message": "Success",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {}
    }
