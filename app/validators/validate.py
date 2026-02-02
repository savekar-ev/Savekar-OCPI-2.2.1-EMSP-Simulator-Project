import json
import os
import logging
from jsonschema import validate, ValidationError, FormatChecker

logger = logging.getLogger("ocpi-validator")

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "json_schemas")

def load_schema(schema_name: str):
    path = os.path.join(SCHEMA_DIR, f"{schema_name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Schema {schema_name} not found at {path}")
    with open(path, "r") as f:
        return json.load(f)

def validate_payload(payload: dict, schema_name: str):
    """
    Validates a payload against a named schema.
    Returns: (is_valid, error_list)
    """
    try:
        schema = load_schema(schema_name)
        validate(instance=payload, schema=schema, format_checker=FormatChecker())
        return True, []
    except ValidationError as e:
        logger.error(f"Schema Validation Failed: {e.message}")
        # Build a readable error path
        path = ".".join([str(p) for p in e.path])
        error_msg = f"Field '{path}': {e.message}"
        return False, [error_msg]
    except Exception as e:
        logger.error(f"Validation Error: {str(e)}")
        return False, [str(e)]
