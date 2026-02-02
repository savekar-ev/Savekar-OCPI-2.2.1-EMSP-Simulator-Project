from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.state import state
from app.validators.validate import validate_payload
from datetime import datetime
from app.log_utils import get_logger

logger = get_logger("ocpi-cdrs")
router = APIRouter()

from app.config import config

@router.post("/ocpi/emsp/2.2.1/cdrs")
async def post_cdr(request: Request):
    """
    Receive CDR from CPO.
    """
    try:
        payload = await request.json()
    except Exception:
         return {
             "status_code": 2001,
             "status_message": "Invalid JSON",
             "timestamp": datetime.utcnow().isoformat()
        }


    is_valid, errors = validate_payload(payload, "cdr")
    
    # DEBUG: Log payload to see what's wrong if validation fails (or always)
    logger.info(f"Incoming CDR Payload: {payload}", direction="CPO->EMSP", module="cdrs")
    
    if not is_valid:
        logger.error("CDR Schema validation failed", direction="CPO->EMSP", module="cdrs", context=f"Errors={errors}")
        return JSONResponse(
            status_code=config.validation_error_http_status,
            content={
                "status_code": 2001,
                "status_message": "Schema validation failed",
                "data": {"errors": errors},
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    cdr_id = payload.get("id")
    state.cdrs[cdr_id] = payload
    logger.info(f"Received Valid CDR {cdr_id}", direction="CPO->EMSP", module="cdrs", context=f"Party={payload.get('party_id')}")
    
    return {
        "status_code": 1000,
        "status_message": "Success",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {}
    }
