from typing import Dict, List, Any
from datetime import datetime

class StakeholderContentGenerator:
    """
    Generates stakeholder-specific content for SBRs
    - Executive one-pager
    - Board/C-suite talking points
    - Budget justification template
    - Monthly accountability scorecard
    """
    
    def generate_executive_onepager(self,
                                      customer_name: str,
                                      overall_score: float,
                                      roi_data: Dict,
                                      top_risks: List[Dict],
                                      top_recommendations: List[Dict]) -> Dict[str, Any]:
        """
        Generate one-pager for executives (30 seconds to read)
        Format: Visual + 3 bullets per section
        """
        return {
            'title': f'Executive Summary: {customer_name} IT Security Review',
            'date': datetime.now().strftime('%B %d, %Y'),
            'overall_score': overall_score,
            'score_status': self._get_score_status(overall_score),
            
            'what_we_found': [
                f"Security posture at {overall_score:.1f}% - {self._get_score_status(overall_score)}",
                f"{len(top_risks)} critical gaps identified requiring immediate attention",
                f"${roi_data.get('total_risk_prevented', 0):,.0f} in potential losses prevented this quarter"
            ],
            
            'the_risk': [
                top_risks[0]['issue'] if len(top_risks) > 0 else 'No critical risks identified',
                top_risks[1]['issue'] if len(top_risks) > 1 else '',
                f"Estimated exposure: ${sum([r.get('financial_impact', 0) for r in top_risks[:3]]):,.0f}"
            ],
            
            'the_cost': [
                f"Investment required: ${roi_data.get('investment_required', 0):,.0f}",
                f"Timeline: {roi_data.get('timeline', '6-12 months')}",
                f"Monthly cost: ${roi_data.get('monthly_cost', 0):,.0f}"
            ],
            
            'the_roi': [
                roi_data.get('presentation', 'ROI analysis included in full report'),
                f"Payback period: {roi_data.get('payback_months', 12)} months",
                f"3-year value: ${roi_data.get('three_year_value', 0):,.0f}"
            ]
        }
    
    def generate_board_talking_points(self,
                                       customer_name: str,
                                       industry: str,
                                       key_metrics: Dict,
                                       peer_benchmark: Dict,
                                       incidents_prevented: int) -> List[Dict[str, str]]:
        """
        Generate board/C-suite talking points (in their words, not technical)
        """
        return [
            {
                'category': 'Performance',
                'talking_point': f"Our infrastructure prevented {incidents_prevented} potential incidents worth ${key_metrics.get('risk_prevented', 0):,.0f} this quarter",
                'context': 'This demonstrates proactive security management and risk mitigation'
            },
            {
                'category': 'Peer Comparison',
                'talking_point': f"We rank in the top {100 - peer_benchmark.get('uptime_percentile', 50)}% for uptime compared to similar {industry} organizations",
                'context': peer_benchmark.get('summary', 'Industry benchmarking analysis included')
            },
            {
                'category': 'Compliance',
                'talking_point': f"We maintain {key_metrics.get('compliance_score', 0):.0f}% compliance with {key_metrics.get('primary_framework', 'industry standards')}",
                'context': 'Regulatory audit-ready with documented controls'
            },
            {
                'category': 'Operational Excellence',
                'talking_point': f"IT operations freed {key_metrics.get('hours_saved', 0):,.0f} staff hours this year through automation",
                'context': f"Value: ${key_metrics.get('efficiency_value', 0):,.0f} redirected to mission-critical work"
            },
            {
                'category': 'Risk Management',
                'talking_point': f"Current security investment provides {key_metrics.get('roi_multiplier', 0):.1f}x return through risk avoidance",
                'context': 'Every dollar invested prevents multiple dollars in potential losses'
            }
        ]
    
    def generate_budget_justification(self,
                                       tiered_budget: Dict,
                                       current_state: Dict,
                                       target_state: Dict) -> Dict[str, Any]:
        """
        Generate budget justification template for internal presentation
        Shows trade-offs, compliance risks, competitive positioning
        """
        return {
            'title': 'IT Security Budget Justification',
            'current_state': {
                'compliance_level': f"{current_state.get('compliance_pct', 0):.0f}%",
                'security_posture': current_state.get('posture_description', 'Needs Improvement'),
                'known_gaps': current_state.get('gap_count', 0),
                'risk_exposure': f"${current_state.get('risk_exposure', 0):,.0f}"
            },
            'target_state': {
                'compliance_level': f"{target_state.get('compliance_pct', 100):.0f}%",
                'security_posture': target_state.get('posture_description', 'Strong'),
                'gaps_closed': target_state.get('gaps_closed', 0),
                'risk_reduction': f"${target_state.get('risk_reduction', 0):,.0f}"
            },
            'budget_options': [
                {
                    'tier': 'Tier 1 Only (Minimum Compliance)',
                    'cost': f"${tiered_budget['tier1']['cost']:,.0f}",
                    'what_you_get': tiered_budget['tier1']['outcome'],
                    'what_you_dont_get': 'Efficiency improvements, competitive advantages',
                    'risk_if_not_approved': tiered_budget['tier1']['risk_if_not_done']
                },
                {
                    'tier': 'Tier 1 + 2 (Recommended)',
                    'cost': f"${tiered_budget['tier1']['cost'] + tiered_budget['tier2']['cost']:,.0f}",
                    'what_you_get': f"{tiered_budget['tier1']['outcome']} + {tiered_budget['tier2']['outcome']}",
                    'what_you_dont_get': 'Advanced automation, competitive edge features',
                    'risk_if_not_approved': 'Operational inefficiency continues, higher long-term costs'
                },
                {
                    'tier': 'All Tiers (Full Protection)',
                    'cost': f"${tiered_budget['tier1']['cost'] + tiered_budget['tier2']['cost'] + tiered_budget['tier3']['cost']:,.0f}",
                    'what_you_get': 'Complete security + efficiency + competitive advantages',
                    'what_you_dont_get': 'Nothing - comprehensive coverage',
                    'risk_if_not_approved': 'N/A'
                }
            ],
            'recommendation': tiered_budget.get('recommendation', 'Tier 1+2 recommended for balanced protection and efficiency'),
            'trade_off_statement': self._generate_tradeoff_statement(tiered_budget)
        }
    
    def generate_monthly_scorecard(self,
                                     customer_name: str,
                                     month: str,
                                     metrics: Dict,
                                     targets: Dict,
                                     ytd_roi: Dict) -> Dict[str, Any]:
        """
        Generate monthly accountability scorecard
        Tracks progress toward outcomes between reviews
        """
        return {
            'title': f'Monthly Performance Card | {customer_name}',
            'month': month,
            'metrics': [
                {
                    'name': 'System Uptime',
                    'actual': f"{metrics.get('uptime_pct', 0):.2f}%",
                    'target': f"{targets.get('uptime_pct', 99.9):.2f}%",
                    'status': '✅' if metrics.get('uptime_pct', 0) >= targets.get('uptime_pct', 99.9) else '⚠️',
                    'impact': f"Prevented {metrics.get('incidents_prevented', 0)} potential incidents worth ${metrics.get('incidents_value', 0):,.0f}"
                },
                {
                    'name': 'Security Incidents Blocked',
                    'actual': metrics.get('incidents_blocked', 0),
                    'target': targets.get('incidents_blocked', 8),
                    'status': '✅' if metrics.get('incidents_blocked', 0) >= targets.get('incidents_blocked', 8) else '⚠️',
                    'impact': f"{metrics.get('incidents_blocked', 0)} incidents stopped before reaching systems"
                },
                {
                    'name': 'Maintenance Window Impact',
                    'actual': f"{metrics.get('maintenance_downtime_min', 0)} minutes",
                    'target': f"< {targets.get('maintenance_downtime_min', 5)} minutes",
                    'status': '✅' if metrics.get('maintenance_downtime_min', 0) <= targets.get('maintenance_downtime_min', 5) else '⚠️',
                    'impact': 'All patches applied during scheduled downtime'
                },
                {
                    'name': 'Staff Hours Freed',
                    'actual': f"{metrics.get('hours_freed', 0):.0f} hours",
                    'target': f"{targets.get('hours_freed', 20):.0f} hours",
                    'status': '✅' if metrics.get('hours_freed', 0) >= targets.get('hours_freed', 20) else '⚠️',
                    'impact': f"${metrics.get('hours_freed', 0) * 50:,.0f} value redirected to mission work"
                }
            ],
            'ytd_summary': {
                'roi_value': f"${ytd_roi.get('total_value', 0):,.0f} in risk prevented",
                'investment_ytd': f"${ytd_roi.get('investment', 0):,.0f}",
                'net_value': f"${ytd_roi.get('net_value', 0):,.0f}",
                'roi_multiplier': f"{ytd_roi.get('multiplier', 0):.1f}x"
            },
            'next_steps': 'Board presentation scheduled. You\'re in great shape.',
            'trend': '📈' if metrics.get('trend', 'improving') == 'improving' else '📉'
        }
    
    def generate_three_tier_content(self,
                                     customer_name: str,
                                     overall_score: float,
                                     roi_data: Dict,
                                     peer_benchmark: Dict,
                                     progress_metrics: Dict) -> Dict[str, Any]:
        """
        Generate three-tier content for different audiences
        Tier A: Internal Use (what they tell their boss)
        Tier B: Peer Credibility (what they say in industry groups)
        Tier C: Their Team's Motivation (what their IT staff sees)
        """
        return {
            'tier_a_internal': {
                'audience': 'Internal Leadership',
                'scorecard': {
                    'overall_score': f"{overall_score:.1f}%",
                    'status': self._get_score_status(overall_score),
                    'trend': progress_metrics.get('trend', 'Improving')
                },
                'roi_summary': roi_data.get('presentation', ''),
                'forward_looking': f"Next quarter we're targeting {overall_score + 10:.0f}% overall score through {len(progress_metrics.get('initiatives', []))} key initiatives"
            },
            'tier_b_peer': {
                'audience': 'Industry Peers',
                'benchmarking': peer_benchmark.get('summary', ''),
                'case_study': f"How we prevented ${roi_data.get('total_risk_prevented', 0):,.0f} in downtime through proactive security",
                'industry_context': f"We exceed industry standards by {overall_score - 70:.0f}%"
            },
            'tier_c_team': {
                'audience': 'IT Staff',
                'progress_dashboard': f"You prevented {progress_metrics.get('incidents_blocked', 0)} incidents this month",
                'skill_building': f"Next month we're implementing {progress_metrics.get('next_initiative', 'automation improvements')}",
                'recognition': f"Your work directly enabled ${progress_metrics.get('value_created', 0):,.0f} in efficiency savings"
            }
        }
    
    def _get_score_status(self, score: float) -> str:
        """Get status description based on score"""
        if score >= 90:
            return 'Excellent'
        elif score >= 75:
            return 'Good'
        elif score >= 60:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def _generate_tradeoff_statement(self, tiered_budget: Dict) -> str:
        """Generate trade-off statement for budget justification"""
        tier1_cost = tiered_budget['tier1']['cost']
        tier2_cost = tiered_budget['tier2']['cost']
        total_12 = tier1_cost + tier2_cost
        
        return f"We can implement Tier 1+2 for ${total_12:,.0f} (compliance + efficiency improvements). OR Tier 1 only for ${tier1_cost:,.0f} and accept higher operational risk and costs."

