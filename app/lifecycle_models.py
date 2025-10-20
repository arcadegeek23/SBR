"""
Lifecycle Manager X Inspired Models
Database models for Goals, Meetings, Agreements, and Segmentation
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class ClientGoal(db.Model):
    """Client business goals and objectives"""
    __tablename__ = 'client_goals'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(100), nullable=False, index=True)
    
    # Goal details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # business_growth, cost_reduction, efficiency, security, compliance
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    
    # Timeline
    target_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Progress tracking
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed, on_hold
    progress_percentage = db.Column(db.Integer, default=0)
    
    # IT initiatives linked to this goal
    linked_initiatives = db.Column(db.JSON)  # Array of initiative IDs/names
    
    # Owner and stakeholders
    owner = db.Column(db.String(255))
    stakeholders = db.Column(db.JSON)  # Array of stakeholder names
    
    # Metrics
    success_metrics = db.Column(db.JSON)  # Key metrics to track
    current_value = db.Column(db.String(100))
    target_value = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'linked_initiatives': self.linked_initiatives,
            'owner': self.owner,
            'stakeholders': self.stakeholders,
            'success_metrics': self.success_metrics,
            'current_value': self.current_value,
            'target_value': self.target_value
        }


class Meeting(db.Model):
    """Client meetings and QBRs"""
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(100), nullable=False, index=True)
    
    # Meeting details
    title = db.Column(db.String(255), nullable=False)
    meeting_type = db.Column(db.String(50))  # qbr, planning, review, emergency, general
    description = db.Column(db.Text)
    
    # Scheduling
    scheduled_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    location = db.Column(db.String(255))  # Physical location or meeting link
    
    # Calendar integration
    google_event_id = db.Column(db.String(255))
    outlook_event_id = db.Column(db.String(255))
    
    # Meeting content
    agenda = db.Column(db.JSON)  # Array of agenda items
    notes = db.Column(db.Text)
    action_items = db.Column(db.JSON)  # Array of action items
    decisions = db.Column(db.JSON)  # Array of decisions made
    
    # Attendees
    attendees = db.Column(db.JSON)  # Array of attendee objects
    
    # Status
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, rescheduled
    
    # Recording and attachments
    recording_url = db.Column(db.String(500))
    attachments = db.Column(db.JSON)  # Array of attachment URLs
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(255))
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'title': self.title,
            'meeting_type': self.meeting_type,
            'description': self.description,
            'scheduled_date': self.scheduled_date.isoformat(),
            'duration_minutes': self.duration_minutes,
            'location': self.location,
            'google_event_id': self.google_event_id,
            'outlook_event_id': self.outlook_event_id,
            'agenda': self.agenda,
            'notes': self.notes,
            'action_items': self.action_items,
            'decisions': self.decisions,
            'attendees': self.attendees,
            'status': self.status,
            'recording_url': self.recording_url,
            'attachments': self.attachments,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'created_by': self.created_by
        }


class ClientAgreement(db.Model):
    """Client service agreements and MRR tracking"""
    __tablename__ = 'client_agreements'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(100), nullable=False, index=True)
    
    # Agreement details
    agreement_name = db.Column(db.String(255), nullable=False)
    agreement_type = db.Column(db.String(50))  # managed_services, project, support, security
    
    # Financial
    monthly_mrr = db.Column(db.Float, nullable=False, default=0.0)
    annual_value = db.Column(db.Float)
    billing_frequency = db.Column(db.String(20), default='monthly')  # monthly, quarterly, annually
    
    # Contract terms
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    renewal_date = db.Column(db.Date)
    contract_term_months = db.Column(db.Integer, default=12)
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, expired, cancelled, pending
    auto_renew = db.Column(db.Boolean, default=True)
    
    # Services included
    services = db.Column(db.JSON)  # Array of service objects
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'agreement_name': self.agreement_name,
            'agreement_type': self.agreement_type,
            'monthly_mrr': self.monthly_mrr,
            'annual_value': self.annual_value,
            'billing_frequency': self.billing_frequency,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'renewal_date': self.renewal_date.isoformat() if self.renewal_date else None,
            'contract_term_months': self.contract_term_months,
            'status': self.status,
            'auto_renew': self.auto_renew,
            'services': self.services,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class ClientSegmentation(db.Model):
    """Auto-calculated client segmentation based on MRR and metrics"""
    __tablename__ = 'client_segmentation'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Tier classification (auto-calculated from MRR)
    tier = db.Column(db.String(20))  # platinum, gold, silver, bronze
    tier_score = db.Column(db.Float)  # Calculated score for tier placement
    
    # MRR-based metrics
    total_mrr = db.Column(db.Float, default=0.0)
    mrr_trend = db.Column(db.String(20))  # growing, stable, declining
    mrr_change_percentage = db.Column(db.Float)
    
    # Value metrics
    lifetime_value = db.Column(db.Float)
    customer_since = db.Column(db.Date)
    tenure_months = db.Column(db.Integer)
    
    # Health score (0-100)
    health_score = db.Column(db.Float)
    health_status = db.Column(db.String(20))  # excellent, good, at_risk, critical
    
    # Engagement metrics
    last_meeting_date = db.Column(db.DateTime)
    meetings_per_quarter = db.Column(db.Integer, default=0)
    last_report_date = db.Column(db.DateTime)
    
    # Risk indicators
    risk_level = db.Column(db.String(20), default='low')  # low, medium, high, critical
    risk_factors = db.Column(db.JSON)  # Array of risk factor descriptions
    
    # Strategic importance
    strategic_account = db.Column(db.Boolean, default=False)
    growth_potential = db.Column(db.String(20))  # high, medium, low
    
    # Custom tags
    tags = db.Column(db.JSON)  # Array of custom tags
    
    # Auto-calculation metadata
    last_calculated = db.Column(db.DateTime, default=datetime.utcnow)
    calculation_version = db.Column(db.String(20), default='1.0')
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'tier': self.tier,
            'tier_score': self.tier_score,
            'total_mrr': self.total_mrr,
            'mrr_trend': self.mrr_trend,
            'mrr_change_percentage': self.mrr_change_percentage,
            'lifetime_value': self.lifetime_value,
            'customer_since': self.customer_since.isoformat() if self.customer_since else None,
            'tenure_months': self.tenure_months,
            'health_score': self.health_score,
            'health_status': self.health_status,
            'last_meeting_date': self.last_meeting_date.isoformat() if self.last_meeting_date else None,
            'meetings_per_quarter': self.meetings_per_quarter,
            'last_report_date': self.last_report_date.isoformat() if self.last_report_date else None,
            'risk_level': self.risk_level,
            'risk_factors': self.risk_factors,
            'strategic_account': self.strategic_account,
            'growth_potential': self.growth_potential,
            'tags': self.tags,
            'last_calculated': self.last_calculated.isoformat(),
            'calculation_version': self.calculation_version
        }


class ActionItem(db.Model):
    """Action items from meetings and reports"""
    __tablename__ = 'action_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(100), nullable=False, index=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=True)
    
    # Action item details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # high, medium, low
    
    # Assignment
    assigned_to = db.Column(db.String(255))
    assigned_by = db.Column(db.String(255))
    
    # Timeline
    due_date = db.Column(db.Date)
    completed_date = db.Column(db.Date)
    
    # Status
    status = db.Column(db.String(20), default='open')  # open, in_progress, completed, cancelled
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'meeting_id': self.meeting_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'assigned_to': self.assigned_to,
            'assigned_by': self.assigned_by,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

