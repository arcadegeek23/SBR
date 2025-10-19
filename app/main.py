from flask import Flask, render_template, request, jsonify, send_file
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

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config.from_object(Config)

# Initialize database
db.init_app(app)

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
    return render_template('index.html')

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
        
        # Step 8: Generate reports
        report_paths = report_builder.generate_report(
            customer_id=customer_id,
            customer_name=customer.get('name', 'Unknown'),
            signals=signals,
            nist_scores=nist_scores,
            gaps=gaps,
            recommendations=recommendations,
            budget=budget,
            ai_insights=ai_insights
        )
        
        # Step 9: Save to database
        report_run = ReportRun(
            customer_id=customer_id,
            customer_name=customer.get('name', 'Unknown'),
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

