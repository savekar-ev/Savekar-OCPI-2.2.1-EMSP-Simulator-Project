from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from .config import config
from .routes import versions, credentials, locations, cdrs, sessions, ui
from .log_utils import setup_logging
import logging
import os

# Setup Logging
setup_logging()
logger = logging.getLogger("ocpi-emsp")

app = FastAPI(title="OCPI 2.2.1 EMSP Simulator")

@app.middleware("http")
async def validation_logging_middleware(request: Request, call_next):
    # This middleware can be used/extended to log precise OCPI flows
    # For now, it just wraps and logs request/response roughly
    logger.info(f"Incoming Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    logger.info(f"Response Status: {response.status_code}")
    return response

# Include Routers
app.include_router(versions.router)
app.include_router(credentials.router)
app.include_router(locations.router)
app.include_router(cdrs.router)
app.include_router(sessions.router)
app.include_router(ui.router)

# Mount Static Files
# We expect 'ui' folder to be at the root, same level as 'app' or 'run.py'
static_dir = os.path.join(os.getcwd(), "ui")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    # Serve the UI entry point
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "OCPI 2.2.1 EMSP Simulator is running. UI not found."}
