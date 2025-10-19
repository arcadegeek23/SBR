import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://sbr_user:sbr_password@db:5432/sbr_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # HaloPSA
    HALO_API_URL = os.getenv('HALO_API_URL', 'https://your-halo-instance.halopsa.com/api')
    HALO_API_KEY = os.getenv('HALO_API_KEY', '')
    HALO_CLIENT_ID = os.getenv('HALO_CLIENT_ID', '')
    HALO_CLIENT_SECRET = os.getenv('HALO_CLIENT_SECRET', '')
    USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'true').lower() == 'true'
    
    # Unit Costs (Monthly)
    COST_MFA_PER_USER = float(os.getenv('COST_MFA_PER_USER', '3.00'))
    COST_EDR_PER_ENDPOINT = float(os.getenv('COST_EDR_PER_ENDPOINT', '5.50'))
    COST_BACKUP_PER_SERVER = float(os.getenv('COST_BACKUP_PER_SERVER', '45.00'))
    COST_SIEM_PER_USER = float(os.getenv('COST_SIEM_PER_USER', '6.50'))
    
    # Thresholds
    THRESHOLD_PATCH_COMPLIANCE = int(os.getenv('THRESHOLD_PATCH_COMPLIANCE', '95'))
    THRESHOLD_BACKUP_SUCCESS = int(os.getenv('THRESHOLD_BACKUP_SUCCESS', '98'))
    THRESHOLD_EDR_COVERAGE = int(os.getenv('THRESHOLD_EDR_COVERAGE', '90'))
    THRESHOLD_SLA_ATTAINMENT = int(os.getenv('THRESHOLD_SLA_ATTAINMENT', '90'))
    
    # Reports
    REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')

