from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class ReportRun(db.Model):
    """Stores generated report metadata and results"""
    __tablename__ = 'report_runs'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(100), nullable=False, index=True)
    customer_name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(50), default='government')
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Signals (stored as JSON)
    signals = db.Column(db.JSON, nullable=False)
    
    # Scores (stored as JSON)
    nist_scores = db.Column(db.JSON, nullable=False)
    overall_score = db.Column(db.Float, nullable=False)
    
    # Gaps and recommendations
    gaps = db.Column(db.JSON, nullable=False)
    recommendations = db.Column(db.JSON, nullable=False)
    
    # Budget
    budget = db.Column(db.JSON, nullable=False)
    total_monthly_cost = db.Column(db.Float, nullable=False)
    
    # Report paths
    markdown_path = db.Column(db.String(500))
    html_path = db.Column(db.String(500))
    pdf_path = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'industry': self.industry,
            'generated_at': self.generated_at.isoformat(),
            'signals': self.signals,
            'nist_scores': self.nist_scores,
            'overall_score': self.overall_score,
            'gaps': self.gaps,
            'recommendations': self.recommendations,
            'budget': self.budget,
            'total_monthly_cost': self.total_monthly_cost,
            'markdown_path': self.markdown_path,
            'html_path': self.html_path,
            'pdf_path': self.pdf_path
        }

class Customer(db.Model):
    """Cache for customer metadata from Halo or manual entry"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(50), default='government')  # government, nonprofit, manufacturing, financial, healthcare
    
    # Contact Information
    contact = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    
    # Organization Details
    employees = db.Column(db.Integer)
    total_assets = db.Column(db.Integer)
    servers = db.Column(db.Integer)
    
    # Technical Metrics (can be manually entered if integration incomplete)
    patch_compliance = db.Column(db.Float)  # Percentage
    backup_success = db.Column(db.Float)    # Percentage
    edr_coverage = db.Column(db.Float)      # Percentage
    sla_attainment = db.Column(db.Float)    # Percentage
    
    # Metadata
    custom_metadata = db.Column(db.JSON)
    last_synced = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'name': self.name,
            'industry': self.industry,
            'contact': self.contact,
            'email': self.email,
            'phone': self.phone,
            'employees': self.employees,
            'total_assets': self.total_assets,
            'servers': self.servers,
            'patch_compliance': self.patch_compliance,
            'backup_success': self.backup_success,
            'edr_coverage': self.edr_coverage,
            'sla_attainment': self.sla_attainment,
            'metadata': self.custom_metadata,
            'last_synced': self.last_synced.isoformat() if self.last_synced else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

