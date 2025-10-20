from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for, flash, session
from datetime import datetime
import os

from app.models import db, ReportRun, Customer
from app.config import Config
from app.halo_connector import HaloConnector
from app.signal_processor import SignalProcessor
from app.scoring_engine import ScoringEngine
from app.budget_engine import BudgetEngine
from app.report_builder import ReportBuilder
from app.ai_insights import AIInsightsEngine
from app.roi_engine import ROIEngine
from app.stakeholder_content import StakeholderContentGenerator
from app.admin_auth import AdminAuth, require_admin
from app.integration_config import IntegrationConfig
from app.halo_sync import HaloSyncService
from app.azure_ai_service import AzureAIService
from app.lifecycle_routes import init_lifecycle_routes

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Initialize database
db.init_app(app)

# Initialize admin components
admin_auth = AdminAuth()
integration_config = IntegrationConfig()

# Initialize components
halo = HaloConnector(
    api_url=Config.HALO_API_URL,
    api_key=Config.HALO_API_KEY,
    client_id=Config.HALO_CLIENT_ID,
    client_secret=Config.HALO_CLIENT_SECRET,
    use_mock=Config.USE_MOCK_DATA
)

signal_processor = SignalProcessor()

scoring_engine = ScoringEngine({
    'THRESHOLD_PATCH_COMPLIANCE': Config.THRESHOLD_PATCH_COMPLIANCE,
    'THRESHOLD_BACKUP_SUCCESS': Config.THRESHOLD_BACKUP_SUCCESS,
    'THRESHOLD_EDR_COVERAGE': Config.THRESHOLD_EDR_COVERAGE,
    'THRESHOLD_SLA_ATTAINMENT': Config.THRESHOLD_SLA_ATTAINMENT
})

budget_engine = BudgetEngine({
    'COST_MFA_PER_USER': Config.COST_MFA_PER_USER,
    'COST_EDR_PER_ENDPOINT': Config.COST_EDR_PER_ENDPOINT,
    'COST_BACKUP_PER_SERVER': Config.COST_BACKUP_PER_SERVER,
    'COST_SIEM_PER_USER': Config.COST_SIEM_PER_USER
})

report_builder = ReportBuilder(
    templates_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
    reports_dir=Config.REPORTS_DIR
)

