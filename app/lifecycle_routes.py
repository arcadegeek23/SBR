"""
Lifecycle Manager API Routes
Goals, Meetings, Agreements, Segmentation endpoints
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, date
import json

lifecycle_bp = Blueprint('lifecycle', __name__, url_prefix='/api/lifecycle')

def init_lifecycle_routes(app, db):
    """Initialize lifecycle routes with app and db"""
    from app.lifecycle_models import ClientGoal, Meeting, ClientAgreement, ClientSegmentation, ActionItem
    from app.segmentation_service import SegmentationService
    from app.clientiq_service import ClientIQService
    from app.calendar_service import CalendarService
    
    segmentation_service = SegmentationService(db)
    clientiq_service = ClientIQService()
    
    # Goals endpoints
    
    @lifecycle_bp.route('/goals', methods=['GET'])
    def get_goals():
        """Get all goals, optionally filtered by customer"""
        customer_id = request.args.get('customer_id')
        
        query = ClientGoal.query
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        
        goals = query.order_by(ClientGoal.created_at.desc()).all()
        return jsonify([g.to_dict() for g in goals])
    
    @lifecycle_bp.route('/goals/<int:goal_id>', methods=['GET'])
    def get_goal(goal_id):
        """Get specific goal"""
        goal = ClientGoal.query.get_or_404(goal_id)
        return jsonify(goal.to_dict())
    
    @lifecycle_bp.route('/goals', methods=['POST'])
    def create_goal():
        """Create new goal"""
        data = request.json
        
        goal = ClientGoal(
            customer_id=data['customer_id'],
            title=data['title'],
            description=data.get('description'),
            category=data.get('category'),
            priority=data.get('priority', 'medium'),
            target_date=datetime.fromisoformat(data['target_date']).date() if data.get('target_date') else None,
            status=data.get('status', 'not_started'),
            progress_percentage=data.get('progress_percentage', 0),
            linked_initiatives=data.get('linked_initiatives'),
            owner=data.get('owner'),
            stakeholders=data.get('stakeholders'),
            success_metrics=data.get('success_metrics'),
            current_value=data.get('current_value'),
            target_value=data.get('target_value')
        )
        
        db.session.add(goal)
        db.session.commit()
        
        return jsonify(goal.to_dict()), 201
    
    @lifecycle_bp.route('/goals/<int:goal_id>', methods=['PUT'])
    def update_goal(goal_id):
        """Update goal"""
        goal = ClientGoal.query.get_or_404(goal_id)
        data = request.json
        
        goal.title = data.get('title', goal.title)
        goal.description = data.get('description', goal.description)
        goal.category = data.get('category', goal.category)
        goal.priority = data.get('priority', goal.priority)
        goal.status = data.get('status', goal.status)
        goal.progress_percentage = data.get('progress_percentage', goal.progress_percentage)
        goal.linked_initiatives = data.get('linked_initiatives', goal.linked_initiatives)
        goal.owner = data.get('owner', goal.owner)
        goal.stakeholders = data.get('stakeholders', goal.stakeholders)
        goal.current_value = data.get('current_value', goal.current_value)
        goal.target_value = data.get('target_value', goal.target_value)
        goal.updated_at = datetime.utcnow()
        
        if data.get('target_date'):
            goal.target_date = datetime.fromisoformat(data['target_date']).date()
        
        db.session.commit()
        return jsonify(goal.to_dict())
    
    @lifecycle_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
    def delete_goal(goal_id):
        """Delete goal"""
        goal = ClientGoal.query.get_or_404(goal_id)
        db.session.delete(goal)
        db.session.commit()
        return '', 204
    
    # Meetings endpoints
    
    @lifecycle_bp.route('/meetings', methods=['GET'])
    def get_meetings():
        """Get all meetings, optionally filtered"""
        customer_id = request.args.get('customer_id')
        status = request.args.get('status')
        
        query = Meeting.query
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        if status:
            query = query.filter_by(status=status)
        
        meetings = query.order_by(Meeting.scheduled_date.desc()).all()
        return jsonify([m.to_dict() for m in meetings])
    
    @lifecycle_bp.route('/meetings/<int:meeting_id>', methods=['GET'])
    def get_meeting(meeting_id):
        """Get specific meeting"""
        meeting = Meeting.query.get_or_404(meeting_id)
        return jsonify(meeting.to_dict())
    
    @lifecycle_bp.route('/meetings', methods=['POST'])
    def create_meeting():
        """Create new meeting"""
        data = request.json
        
        meeting = Meeting(
            customer_id=data['customer_id'],
            title=data['title'],
            meeting_type=data.get('meeting_type'),
            description=data.get('description'),
            scheduled_date=datetime.fromisoformat(data['scheduled_date']),
            duration_minutes=data.get('duration_minutes', 60),
            location=data.get('location'),
            agenda=data.get('agenda'),
            attendees=data.get('attendees'),
            status='scheduled',
            created_by=data.get('created_by')
        )
        
        db.session.add(meeting)
        db.session.commit()
        
        # Create calendar event if configured
        # TODO: Implement calendar sync
        
        return jsonify(meeting.to_dict()), 201
    
    @lifecycle_bp.route('/meetings/<int:meeting_id>', methods=['PUT'])
    def update_meeting(meeting_id):
        """Update meeting"""
        meeting = Meeting.query.get_or_404(meeting_id)
        data = request.json
        
        meeting.title = data.get('title', meeting.title)
        meeting.description = data.get('description', meeting.description)
        meeting.meeting_type = data.get('meeting_type', meeting.meeting_type)
        meeting.location = data.get('location', meeting.location)
        meeting.agenda = data.get('agenda', meeting.agenda)
        meeting.notes = data.get('notes', meeting.notes)
        meeting.action_items = data.get('action_items', meeting.action_items)
        meeting.decisions = data.get('decisions', meeting.decisions)
        meeting.attendees = data.get('attendees', meeting.attendees)
        meeting.status = data.get('status', meeting.status)
        meeting.recording_url = data.get('recording_url', meeting.recording_url)
        meeting.updated_at = datetime.utcnow()
        
        if data.get('scheduled_date'):
            meeting.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        if data.get('duration_minutes'):
            meeting.duration_minutes = data['duration_minutes']
        
        db.session.commit()
        return jsonify(meeting.to_dict())
    
    @lifecycle_bp.route('/meetings/<int:meeting_id>', methods=['DELETE'])
    def delete_meeting(meeting_id):
        """Delete meeting"""
        meeting = Meeting.query.get_or_404(meeting_id)
        db.session.delete(meeting)
        db.session.commit()
        return '', 204
    
    # Agreements endpoints
    
    @lifecycle_bp.route('/agreements', methods=['GET'])
    def get_agreements():
        """Get all agreements"""
        customer_id = request.args.get('customer_id')
        
        query = ClientAgreement.query
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        
        agreements = query.order_by(ClientAgreement.start_date.desc()).all()
        return jsonify([a.to_dict() for a in agreements])
    
    @lifecycle_bp.route('/agreements', methods=['POST'])
    def create_agreement():
        """Create new agreement"""
        data = request.json
        
        agreement = ClientAgreement(
            customer_id=data['customer_id'],
            agreement_name=data['agreement_name'],
            agreement_type=data.get('agreement_type'),
            monthly_mrr=data.get('monthly_mrr', 0.0),
            annual_value=data.get('annual_value'),
            billing_frequency=data.get('billing_frequency', 'monthly'),
            start_date=datetime.fromisoformat(data['start_date']).date(),
            end_date=datetime.fromisoformat(data['end_date']).date() if data.get('end_date') else None,
            renewal_date=datetime.fromisoformat(data['renewal_date']).date() if data.get('renewal_date') else None,
            contract_term_months=data.get('contract_term_months', 12),
            status=data.get('status', 'active'),
            auto_renew=data.get('auto_renew', True),
            services=data.get('services')
        )
        
        db.session.add(agreement)
        db.session.commit()
        
        # Trigger segmentation recalculation
        _recalculate_segmentation(agreement.customer_id)
        
        return jsonify(agreement.to_dict()), 201
    
    @lifecycle_bp.route('/agreements/<int:agreement_id>', methods=['PUT'])
    def update_agreement(agreement_id):
        """Update agreement"""
        agreement = ClientAgreement.query.get_or_404(agreement_id)
        data = request.json
        
        agreement.agreement_name = data.get('agreement_name', agreement.agreement_name)
        agreement.monthly_mrr = data.get('monthly_mrr', agreement.monthly_mrr)
        agreement.status = data.get('status', agreement.status)
        agreement.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Trigger segmentation recalculation
        _recalculate_segmentation(agreement.customer_id)
        
        return jsonify(agreement.to_dict())
    
    # Segmentation endpoints
    
    @lifecycle_bp.route('/segmentation', methods=['GET'])
    def get_all_segmentation():
        """Get all client segmentation data"""
        tier = request.args.get('tier')
        
        query = ClientSegmentation.query
        if tier:
            query = query.filter_by(tier=tier)
        
        segments = query.all()
        return jsonify([s.to_dict() for s in segments])
    
    @lifecycle_bp.route('/segmentation/<customer_id>', methods=['GET'])
    def get_segmentation(customer_id):
        """Get segmentation for specific customer"""
        segment = ClientSegmentation.query.filter_by(customer_id=customer_id).first()
        if not segment:
            # Calculate if doesn't exist
            segment = _recalculate_segmentation(customer_id)
        
        return jsonify(segment.to_dict() if segment else {})
    
    @lifecycle_bp.route('/segmentation/<customer_id>/recalculate', methods=['POST'])
    def recalculate_segmentation(customer_id):
        """Force recalculation of segmentation"""
        segment = _recalculate_segmentation(customer_id)
        return jsonify(segment.to_dict() if segment else {})
    
    # Action Items endpoints
    
    @lifecycle_bp.route('/action-items', methods=['GET'])
    def get_action_items():
        """Get action items"""
        customer_id = request.args.get('customer_id')
        status = request.args.get('status')
        
        query = ActionItem.query
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        if status:
            query = query.filter_by(status=status)
        
        items = query.order_by(ActionItem.due_date.asc()).all()
        return jsonify([i.to_dict() for i in items])
    
    @lifecycle_bp.route('/action-items', methods=['POST'])
    def create_action_item():
        """Create action item"""
        data = request.json
        
        item = ActionItem(
            customer_id=data['customer_id'],
            meeting_id=data.get('meeting_id'),
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            assigned_to=data.get('assigned_to'),
            assigned_by=data.get('assigned_by'),
            due_date=datetime.fromisoformat(data['due_date']).date() if data.get('due_date') else None,
            status='open'
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify(item.to_dict()), 201
    
    @lifecycle_bp.route('/action-items/<int:item_id>', methods=['PUT'])
    def update_action_item(item_id):
        """Update action item"""
        item = ActionItem.query.get_or_404(item_id)
        data = request.json
        
        item.title = data.get('title', item.title)
        item.status = data.get('status', item.status)
        item.priority = data.get('priority', item.priority)
        item.updated_at = datetime.utcnow()
        
        if data.get('status') == 'completed' and not item.completed_date:
            item.completed_date = date.today()
        
        db.session.commit()
        return jsonify(item.to_dict())
    
    # ClientIQ endpoints
    
    @lifecycle_bp.route('/clientiq/<customer_id>/summary', methods=['GET'])
    def get_client_summary(customer_id):
        """Get AI-powered client summary"""
        from app.models import Customer, ReportRun
        
        customer = Customer.query.filter_by(customer_id=customer_id).first_or_404()
        reports = ReportRun.query.filter_by(customer_id=customer_id).order_by(ReportRun.generated_at.desc()).limit(5).all()
        meetings = Meeting.query.filter_by(customer_id=customer_id).order_by(Meeting.scheduled_date.desc()).limit(10).all()
        goals = ClientGoal.query.filter_by(customer_id=customer_id).all()
        agreements = ClientAgreement.query.filter_by(customer_id=customer_id).all()
        
        summary = clientiq_service.generate_client_summary(
            customer.to_dict(),
            [r.to_dict() for r in reports],
            [m.to_dict() for m in meetings],
            [g.to_dict() for g in goals],
            [a.to_dict() for a in agreements]
        )
        
        return jsonify(summary)
    
    @lifecycle_bp.route('/clientiq/<customer_id>/meeting-prep', methods=['GET'])
    def get_meeting_prep(customer_id):
        """Get AI-powered meeting preparation"""
        from app.models import Customer
        
        customer = Customer.query.filter_by(customer_id=customer_id).first_or_404()
        meeting_type = request.args.get('type', 'qbr')
        
        # Get segmentation data
        segment = ClientSegmentation.query.filter_by(customer_id=customer_id).first()
        
        customer_data = customer.to_dict()
        if segment:
            customer_data.update(segment.to_dict())
        
        prep = clientiq_service.generate_meeting_prep(customer_data, meeting_type)
        
        return jsonify(prep)
    
    # Helper functions
    
    def _recalculate_segmentation(customer_id):
        """Recalculate segmentation for a customer"""
        from app.models import ReportRun
        
        agreements = ClientAgreement.query.filter_by(customer_id=customer_id).all()
        meetings = Meeting.query.filter_by(customer_id=customer_id).all()
        reports = ReportRun.query.filter_by(customer_id=customer_id).all()
        
        segment_data = segmentation_service.calculate_segmentation(
            customer_id,
            [a.to_dict() for a in agreements],
            [m.to_dict() for m in meetings],
            [r.to_dict() for r in reports]
        )
        
        # Update or create segmentation record
        segment = ClientSegmentation.query.filter_by(customer_id=customer_id).first()
        
        if segment:
            for key, value in segment_data.items():
                if hasattr(segment, key):
                    setattr(segment, key, value)
        else:
            segment = ClientSegmentation(**segment_data)
            db.session.add(segment)
        
        db.session.commit()
        return segment
    
    return lifecycle_bp

