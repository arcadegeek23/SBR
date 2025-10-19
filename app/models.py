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
    """Cache for customer metadata from Halo"""
    __tablename__ = 'customers'
    
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    custom_metadata = db.Column(db.JSON)
    last_synced = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'metadata': self.custom_metadata,
            'last_synced': self.last_synced.isoformat()
        }

