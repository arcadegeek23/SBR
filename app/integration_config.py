"""
Integration Configuration Manager
Handles storage and retrieval of integration settings
"""
import json
import os
from typing import Dict, Optional
from datetime import datetime

class IntegrationConfig:
    """Manages integration configurations"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or os.path.join(os.path.dirname(__file__), '..', 'config', 'integrations.json')
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        
        # Return default config
        return {
            'halo': {
                'enabled': False,
                'api_url': '',
                'client_id': '',
                'client_secret': '',
                'tenant_id': '',
                'last_sync': None,
                'sync_status': 'never'
            },
            'okta': {
                'enabled': False,
                'domain': '',
                'client_id': '',
                'client_secret': '',
                'redirect_uri': '',
                'issuer': '',
                'authorization_endpoint': '',
                'token_endpoint': '',
                'userinfo_endpoint': ''
            },
            'azure_ai': {
                'enabled': False,
                'endpoint': '',
                'api_key': '',
                'deployment_name': '',
                'api_version': '2024-02-15-preview',
                'model': 'gpt-4',
                'temperature': 0.7,
                'max_tokens': 2000
            },
            'sync_history': []
        }
    
    def _save_config(self) -> bool:
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_halo_config(self) -> Dict:
        """Get HaloPSA configuration"""
        return self.config.get('halo', {})
    
    def set_halo_config(self, config: Dict) -> bool:
        """Set HaloPSA configuration"""
        self.config['halo'].update(config)
        return self._save_config()
    
    def get_okta_config(self) -> Dict:
        """Get Okta configuration"""
        return self.config.get('okta', {})
    
    def set_okta_config(self, config: Dict) -> bool:
        """Set Okta configuration"""
        self.config['okta'].update(config)
        return self._save_config()
    
    def get_azure_ai_config(self) -> Dict:
        """Get Azure AI configuration"""
        return self.config.get('azure_ai', {})
    
    def set_azure_ai_config(self, config: Dict) -> bool:
        """Set Azure AI configuration"""
        self.config['azure_ai'].update(config)
        return self._save_config()
    
    def add_sync_history(self, sync_type: str, status: str, message: str, records_synced: int = 0) -> bool:
        """Add sync history entry"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': sync_type,
            'status': status,
            'message': message,
            'records_synced': records_synced
        }
        
        if 'sync_history' not in self.config:
            self.config['sync_history'] = []
        
        self.config['sync_history'].insert(0, entry)
        
        # Keep only last 50 entries
        self.config['sync_history'] = self.config['sync_history'][:50]
        
        return self._save_config()
    
    def get_sync_history(self, limit: int = 20) -> list:
        """Get sync history"""
        return self.config.get('sync_history', [])[:limit]
    
    def update_last_sync(self, sync_type: str, status: str) -> bool:
        """Update last sync timestamp"""
        if sync_type == 'halo':
            self.config['halo']['last_sync'] = datetime.now().isoformat()
            self.config['halo']['sync_status'] = status
        
        return self._save_config()

