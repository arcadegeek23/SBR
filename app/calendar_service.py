"""
Calendar Integration Service
Supports Microsoft Graph API (Office 365) and Gmail API
"""
import os
import json
import requests
from datetime import datetime, timedelta

class CalendarService:
    """Unified calendar service for Microsoft 365 and Gmail"""
    
    def __init__(self, provider='microsoft', access_token=None, config=None):
        """
        Initialize calendar service
        
        Args:
            provider: 'microsoft' or 'gmail'
            access_token: OAuth access token
            config: Configuration dict with API credentials
        """
        self.provider = provider
        self.access_token = access_token
        self.config = config or {}
        
        if provider == 'microsoft':
            self.base_url = 'https://graph.microsoft.com/v1.0'
        elif provider == 'gmail':
            self.base_url = 'https://www.googleapis.com/calendar/v3'
    
    def create_event(self, meeting_data):
        """
        Create calendar event
        
        Args:
            meeting_data: dict with meeting details
        
        Returns:
            Event ID from calendar provider
        """
        if not self.access_token:
            return None
        
        if self.provider == 'microsoft':
            return self._create_microsoft_event(meeting_data)
        elif self.provider == 'gmail':
            return self._create_gmail_event(meeting_data)
    
    def update_event(self, event_id, meeting_data):
        """Update existing calendar event"""
        if not self.access_token:
            return False
        
        if self.provider == 'microsoft':
            return self._update_microsoft_event(event_id, meeting_data)
        elif self.provider == 'gmail':
            return self._update_gmail_event(event_id, meeting_data)
    
    def delete_event(self, event_id):
        """Delete calendar event"""
        if not self.access_token:
            return False
        
        if self.provider == 'microsoft':
            return self._delete_microsoft_event(event_id)
        elif self.provider == 'gmail':
            return self._delete_gmail_event(event_id)
    
    def get_events(self, start_date=None, end_date=None):
        """Get calendar events in date range"""
        if not self.access_token:
            return []
        
        if self.provider == 'microsoft':
            return self._get_microsoft_events(start_date, end_date)
        elif self.provider == 'gmail':
            return self._get_gmail_events(start_date, end_date)
    
    # Microsoft Graph API methods
    
    def _create_microsoft_event(self, meeting_data):
        """Create event using Microsoft Graph API"""
        try:
            url = f"{self.base_url}/me/events"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            event_data = {
                'subject': meeting_data.get('title'),
                'body': {
                    'contentType': 'HTML',
                    'content': meeting_data.get('description', '')
                },
                'start': {
                    'dateTime': meeting_data.get('start_time'),
                    'timeZone': 'UTC'
                },
                'end': {
                    'dateTime': self._calculate_end_time(
                        meeting_data.get('start_time'),
                        meeting_data.get('duration_minutes', 60)
                    ),
                    'timeZone': 'UTC'
                },
                'location': {
                    'displayName': meeting_data.get('location', 'Online')
                },
                'attendees': self._format_microsoft_attendees(meeting_data.get('attendees', []))
            }
            
            response = requests.post(url, headers=headers, json=event_data)
            response.raise_for_status()
            
            result = response.json()
            return result.get('id')
            
        except Exception as e:
            print(f"Error creating Microsoft event: {e}")
            return None
    
    def _update_microsoft_event(self, event_id, meeting_data):
        """Update Microsoft event"""
        try:
            url = f"{self.base_url}/me/events/{event_id}"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            event_data = {
                'subject': meeting_data.get('title'),
                'body': {
                    'contentType': 'HTML',
                    'content': meeting_data.get('description', '')
                },
                'start': {
                    'dateTime': meeting_data.get('start_time'),
                    'timeZone': 'UTC'
                },
                'end': {
                    'dateTime': self._calculate_end_time(
                        meeting_data.get('start_time'),
                        meeting_data.get('duration_minutes', 60)
                    ),
                    'timeZone': 'UTC'
                }
            }
            
            response = requests.patch(url, headers=headers, json=event_data)
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Error updating Microsoft event: {e}")
            return False
    
    def _delete_microsoft_event(self, event_id):
        """Delete Microsoft event"""
        try:
            url = f"{self.base_url}/me/events/{event_id}"
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Error deleting Microsoft event: {e}")
            return False
    
    def _get_microsoft_events(self, start_date, end_date):
        """Get Microsoft events"""
        try:
            url = f"{self.base_url}/me/calendar/events"
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            params = {}
            if start_date and end_date:
                params['$filter'] = f"start/dateTime ge '{start_date}' and end/dateTime le '{end_date}'"
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            result = response.json()
            return result.get('value', [])
            
        except Exception as e:
            print(f"Error getting Microsoft events: {e}")
            return []
    
    def _format_microsoft_attendees(self, attendees):
        """Format attendees for Microsoft Graph"""
        formatted = []
        for attendee in attendees:
            formatted.append({
                'emailAddress': {
                    'address': attendee.get('email'),
                    'name': attendee.get('name')
                },
                'type': 'required'
            })
        return formatted
    
    # Gmail API methods
    
    def _create_gmail_event(self, meeting_data):
        """Create event using Gmail Calendar API"""
        try:
            url = f"{self.base_url}/calendars/primary/events"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            event_data = {
                'summary': meeting_data.get('title'),
                'description': meeting_data.get('description', ''),
                'start': {
                    'dateTime': meeting_data.get('start_time'),
                    'timeZone': 'UTC'
                },
                'end': {
                    'dateTime': self._calculate_end_time(
                        meeting_data.get('start_time'),
                        meeting_data.get('duration_minutes', 60)
                    ),
                    'timeZone': 'UTC'
                },
                'location': meeting_data.get('location', 'Online'),
                'attendees': self._format_gmail_attendees(meeting_data.get('attendees', []))
            }
            
            response = requests.post(url, headers=headers, json=event_data)
            response.raise_for_status()
            
            result = response.json()
            return result.get('id')
            
        except Exception as e:
            print(f"Error creating Gmail event: {e}")
            return None
    
    def _update_gmail_event(self, event_id, meeting_data):
        """Update Gmail event"""
        try:
            url = f"{self.base_url}/calendars/primary/events/{event_id}"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            event_data = {
                'summary': meeting_data.get('title'),
                'description': meeting_data.get('description', ''),
                'start': {
                    'dateTime': meeting_data.get('start_time'),
                    'timeZone': 'UTC'
                },
                'end': {
                    'dateTime': self._calculate_end_time(
                        meeting_data.get('start_time'),
                        meeting_data.get('duration_minutes', 60)
                    ),
                    'timeZone': 'UTC'
                }
            }
            
            response = requests.put(url, headers=headers, json=event_data)
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Error updating Gmail event: {e}")
            return False
    
    def _delete_gmail_event(self, event_id):
        """Delete Gmail event"""
        try:
            url = f"{self.base_url}/calendars/primary/events/{event_id}"
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Error deleting Gmail event: {e}")
            return False
    
    def _get_gmail_events(self, start_date, end_date):
        """Get Gmail events"""
        try:
            url = f"{self.base_url}/calendars/primary/events"
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            params = {}
            if start_date:
                params['timeMin'] = start_date
            if end_date:
                params['timeMax'] = end_date
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_status()
            
            result = response.json()
            return result.get('items', [])
            
        except Exception as e:
            print(f"Error getting Gmail events: {e}")
            return []
    
    def _format_gmail_attendees(self, attendees):
        """Format attendees for Gmail API"""
        formatted = []
        for attendee in attendees:
            formatted.append({
                'email': attendee.get('email'),
                'displayName': attendee.get('name')
            })
        return formatted
    
    # Utility methods
    
    def _calculate_end_time(self, start_time, duration_minutes):
        """Calculate end time from start time and duration"""
        if isinstance(start_time, str):
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        else:
            start_dt = start_time
        
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        return end_dt.isoformat()
    
    @staticmethod
    def get_oauth_url(provider, client_id, redirect_uri, state=None):
        """Get OAuth authorization URL"""
        if provider == 'microsoft':
            scope = 'Calendars.ReadWrite offline_access'
            auth_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
            params = {
                'client_id': client_id,
                'response_type': 'code',
                'redirect_uri': redirect_uri,
                'scope': scope,
                'state': state or ''
            }
        elif provider == 'gmail':
            scope = 'https://www.googleapis.com/auth/calendar'
            auth_url = 'https://accounts.google.com/o/oauth2/v2/auth'
            params = {
                'client_id': client_id,
                'response_type': 'code',
                'redirect_uri': redirect_uri,
                'scope': scope,
                'access_type': 'offline',
                'state': state or ''
            }
        else:
            return None
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{auth_url}?{query_string}"

