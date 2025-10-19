import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random

class HaloConnector:
    """Connects to HaloPSA API or provides mock data"""
    
    def __init__(self, api_url: str, api_key: str, client_id: str, client_secret: str, use_mock: bool = True):
        self.api_url = api_url
        self.api_key = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_mock = use_mock
        self.access_token = None
    
    def _authenticate(self) -> bool:
        """Authenticate with HaloPSA and get access token"""
        if self.use_mock:
            return True
        
        try:
            auth_url = f"{self.api_url}/token"
            response = requests.post(
                auth_url,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'scope': 'all'
                }
            )
            response.raise_for_status()
            self.access_token = response.json().get('access_token')
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def _get_headers(self) -> Dict:
        """Get request headers with authentication"""
        if self.use_mock:
            return {}
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_customer(self, customer_id: str) -> Optional[Dict]:
        """Get customer metadata"""
        if self.use_mock:
            return self._mock_customer(customer_id)
        
        try:
            if not self.access_token:
                self._authenticate()
            
            url = f"{self.api_url}/customers/{customer_id}"
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch customer: {e}")
            return None
    
    def get_assets(self, customer_id: str) -> List[Dict]:
        """Get asset inventory for customer"""
        if self.use_mock:
            return self._mock_assets(customer_id)
        
        try:
            if not self.access_token:
                self._authenticate()
            
            url = f"{self.api_url}/assets"
            params = {'customerId': customer_id}
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch assets: {e}")
            return []
    
    def get_tickets(self, customer_id: str, days: int = 90) -> List[Dict]:
        """Get tickets for customer"""
        if self.use_mock:
            return self._mock_tickets(customer_id, days)
        
        try:
            if not self.access_token:
                self._authenticate()
            
            url = f"{self.api_url}/tickets"
            params = {
                'customerId': customer_id,
                'startDate': (datetime.now() - timedelta(days=days)).isoformat()
            }
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch tickets: {e}")
            return []
    
    def get_users(self, customer_id: str) -> List[Dict]:
        """Get users for customer"""
        if self.use_mock:
            return self._mock_users(customer_id)
        
        try:
            if not self.access_token:
                self._authenticate()
            
            url = f"{self.api_url}/users"
            params = {'customerId': customer_id}
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch users: {e}")
            return []
    
    # Mock data methods
    def _mock_customer(self, customer_id: str) -> Dict:
        """Generate mock customer data"""
        return {
            'id': customer_id,
            'name': f'Acme Corporation {customer_id}',
            'industry': 'Technology',
            'mfa_enforced': random.choice([True, False]),
            'employee_count': random.randint(50, 500)
        }
    
    def _mock_assets(self, customer_id: str) -> List[Dict]:
        """Generate mock asset data"""
        asset_count = random.randint(20, 100)
        assets = []
        
        for i in range(asset_count):
            asset_type = random.choice(['Server', 'Workstation', 'Laptop', 'Mobile'])
            assets.append({
                'id': f'asset-{customer_id}-{i}',
                'name': f'{asset_type}-{i:03d}',
                'type': asset_type,
                'patchstatus': random.choice(['Compliant', 'Compliant', 'Compliant', 'UpToDate', 'OutOfDate', 'Unknown']),
                'antivirusstatus': random.choice(['Protected', 'Protected', 'Enabled', 'Disabled', 'Unknown']),
                'backup_enabled': random.choice([True, True, True, False]),
                'os': random.choice(['Windows 11', 'Windows 10', 'Windows Server 2022', 'macOS', 'Linux'])
            })
        
        return assets
    
    def _mock_tickets(self, customer_id: str, days: int = 90) -> List[Dict]:
        """Generate mock ticket data with detailed attributes"""
        ticket_count = random.randint(50, 150)
        tickets = []
        
        categories = ['Hardware Issue', 'Software Issue', 'Network Issue', 'Security', 'Password Reset', 
                     'Account Access', 'Equipment Failure', 'Application Error', 'Email Issue', 'Printer Issue']
        priorities = ['Low', 'Normal', 'Normal', 'Normal', 'High', 'Critical']
        statuses = ['Resolved', 'Resolved', 'Resolved', 'Closed', 'Open']
        
        # Generate user names for ticket assignment
        user_names = [f'User {i}' for i in range(random.randint(25, 100))]
        
        # Generate asset names
        asset_names = []
        for asset_type in ['Server', 'Workstation', 'Laptop']:
            for i in range(random.randint(5, 20)):
                asset_names.append((f'{asset_type}-{i:03d}', asset_type))
        
        for i in range(ticket_count):
            month_offset = random.randint(0, 2)  # Distribute across 3 months
            created = datetime.now() - timedelta(days=random.randint(month_offset * 30, (month_offset + 1) * 30))
            resolution_hours = random.randint(1, 120)
            resolved = created + timedelta(hours=resolution_hours)
            
            priority = random.choice(priorities)
            category = random.choice(categories)
            status = random.choice(statuses)
            user = random.choice(user_names)
            asset_info = random.choice(asset_names)
            
            # SLA based on priority
            sla_target = {'Critical': 4, 'High': 8, 'Normal': 24, 'Low': 48}.get(priority, 24)
            sla_met = resolution_hours <= sla_target
            
            tickets.append({
                'id': f'ticket-{customer_id}-{i}',
                'subject': f'{category} - {user}',
                'created_at': created.isoformat(),
                'resolved_at': resolved.isoformat() if status in ['Resolved', 'Closed'] else None,
                'resolution_hours': resolution_hours if status in ['Resolved', 'Closed'] else None,
                'sla_met': sla_met,
                'category': category,
                'priority': priority,
                'status': status,
                'user': user,
                'asset': asset_info[0],
                'asset_type': asset_info[1],
                'month_offset': month_offset
            })
        
        return tickets
    
    def _mock_users(self, customer_id: str) -> List[Dict]:
        """Generate mock user data"""
        user_count = random.randint(25, 200)
        users = []
        
        for i in range(user_count):
            users.append({
                'id': f'user-{customer_id}-{i}',
                'name': f'User {i}',
                'email': f'user{i}@customer{customer_id}.com',
                'active': random.choice([True, True, True, True, False])
            })
        
        return users