ai_insights_engine = AIInsightsEngine()

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Main dashboard"""
    # Check if user is logged in as admin
    is_admin = session.get('admin_logged_in', False)
    return render_template('index.html', is_admin=is_admin)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'mock_data': Config.USE_MOCK_DATA
    })

@app.route('/api/generate-review', methods=['POST'])
def generate_review():
    """Generate a Strategic Business Review"""
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        
        if not customer_id:
            return jsonify({'error': 'customer_id is required'}), 400
        
        # Step 1: Fetch data from Halo
        customer = halo.get_customer(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
        
        assets = halo.get_assets(customer_id)
        tickets = halo.get_tickets(customer_id)
        users = halo.get_users(customer_id)
        
        # Step 2: Derive signals
        signals = signal_processor.derive_signals(customer, assets, tickets, users)
        
        # Step 3: Calculate NIST scores
        nist_scores = scoring_engine.calculate_nist_scores(signals)
        
        # Step 4: Identify gaps
        gaps = scoring_engine.identify_gaps(signals, nist_scores)
        
        # Step 5: Generate recommendations
        recommendations = scoring_engine.generate_recommendations(gaps, signals)
        
        # Step 6: Calculate budget
        budget = budget_engine.calculate_budget(signals, gaps)
        
        # Step 7: Generate AI insights
        customer_data = {
            'customer': customer,
            'assets': assets,
            'tickets': tickets,
            'users': users
        }
        ai_insights = ai_insights_engine.generate_insights(signals, customer_data)
        
        # Step 7b: Calculate ROI and generate stakeholder content
        industry = customer.get('industry', 'government')
        roi_engine = ROIEngine(industry=industry)
        stakeholder_gen = StakeholderContentGenerator()
        
        # Calculate all 4 ROI formats
        critical_incidents = len([t for t in tickets if t.get('priority') == 'Critical'])
        annual_investment = budget.get('total_monthly', 0) * 12
        
        roi_risk_avoidance = roi_engine.calculate_risk_avoidance_roi(
            investment=annual_investment,
            incidents_prevented=max(critical_incidents, 3),
            avg_incident_duration_hours=6.0
        )
        
        roi_efficiency = roi_engine.calculate_efficiency_unlock_roi(
            hours_freed_annually=ai_insights.get('ticket_analysis', {}).get('total_tickets', 100) * 0.25,
            cost_per_hour=50.0
        )
        
        roi_compliance = roi_engine.calculate_compliance_roi(
            current_compliance_pct=nist_scores.get('Overall', 0) * 100,
            target_compliance_pct=100,
            penalty_at_current=250000,
            cost_to_reach_target=annual_investment
        )
        
        roi_three_year = roi_engine.calculate_three_year_stacked_roi(
            year1_investment=annual_investment,
            year1_savings=roi_risk_avoidance.get('total_risk_prevented', 0) * 0.3
        )
        
        # Generate industry-specific metrics and peer benchmarking
        industry_metrics = roi_engine.generate_industry_metrics(signals, tickets)
        peer_benchmark = roi_engine.generate_peer_benchmark(signals)
        
        # Calculate tiered budget
        tiered_budget = roi_engine.calculate_tiered_budget(
            total_budget=annual_investment,
            gaps=gaps,
            current_monthly_cost=budget.get('total_monthly', 0)
        )
        
        # Combine all ROI data
        roi_data = {
            'risk_avoidance': roi_risk_avoidance,
            'efficiency': roi_efficiency,
            'compliance': roi_compliance,
            'three_year': roi_three_year,
            'industry_metrics': industry_metrics,
            'peer_benchmark': peer_benchmark,
            'tiered_budget': tiered_budget
        }
        
        # Generate stakeholder content
        executive_onepager = stakeholder_gen.generate_executive_onepager(
            customer_name=customer.get('name', 'Unknown'),
            overall_score=nist_scores.get('Overall', 0) * 100,
            roi_data=roi_risk_avoidance,
            top_risks=gaps[:3],
            top_recommendations=recommendations[:3]
        )
        
        board_talking_points = stakeholder_gen.generate_board_talking_points(
            customer_name=customer.get('name', 'Unknown'),
            industry=industry,
            key_metrics=industry_metrics,
            peer_benchmark=peer_benchmark,
            incidents_prevented=critical_incidents
        )
        
        budget_justification = stakeholder_gen.generate_budget_justification(
            tiered_budget=tiered_budget,
            current_state={
                'compliance_pct': nist_scores.get('Overall', 0) * 100,
                'gap_count': len(gaps),
                'posture_description': 'Needs Improvement' if nist_scores.get('Overall', 0) < 0.75 else 'Good',
                'risk_exposure': roi_risk_avoidance.get('total_risk_prevented', 0)
            },
            target_state={
                'compliance_pct': 100,
                'gaps_closed': len(gaps),
                'posture_description': 'Strong',
                'risk_reduction': roi_risk_avoidance.get('total_risk_prevented', 0)
            }
        )
        
        stakeholder_data = {
            'executive_onepager': executive_onepager,
            'board_talking_points': board_talking_points,
            'budget_justification': budget_justification,
            'industry': industry_metrics.get('industry', 'Unknown')
        }
        
        # Step 8: Generate reports
        report_paths = report_builder.generate_report(
            customer_id=customer_id,
            customer_name=customer.get('name', 'Unknown'),
            signals=signals,
            nist_scores=nist_scores,
            gaps=gaps,
            recommendations=recommendations,
            budget=budget,
            ai_insights=ai_insights,
            roi_data=roi_data,
            stakeholder_data=stakeholder_data
        )
        
        # Step 9: Save to database
        report_run = ReportRun(
            customer_id=customer_id,
            customer_name=customer.get('name', 'Unknown'),
            industry=customer.get('industry', 'government'),
            signals=signals,
            nist_scores=nist_scores,
            overall_score=nist_scores.get('Overall', 0),
            gaps=gaps,
            recommendations=recommendations,
            budget=budget,
            total_monthly_cost=budget.get('total_monthly', 0),
            markdown_path=report_paths.get('markdown'),
            html_path=report_paths.get('html'),
            pdf_path=report_paths.get('pdf')
        )
        
        db.session.add(report_run)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'report_id': report_run.id,
            'customer_name': customer.get('name'),
            'overall_score': nist_scores.get('Overall'),
            'total_monthly_cost': budget.get('total_monthly'),
            'gaps_count': len(gaps),
            'reports': {
                'markdown': os.path.basename(report_paths.get('markdown')),
                'html': os.path.basename(report_paths.get('html')),
                'pdf': os.path.basename(report_paths.get('pdf')) if report_paths.get('pdf') else None
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports')
def list_reports():
    """List all generated reports"""
    reports = ReportRun.query.order_by(ReportRun.generated_at.desc()).all()
    return jsonify({
        'reports': [r.to_dict() for r in reports]
    })

@app.route('/api/reports/<int:report_id>')
def get_report(report_id):
    """Get a specific report"""
    report = ReportRun.query.get_or_404(report_id)
    return jsonify(report.to_dict())

@app.route('/api/reports/<int:report_id>/download/<format>')
def download_report(report_id, format):
    """Download a report in specified format"""
    report = ReportRun.query.get_or_404(report_id)
    
    if format == 'markdown':
        filepath = report.markdown_path
        mimetype = 'text/markdown'
    elif format == 'html':
        filepath = report.html_path
        mimetype = 'text/html'
    elif format == 'pdf':
        filepath = report.pdf_path
        mimetype = 'application/pdf'
    else:
        return jsonify({'error': 'Invalid format'}), 400
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'Report file not found'}), 404
    
    return send_file(filepath, mimetype=mimetype, as_attachment=True)

@app.route('/view/<int:report_id>')
def view_report(report_id):
    """View a report in the browser"""
    report = ReportRun.query.get_or_404(report_id)
    
    if not report.html_path or not os.path.exists(report.html_path):
        return "Report not found", 404
    
    with open(report.html_path, 'r') as f:
        html_content = f.read()
    
    return html_content

# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if admin_auth.verify_credentials(username, password):
            admin_auth.login(username)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Admin logout"""
    admin_auth.logout()
    flash('Logged out successfully', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@require_admin
def admin_panel():
    """Admin panel main page"""
    # Get configuration
    halo_config = integration_config.get_halo_config()
    okta_config = integration_config.get_okta_config()
    azure_config = integration_config.get_azure_ai_config()
    sync_history = integration_config.get_sync_history()
    
    # Get customer statistics
    customers = Customer.query.all()
    customer_count = len(customers)
    report_count = ReportRun.query.count()
    
    # Add report count to each customer
    for customer in customers:
        customer.report_count = ReportRun.query.filter_by(customer_id=customer.customer_id).count()
    
    return render_template('admin.html',
                         halo_config=halo_config,
                         okta_config=okta_config,
                         azure_config=azure_config,
                         sync_history=sync_history,
                         customers=customers,
                         customer_count=customer_count,
                         report_count=report_count)

@app.route('/admin/halo/save', methods=['POST'])
@require_admin
def save_halo_config():
    """Save HaloPSA configuration"""
    config = {
        'enabled': request.form.get('enabled') == 'on',
        'api_url': request.form.get('api_url', ''),
        'client_id': request.form.get('client_id', ''),
        'client_secret': request.form.get('client_secret', ''),
        'tenant_id': request.form.get('tenant_id', '')
    }
    
    if integration_config.set_halo_config(config):
        flash('HaloPSA configuration saved successfully', 'success')
    else:
        flash('Error saving configuration', 'error')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/halo/test', methods=['POST'])
@require_admin
def test_halo_connection():
    """Test HaloPSA connection"""
    config = integration_config.get_halo_config()
    
    if not config.get('api_url') or not config.get('client_id'):
        return jsonify({'success': False, 'message': 'Configuration incomplete'})
    
    try:
        sync_service = HaloSyncService(
            api_url=config['api_url'],
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            tenant_id=config.get('tenant_id')
        )
        
        success, message = sync_service.test_connection()
        return jsonify({'success': success, 'message': message})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/halo/import', methods=['POST'])
@require_admin
def import_halo_customers():
    """Import customers from HaloPSA"""
    config = integration_config.get_halo_config()
    
    if not config.get('enabled'):
        return jsonify({'success': False, 'message': 'HaloPSA integration not enabled'})
    
    try:
        sync_service = HaloSyncService(
            api_url=config['api_url'],
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            tenant_id=config.get('tenant_id')
        )
        
        # Fetch customers
        success, customers, message = sync_service.fetch_customers()
        
        if not success:
            integration_config.add_sync_history('halo', 'error', message, 0)
            return jsonify({'success': False, 'message': message})
        
        # Import to database
        added, updated, errors = sync_service.import_customers_to_db(customers)
        
        # Update sync history
        total = added + updated
        integration_config.add_sync_history(
            'halo', 
            'success', 
            f'Imported {total} customers ({added} new, {updated} updated, {errors} errors)',
            total
        )
        integration_config.update_last_sync('halo', 'success')
        
        return jsonify({
            'success': True,
            'added': added,
            'updated': updated,
            'errors': errors,
            'total': total,
            'message': f'Successfully imported {total} customers'
        })
    
    except Exception as e:
        integration_config.add_sync_history('halo', 'error', str(e), 0)
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/okta/save', methods=['POST'])
@require_admin
def save_okta_config():
    """Save Okta configuration"""
    config = {
        'enabled': request.form.get('enabled') == 'on',
        'domain': request.form.get('domain', ''),
        'client_id': request.form.get('client_id', ''),
        'client_secret': request.form.get('client_secret', ''),
        'redirect_uri': request.form.get('redirect_uri', ''),
        'issuer': request.form.get('issuer', '')
    }
    
    if integration_config.set_okta_config(config):
        flash('Okta configuration saved successfully', 'success')
    else:
        flash('Error saving configuration', 'error')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/okta/test', methods=['POST'])
@require_admin
def test_okta_connection():
    """Test Okta connection"""
    config = integration_config.get_okta_config()
    
    if not config.get('domain') or not config.get('client_id'):
        return jsonify({'success': False, 'message': 'Configuration incomplete'})
    
    try:
        # Test by fetching OIDC discovery document
        import requests
        issuer = config.get('issuer') or f"https://{config['domain']}/oauth2/default"
        discovery_url = f"{issuer}/.well-known/openid-configuration"
        
        response = requests.get(discovery_url, timeout=10)
        
        if response.status_code == 200:
            return jsonify({'success': True, 'message': 'Connection successful! OIDC discovery endpoint accessible.'})
        else:
            return jsonify({'success': False, 'message': f'Discovery endpoint returned {response.status_code}'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/azure/save', methods=['POST'])
@require_admin
def save_azure_config():
    """Save Azure AI configuration"""
    config = {
        'enabled': request.form.get('enabled') == 'on',
        'endpoint': request.form.get('endpoint', ''),
        'api_key': request.form.get('api_key', ''),
        'deployment_name': request.form.get('deployment_name', ''),
        'api_version': request.form.get('api_version', '2024-02-15-preview'),
        'temperature': float(request.form.get('temperature', 0.7)),
        'max_tokens': int(request.form.get('max_tokens', 2000))
    }
    
    if integration_config.set_azure_ai_config(config):
        flash('Azure AI configuration saved successfully', 'success')
    else:
        flash('Error saving configuration', 'error')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/azure/test', methods=['POST'])
@require_admin
def test_azure_connection():
    """Test Azure AI connection"""
    config = integration_config.get_azure_ai_config()
    
    if not config.get('endpoint') or not config.get('api_key'):
        return jsonify({'success': False, 'message': 'Configuration incomplete'})
    
    try:
        ai_service = AzureAIService(
            endpoint=config['endpoint'],
            api_key=config['api_key'],
            deployment_name=config['deployment_name'],
            api_version=config['api_version']
        )
        
        success, message = ai_service.test_connection()
        return jsonify({'success': success, 'message': message})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Customer Management API Endpoints
@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    try:
        customers = Customer.query.all()
        customer_list = []
        for customer in customers:
            report_count = ReportRun.query.filter_by(customer_id=customer.customer_id).count()
            customer_dict = customer.to_dict()
            customer_dict['report_count'] = report_count
            customer_list.append(customer_dict)
        
        return jsonify({'success': True, 'customers': customer_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a specific customer"""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'success': False, 'message': 'Customer not found'}), 404
        
        return jsonify({'success': True, 'customer': customer.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Create a new customer"""
    try:
        data = request.get_json()
        
        # Check if customer_id already exists
        existing = Customer.query.filter_by(customer_id=data.get('customer_id')).first()
        if existing:
            return jsonify({'success': False, 'message': 'Customer ID already exists'}), 400
        
        customer = Customer(
            customer_id=data.get('customer_id'),
            name=data.get('name'),
            industry=data.get('industry'),
            employees=data.get('employees'),
            contact=data.get('contact'),
            email=data.get('email'),
            phone=data.get('phone'),
            total_assets=data.get('total_assets'),
            servers=data.get('servers'),
            patch_compliance=data.get('patch_compliance'),
            backup_success=data.get('backup_success'),
            edr_coverage=data.get('edr_coverage'),
            sla_attainment=data.get('sla_attainment')
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({'success': True, 'customer': customer.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update an existing customer"""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'success': False, 'message': 'Customer not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            customer.name = data['name']
        if 'industry' in data:
            customer.industry = data['industry']
        if 'employees' in data:
            customer.employees = data['employees']
        if 'contact' in data:
            customer.contact = data['contact']
        if 'email' in data:
            customer.email = data['email']
        if 'phone' in data:
            customer.phone = data['phone']
        if 'total_assets' in data:
            customer.total_assets = data['total_assets']
        if 'servers' in data:
            customer.servers = data['servers']
        if 'patch_compliance' in data:
            customer.patch_compliance = data['patch_compliance']
        if 'backup_success' in data:
            customer.backup_success = data['backup_success']
        if 'edr_coverage' in data:
            customer.edr_coverage = data['edr_coverage']
        if 'sla_attainment' in data:
            customer.sla_attainment = data['sla_attainment']
        
        db.session.commit()
        
        return jsonify({'success': True, 'customer': customer.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer"""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'success': False, 'message': 'Customer not found'}), 404
        
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Customer deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/generate-ai-readiness', methods=['POST'])
def generate_ai_readiness():
    """Generate AI Readiness Assessment"""
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        
        if not customer_id:
            return jsonify({'success': False, 'message': 'Customer ID required'}), 400
        
        # For now, return success with placeholder
        # In production, this would generate a full AI readiness report
        return jsonify({
            'success': True,
            'message': 'AI Readiness assessment feature coming soon!',
            'customer_id': customer_id
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Initialize lifecycle routes
lifecycle_bp = init_lifecycle_routes(app, db)
app.register_blueprint(lifecycle_bp)

# Add client overview route
@app.route('/client/<customer_id>')
def client_overview(customer_id):
    """Client overview page"""
    from app.lifecycle_models import ClientSegmentation
    
    customer = Customer.query.filter_by(customer_id=customer_id).first_or_404()
    segment = ClientSegmentation.query.filter_by(customer_id=customer_id).first()
    
    return render_template('client_overview.html', 
                         customer=customer.to_dict(),
                         segment=segment.to_dict() if segment else {})

# Add meetings hub route
@app.route('/meetings')
def meetings_hub():
    """Meetings hub page"""
    return render_template('meetings_hub.html')

if __name__ == '__main__':
    app.run(host='0.0.0', port=5000, debug=True)

