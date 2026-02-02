from fastapi import APIRouter, Request, Path, Body, HTTPException
from fastapi.responses import JSONResponse
from app.state import state
from datetime import datetime
from app.log_utils import get_logger
from app.config import config

logger = get_logger("ocpi-sessions")
router = APIRouter()

ALLOWED_PATCH_FIELDS = {"status", "kwh", "end_datetime", "last_updated"}

@router.get("/ocpi/emsp/2.2.1/sessions/{session_id}")
async def get_session(
    session_id: str = Path(..., max_length=36)
):
    """
    Get session details (Debug/Optional).
    """
    logger.info(f"GET Session request", direction="CPO->EMSP", module="sessions", context=f"SessionID={session_id}")
    
    if session_id in state.sessions:
        return {
            "status_code": 1000,
            "status_message": "Success",
            "timestamp": datetime.utcnow().isoformat(),
            "data": state.sessions[session_id]
        }
    else:
        # OCPI compliant 404 for objects usually returns 200 OK with custom status code or fails.
        # But standard HTTP 404 is often accepted for missing resources. 
        # For OCPI, it's often better to return success with encoded error or just 200 OK with empty data?
        # Standard HTTP 404 is commonly used for "Device/Object not found".
        return JSONResponse(
            status_code=404,
            content={
                "status_code": 2003,
                "status_message": "Session not found",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@router.patch("/ocpi/emsp/2.2.1/sessions/{session_id}")
async def patch_session(
    request: Request,
    session_id: str = Path(..., max_length=36)
):
    """
    Receive session updates from CPO.
    """
    try:
        payload = await request.json()
    except Exception:
         return JSONResponse(
             status_code=config.validation_error_http_status,
             content={
                 "status_code": 2001,
                 "status_message": "Invalid JSON",
                 "timestamp": datetime.utcnow().isoformat()
            }
        )

    # Payload Guard
    filtered_payload = {k: v for k, v in payload.items() if k in ALLOWED_PATCH_FIELDS}
    ignored_fields = [k for k in payload.keys() if k not in ALLOWED_PATCH_FIELDS]
    
    if ignored_fields:
        logger.warning(f"Ignored fields in PATCH", direction="CPO->EMSP", module="sessions", context=f"Ignored={ignored_fields}")

    # Create or Update Session in State
    if session_id not in state.sessions:
        state.sessions[session_id] = {"id": session_id}
        logger.info(f"New Session Created via PATCH", direction="CPO->EMSP", module="sessions", context=f"SessionID={session_id}")

    state.sessions[session_id].update(filtered_payload)
    
    current_status = state.sessions[session_id].get("status", "UNKNOWN")
    logger.info(f"Session {session_id} updated", direction="CPO->EMSP", module="sessions", context=f"status={current_status}")

    return {
        "status_code": 1000,
        "status_message": "Success",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {}
    }
