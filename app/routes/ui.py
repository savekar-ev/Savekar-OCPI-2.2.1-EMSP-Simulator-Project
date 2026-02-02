from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel
from app.state import state
from app.client.cpo_client import cpo_client
from app.log_utils import get_logger

router = APIRouter(prefix="/ui", tags=["UI"])
logger = get_logger("ui-api")

class ConfigUpdate(BaseModel):
    cpo_url: str
    bootstrap_token: str

@router.get("/config")
async def get_config():
    return {
        "cpo_url": state.cpo_url,
        "bootstrap_token": state.bootstrap_token
    }

@router.post("/config")
async def update_config(cfg: ConfigUpdate):
    state.cpo_url = cfg.cpo_url
    state.bootstrap_token = cfg.bootstrap_token
    logger.info(f"UI updated config: CPO_URL={state.cpo_url}", module="ui")
    return {"status": "ok", "message": "Configuration updated"}

@router.post("/actions/credentials")
async def action_credentials():
    logger.info("UI triggers Credentials Exchange", module="ui")
    success = cpo_client.post_credentials()
    if success:
        return {"status": "ok", "message": "Credentials Exchange Successful"}
    else:
        return {"status": "error", "message": "Credentials Exchange Failed. Check logs."}

@router.post("/actions/versions")
async def action_versions():
    logger.info("UI triggers Get Versions", module="ui")
    data = cpo_client.get_versions()
    return {"status": "ok", "data": data}

@router.post("/actions/locations")
async def action_locations():
    logger.info("UI triggers Get Locations", module="ui")
    data = cpo_client.get_locations()
    return {"status": "ok", "data": data}

@router.post("/actions/tariffs")
async def action_tariffs():
    logger.info("UI triggers Get Tariffs", module="ui")
    data = cpo_client.get_tariffs()
    return {"status": "ok", "data": data}

# Simple inputs for session start
class SessionStartInput(BaseModel):
    location_id: str
    evse_uid: str
    token_uid: str

@router.post("/actions/sessions/start")
async def action_start_session(inp: SessionStartInput):
    logger.info(f"UI triggers Start Session loc={inp.location_id} evse={inp.evse_uid}", module="ui")
    data = cpo_client.start_session(inp.location_id, inp.evse_uid, inp.token_uid)
    return {"status": "ok", "data": data}

class SessionStopInput(BaseModel):
    session_id: str

@router.post("/actions/sessions/stop")
async def action_stop_session(inp: SessionStopInput):
    logger.info(f"UI triggers Stop Session session={inp.session_id}", module="ui")
    data = cpo_client.stop_session(inp.session_id)
    return {"status": "ok", "data": data}
