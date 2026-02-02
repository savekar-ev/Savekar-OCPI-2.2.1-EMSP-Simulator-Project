from .config import config

class State:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        # Tokens
        self.cpo_token_to_emsp = config.initial_cpo_token_to_emsp
        self.emsp_token_to_cpo = config.initial_emsp_token_to_cpo
        
        # Data storage
        self.locations = {}  # location_id -> Location object
        self.sessions = {}   # session_id -> Session object
        self.cdrs = {}       # cdr_id -> CDR object
        
        # Validation status tracking (for testing verification)
        self.validation_failures = []

        # Dynamic Config from UI
        self.cpo_url = config.cpo_url
        self.bootstrap_token = config.bootstrap_token

    def set_tokens(self, cpo_token: str, emsp_token: str):
        self.cpo_token_to_emsp = cpo_token
        self.emsp_token_to_cpo = emsp_token

state = State()
