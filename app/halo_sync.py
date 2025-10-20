"""
HaloPSA Sync Service
Handles customer import and synchronization with HaloPSA
"""
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from app.models import db, Customer

class HaloSyncService:
    """Service for syncing with HaloPSA"""
    
    def __init__(self, api_url: str, client_id: str, client_secret: str, tenant_id: str = None):
        self.api_url = api_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.access_token = None
        self.token_expires = None
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test connection to HaloPSA API"""
        try:
            # Attempt to get access token
            success = self._get_access_token()
            if not success:
                return False, "Failed to obtain access token. Check credentials."
            
            # Test API call
            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(f"{self.api_url}/api/client", headers=headers, timeout=10)
            
            if response.status_code == 200:
                return True, "Connection successful!"
            else:
                return False, f"API returned status {response.status_code}: {response.text}"
        
        except requests.exceptions.Timeout:
            return False, "Connection timeout. Check API URL."
        except requests.exceptions.ConnectionError:
            return False, "Connection error. Check API URL and network."
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def _get_access_token(self) -> bool:
        """Get OAuth access token from HaloPSA"""
        try:
            # Check if token is still valid
            if self.access_token and self.token_expires:
                if datetime.now() < self.token_expires:
                    return True
            
            # Request new token
            token_url = f"{self.api_url}/auth/token"
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'all'
            }
            
            if self.tenant_id:
                data['tenant'] = self.tenant_id
            
            response = requests.post(token_url, data=data, timeout=10)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 3600)
                self.token_expires = datetime.now() + timedelta(seconds=expires_in - 60)
                return True
            else:
                print(f"Token request failed: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            print(f"Error getting access token: {e}")
            return False
    
    def fetch_customers(self) -> Tuple[bool, List[Dict], str]:
        """Fetch all customers from HaloPSA"""
        try:
            if not self._get_access_token():
                return False, [], "Failed to authenticate with HaloPSA"
            
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            # Fetch clients (customers)
            response = requests.get(
                f"{self.api_url}/api/client",
                headers=headers,
                params={'pageinate': 'false', 'count': 1000},
                timeout=30
            )
            
            if response.status_code == 200:
                customers = response.json()
                
                # Transform to our format
                transformed = []
                for customer in customers:
                    transformed.append({
                        'customer_id': str(customer.get('id', '')),
                        'name': customer.get('name', 'Unknown'),
                        'industry': self._map_industry(customer.get('customfields', [])),
                        'metadata': {
                            'halo_id': customer.get('id'),
                            'website': customer.get('website', ''),
                            'phone': customer.get('phone', ''),
                            'notes': customer.get('notes', ''),
                            'is_vip': customer.get('isvip', False),
                            'status': customer.get('inactive', False) and 'inactive' or 'active'
                        }
                    })
                
                return True, transformed, f"Successfully fetched {len(transformed)} customers"
            else:
                return False, [], f"API error: {response.status_code} - {response.text}"
        
        except Exception as e:
            return False, [], f"Error fetching customers: {str(e)}"
    
    def _map_industry(self, custom_fields: List[Dict]) -> str:
        """Map Halo custom fields to industry"""
        # Look for industry field in custom fields
        for field in custom_fields:
            if field.get('name', '').lower() in ['industry', 'sector', 'vertical']:
                value = field.get('value', '').lower()
                if 'gov' in value or 'public' in value:
                    return 'government'
                elif 'nonprofit' in value or 'charity' in value:
                    return 'nonprofit'
                elif 'manufact' in value or 'industrial' in value:
                    return 'manufacturing'
                elif 'financ' in value or 'bank' in value:
                    return 'financial'
                elif 'health' in value or 'medical' in value:
                    return 'healthcare'
        
        return 'government'  # Default
    
    def import_customers_to_db(self, customers: List[Dict]) -> Tuple[int, int, int]:
        """
        Import customers to database
        Returns: (added, updated, errors)
        """
        added = 0
        updated = 0
        errors = 0
        
        for customer_data in customers:
            try:
                customer_id = customer_data['customer_id']
                
                # Check if customer exists
                existing = Customer.query.filter_by(customer_id=customer_id).first()
                
                if existing:
                    # Update existing
                    existing.name = customer_data['name']
                    existing.industry = customer_data['industry']
                    existing.custom_metadata = customer_data['metadata']
                    updated += 1
                else:
                    # Create new
                    new_customer = Customer(
                        customer_id=customer_id,
                        name=customer_data['name'],
                        industry=customer_data['industry'],
                        custom_metadata=customer_data['metadata']
                    )
                    db.session.add(new_customer)
                    added += 1
                
                db.session.commit()
            
            except Exception as e:
                print(f"Error importing customer {customer_data.get('customer_id')}: {e}")
                db.session.rollback()
                errors += 1
        
        return added, updated, errors

from datetime import timedelta

