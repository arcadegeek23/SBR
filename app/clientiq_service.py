"""
ClientIQ - AI-Powered Client Intelligence Service
Generates AI summaries and meeting prep using Azure OpenAI
"""
import os
import json
from datetime import datetime, timedelta
from openai import AzureOpenAI

class ClientIQService:
    """AI-powered client intelligence and meeting preparation"""
    
    def __init__(self, azure_endpoint=None, azure_api_key=None, deployment_name=None):
        """Initialize ClientIQ with Azure OpenAI credentials"""
        self.azure_endpoint = azure_endpoint or os.getenv('AZURE_OPENAI_ENDPOINT')
        self.azure_api_key = azure_api_key or os.getenv('AZURE_OPENAI_API_KEY')
        self.deployment_name = deployment_name or os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4')
        
        self.client = None
        if self.azure_endpoint and self.azure_api_key:
            try:
                self.client = AzureOpenAI(
                    azure_endpoint=self.azure_endpoint,
                    api_key=self.azure_api_key,
                    api_version="2024-02-15-preview"
                )
            except Exception as e:
                print(f"Failed to initialize Azure OpenAI client: {e}")
    
    def generate_client_summary(self, customer_data, reports, meetings, goals, agreements):
        """
        Generate AI-powered client summary
        
        Args:
            customer_data: Customer information dict
            reports: List of recent reports
            meetings: List of recent meetings
            goals: List of client goals
            agreements: List of client agreements
        
        Returns:
            dict with summary sections
        """
        if not self.client:
            return self._generate_mock_summary(customer_data)
        
        # Prepare context for AI
        context = self._prepare_context(customer_data, reports, meetings, goals, agreements)
        
        try:
            # Generate summary using Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": f"Generate a comprehensive client summary for:\n\n{context}"}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            summary_text = response.choices[0].message.content
            
            # Parse and structure the summary
            return self._parse_summary(summary_text, customer_data)
            
        except Exception as e:
            print(f"Error generating AI summary: {e}")
            return self._generate_mock_summary(customer_data)
    
    def generate_meeting_prep(self, customer_data, meeting_type='qbr'):
        """
        Generate AI-powered meeting preparation
        
        Args:
            customer_data: Customer information dict with recent activity
            meeting_type: Type of meeting (qbr, planning, review, etc.)
        
        Returns:
            dict with meeting prep sections
        """
        if not self.client:
            return self._generate_mock_meeting_prep(customer_data, meeting_type)
        
        try:
            prompt = self._get_meeting_prep_prompt(customer_data, meeting_type)
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert MSP account manager preparing for client meetings."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            prep_text = response.choices[0].message.content
            return self._parse_meeting_prep(prep_text, meeting_type)
            
        except Exception as e:
            print(f"Error generating meeting prep: {e}")
            return self._generate_mock_meeting_prep(customer_data, meeting_type)
    
    def generate_insights(self, customer_data, reports):
        """
        Generate AI insights from customer data and reports
        
        Args:
            customer_data: Customer information
            reports: Recent reports
        
        Returns:
            list of insight dicts
        """
        if not self.client:
            return self._generate_mock_insights(customer_data)
        
        try:
            context = f"""
            Customer: {customer_data.get('name')}
            Industry: {customer_data.get('industry')}
            Recent Reports: {len(reports)}
            Latest Security Score: {reports[0].get('overall_score') if reports else 'N/A'}
            """
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are an AI analyst identifying key insights and recommendations for MSP clients."},
                    {"role": "user", "content": f"Analyze this client data and provide 3-5 key insights:\n\n{context}"}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            insights_text = response.choices[0].message.content
            return self._parse_insights(insights_text)
            
        except Exception as e:
            print(f"Error generating insights: {e}")
            return self._generate_mock_insights(customer_data)
    
    def _get_system_prompt(self):
        """Get system prompt for client summary generation"""
        return """You are ClientIQ, an AI assistant for MSPs that generates comprehensive client summaries.
        
Your summaries should include:
1. Executive Overview - High-level client status
2. Recent Activity - Key events and changes
3. Health Assessment - Overall client health and risks
4. Key Metrics - Important KPIs and trends
5. Action Items - Recommended next steps

Be concise, professional, and actionable. Focus on insights that help account managers prepare for client interactions."""
    
    def _prepare_context(self, customer_data, reports, meetings, goals, agreements):
        """Prepare context string for AI"""
        context_parts = []
        
        # Customer info
        context_parts.append(f"Client: {customer_data.get('name')}")
        context_parts.append(f"Industry: {customer_data.get('industry')}")
        
        # Recent reports
        if reports:
            latest_report = reports[0]
            context_parts.append(f"Latest Security Score: {latest_report.get('overall_score', 0):.1f}%")
            context_parts.append(f"Identified Gaps: {len(latest_report.get('gaps', []))}")
        
        # Meetings
        if meetings:
            context_parts.append(f"Recent Meetings: {len(meetings)}")
            context_parts.append(f"Last Meeting: {meetings[0].get('scheduled_date', 'N/A')}")
        
        # Goals
        if goals:
            active_goals = [g for g in goals if g.get('status') != 'completed']
            context_parts.append(f"Active Goals: {len(active_goals)}")
        
        # Agreements
        if agreements:
            total_mrr = sum(a.get('monthly_mrr', 0) for a in agreements)
            context_parts.append(f"Total MRR: ${total_mrr:,.2f}")
        
        return "\n".join(context_parts)
    
    def _parse_summary(self, summary_text, customer_data):
        """Parse AI-generated summary into structured format"""
        return {
            'customer_name': customer_data.get('name'),
            'generated_at': datetime.utcnow().isoformat(),
            'summary': summary_text,
            'sections': {
                'overview': self._extract_section(summary_text, 'overview'),
                'recent_activity': self._extract_section(summary_text, 'activity'),
                'health': self._extract_section(summary_text, 'health'),
                'metrics': self._extract_section(summary_text, 'metrics'),
                'actions': self._extract_section(summary_text, 'action')
            }
        }
    
    def _extract_section(self, text, keyword):
        """Extract section from summary text"""
        # Simple extraction - in production, use better parsing
        lines = text.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if keyword.lower() in line.lower():
                in_section = True
            elif in_section and line.strip().startswith(('##', '**', '-')):
                break
            elif in_section:
                section_lines.append(line)
        
        return '\n'.join(section_lines).strip() if section_lines else text[:200]
    
    def _get_meeting_prep_prompt(self, customer_data, meeting_type):
        """Generate meeting prep prompt"""
        return f"""
Prepare meeting notes for a {meeting_type.upper()} with {customer_data.get('name')}.

Include:
1. Meeting objectives
2. Key discussion topics
3. Questions to ask
4. Recommended talking points
5. Potential upsell opportunities

Customer Context:
- Industry: {customer_data.get('industry')}
- Current Status: {customer_data.get('health_status', 'Active')}
- MRR: ${customer_data.get('total_mrr', 0):,.2f}
"""
    
    def _parse_meeting_prep(self, prep_text, meeting_type):
        """Parse meeting prep into structured format"""
        return {
            'meeting_type': meeting_type,
            'generated_at': datetime.utcnow().isoformat(),
            'prep_notes': prep_text,
            'objectives': self._extract_list(prep_text, 'objective'),
            'topics': self._extract_list(prep_text, 'topic'),
            'questions': self._extract_list(prep_text, 'question'),
            'talking_points': self._extract_list(prep_text, 'talking point')
        }
    
    def _extract_list(self, text, keyword):
        """Extract bulleted list items containing keyword"""
        lines = text.split('\n')
        items = []
        for line in lines:
            if keyword.lower() in line.lower() or line.strip().startswith(('-', '*', '•')):
                clean_line = line.strip().lstrip('-*•').strip()
                if clean_line:
                    items.append(clean_line)
        return items[:5]  # Return top 5
    
    def _parse_insights(self, insights_text):
        """Parse insights into structured list"""
        insights = []
        lines = insights_text.split('\n')
        
        for line in lines:
            if line.strip().startswith(('-', '*', '•', '1', '2', '3', '4', '5')):
                clean_line = line.strip().lstrip('-*•123456789.').strip()
                if clean_line:
                    insights.append({
                        'insight': clean_line,
                        'category': 'general',
                        'priority': 'medium'
                    })
        
        return insights[:5]
    
    def _generate_mock_summary(self, customer_data):
        """Generate mock summary when AI is not available"""
        return {
            'customer_name': customer_data.get('name'),
            'generated_at': datetime.utcnow().isoformat(),
            'summary': f"Client summary for {customer_data.get('name')} - AI Insights unavailable (configure Azure OpenAI in admin panel)",
            'sections': {
                'overview': f"{customer_data.get('name')} is an active client in the {customer_data.get('industry', 'general')} industry.",
                'recent_activity': "Recent activity data will appear here when AI Insights is configured.",
                'health': "Client health assessment requires Azure OpenAI configuration.",
                'metrics': "Key metrics will be displayed when AI analysis is enabled.",
                'actions': "Recommended actions will be generated by AI when configured."
            }
        }
    
    def _generate_mock_meeting_prep(self, customer_data, meeting_type):
        """Generate mock meeting prep"""
        return {
            'meeting_type': meeting_type,
            'generated_at': datetime.utcnow().isoformat(),
            'prep_notes': f"Meeting preparation for {customer_data.get('name')} - Configure Azure OpenAI for AI-generated prep",
            'objectives': ["Review client status", "Discuss upcoming initiatives"],
            'topics': ["Security posture", "Budget planning", "Goal progress"],
            'questions': ["What are your top priorities?", "Any concerns we should address?"],
            'talking_points': ["Recent improvements", "Recommended next steps"]
        }
    
    def _generate_mock_insights(self, customer_data):
        """Generate mock insights"""
        return [
            {
                'insight': f"{customer_data.get('name')} requires Azure OpenAI configuration for AI-generated insights",
                'category': 'configuration',
                'priority': 'high'
            },
            {
                'insight': "Configure Azure OpenAI in the admin panel to enable ClientIQ features",
                'category': 'setup',
                'priority': 'high'
            }
        ]

