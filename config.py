"""
Configuration management for Augur Seller Scoring Application
Supports both environment variables and TOML configuration files
"""

import os
import toml
from typing import Optional, Dict, Any

class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self._config = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from TOML file if available, otherwise use environment variables"""
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self._config = toml.load(f)
            except Exception as e:
                print(f"Warning: Could not load TOML config file: {e}")
                self._config = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with TOML taking priority"""
        # First try TOML config
        if self._config:
            keys = key.split('.')
            value = self._config
            try:
                for k in keys:
                    value = value[k]
                if value is not None:
                    return value
            except (KeyError, TypeError):
                pass
        
        # Fallback to environment variable
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
        
        return default
    
    @property
    def db_user(self) -> str:
        return self.get('database.user', 'Augur_App')
    
    @property
    def db_password(self) -> str:
        return self.get('database.password', '')
    
    @property
    def db_host(self) -> str:
        return self.get('database.host', 'localhost')
    
    @property
    def db_name(self) -> str:
        return self.get('database.name', 'augur')
    
    @property
    def db_port(self) -> str:
        return self.get('database.port', '5432')
    
    @property
    def streamlit_server_port(self) -> int:
        return int(self.get('application.streamlit_server_port', '8501'))
    
    @property
    def streamlit_server_address(self) -> str:
        return self.get('application.streamlit_server_address', '0.0.0.0')
    
    @property
    def default_tenure_weight(self) -> float:
        return float(self.get('scoring.default_tenure_weight', '0.3'))
    
    @property
    def default_equity_weight(self) -> float:
        return float(self.get('scoring.default_equity_weight', '0.25'))
    
    @property
    def default_legal_weight(self) -> float:
        return float(self.get('scoring.default_legal_weight', '0.2'))
    
    @property
    def default_permit_weight(self) -> float:
        return float(self.get('scoring.default_permit_weight', '0.15'))
    
    @property
    def default_listing_weight(self) -> float:
        return float(self.get('scoring.default_listing_weight', '0.1'))
    
    @property
    def time_decay_half_life_days(self) -> int:
        return int(self.get('time_decay.half_life_days', '90'))
    
    @property
    def optuna_n_trials(self) -> int:
        return int(self.get('optuna.n_trials', '200'))
    
    @property
    def optuna_timeout_seconds(self) -> int:
        return int(self.get('optuna.timeout_seconds', '3600'))
    
    @property
    def top_k_default(self) -> int:
        return int(self.get('export.top_k_default', '100'))
    
    @property
    def ghl_export_format(self) -> str:
        return self.get('export.ghl_export_format', 'ghl_csv')
    
    def get_database_url(self) -> str:
        """Get the complete database URL"""
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

# Global config instance
config = Config('config.toml')
