import logging
import os
from .config import config

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def error(self, message, direction="INTERNAL", module="SYSTEM", context=None):
        self._log(logging.ERROR, message, direction, module, context)

    def warning(self, message, direction="INTERNAL", module="SYSTEM", context=None):
        self._log(logging.WARNING, message, direction, module, context)

    def info(self, message, direction="INTERNAL", module="SYSTEM", context=None):
        self._log(logging.INFO, message, direction, module, context)
        
    def debug(self, message, direction="INTERNAL", module="SYSTEM", context=None):
        self._log(logging.DEBUG, message, direction, module, context)

    def _log(self, level, message, direction, module, context):
        # Format: [Direction][Module] message {Context}
        prefix = f"[{direction}][{module}]"
        
        # If context is provided (e.g. invalid field path), append it
        if context:
            full_message = f"{prefix} {message} | Context: {context}"
        else:
            full_message = f"{prefix} {message}"
            
        self.logger.log(level, full_message)

def setup_logging():
    log_config = config.logging_config
    log_level_str = config._config.get("log_level", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    handlers = [logging.StreamHandler()]
    
    if log_config.get("log_to_file"):
        file_path = log_config.get("file_path", "logs/emsp-simulator.log")
        # Ensure dir exists
        log_dir = os.path.dirname(file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        handlers.append(logging.FileHandler(file_path))

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers,
        force=True # Reset any existing config
    )

def get_logger(name):
    # Ensure setup is ran once mainly? 
    # Or just return wrapper
    return StructuredLogger(name)
