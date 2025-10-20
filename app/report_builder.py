from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import markdown
import os
from weasyprint import HTML

class ReportBuilder:
    """Generates reports in multiple formats"""
    
    def __init__(self, templates_dir: str, reports_dir: str):
        self.templates_dir = templates_dir
        self.reports_dir = reports_dir
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Ensure reports directory exists
        os.makedirs(reports_dir, exist_ok=True)
    
    def generate_report(self, customer_id: str, customer_name: str, signals: dict, 
                       nist_scores: dict, gaps: list, recommendations: list, 
                       budget: dict, ai_insights: dict = None, roi_data: dict = None, 
                       stakeholder_data: dict = None) -> dict:
        """
        Generate report in all formats
        
        Returns:
            Dict with paths to generated reports
        """
        # Prepare template context
        context = {
            'customer_id': customer_id,
            'customer_name': customer_name,
            'generated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p'),
            'review_period': 'Last 90 Days',
            'signals': signals,
            'nist_scores': nist_scores,
            'overall_score': nist_scores.get('Overall', 0),
            'gaps': gaps,
            'recommendations': recommendations,
            'budget': budget,
            'ai_insights': ai_insights or {},
            'roi_data': roi_data or {},
            'stakeholder_data': stakeholder_data or {}
        }
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_filename = f"sbr_{customer_id}_{timestamp}"
        
        # Generate Markdown
        md_path = self._generate_markdown(base_filename, context)
        
        # Generate HTML
        html_path = self._generate_html(base_filename, context)
        
        # Generate PDF
        pdf_path = self._generate_pdf(base_filename, html_path)
        
        return {
            'markdown': md_path,
            'html': html_path,
            'pdf': pdf_path
        }
    
    def _generate_markdown(self, filename: str, context: dict) -> str:
        """Generate Markdown report"""
        template = self.env.get_template('report_template.md')
        content = template.render(**context)
        
        filepath = os.path.join(self.reports_dir, f"{filename}.md")
        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath
    
    def _generate_html(self, filename: str, context: dict) -> str:
        """Generate HTML report"""
        template = self.env.get_template('report_template.html')
        content = template.render(**context)
        
        filepath = os.path.join(self.reports_dir, f"{filename}.html")
        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath
    
    def _generate_pdf(self, filename: str, html_path: str) -> str:
        """Generate PDF report from HTML"""
        try:
            pdf_path = os.path.join(self.reports_dir, f"{filename}.pdf")
            HTML(filename=html_path).write_pdf(pdf_path)
            return pdf_path
        except Exception as e:
            print(f"PDF generation failed: {e}")
            return None

