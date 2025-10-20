"""
Admin Authentication Module
Handles admin user authentication and authorization
"""
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os

class AdminAuth:
    """Admin authentication manager"""
    
    def __init__(self):
        # Default admin credentials (should be changed in production)
        self.admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        self.admin_password_hash = generate_password_hash(os.getenv('ADMIN_PASSWORD', 'admin123'))
    
    def verify_credentials(self, username: str, password: str) -> bool:
        """Verify admin credentials"""
        if username == self.admin_username:
            return check_password_hash(self.admin_password_hash, password)
        return False
    
    def login(self, username: str) -> None:
        """Set admin session"""
        session['admin_logged_in'] = True
        session['admin_username'] = username
    
    def logout(self) -> None:
        """Clear admin session"""
        session.pop('admin_logged_in', None)
        session.pop('admin_username', None)
    
    def is_logged_in(self) -> bool:
        """Check if admin is logged in"""
        return session.get('admin_logged_in', False)

def require_admin(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please log in to access the admin panel', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

