import yaml
import os

class Config:
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        try:
            with open("config.yaml", "r") as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config.yaml: {e}")
            self._config = {}

    @property
    def bootstrap_token(self):
        return self._config.get("bootstrap_token")

    @property
    def cpo_url(self):
        return self._config.get("cpo_url")

    @property
    def validation_error_http_status(self):
        return self._config.get("validation_error_http_status", 400)
    
    @property
    def environment(self):
        return self._config.get("environment", "local")

    @property
    def logging_config(self):
        return self._config.get("logging", {})

    @property
    def business_details(self):
        return self._config.get("business_details", {})
    
    # These might be overwritten by state if dynamic exchange happens,
    # but initially loaded from config.
    @property
    def initial_emsp_token_to_cpo(self):
        return self._config.get("emsp_token_to_cpo")

    @property
    def initial_cpo_token_to_emsp(self):
        return self._config.get("cpo_token_to_emsp")

# Global instance
config = Config()
