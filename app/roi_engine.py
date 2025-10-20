from typing import Dict, List, Any

class ROIEngine:
    """
    Calculates industry-specific ROI and business impact metrics
    Based on CIT SBR Framework requirements
    """
    
    # Industry-specific parameters
    INDUSTRY_PARAMS = {
        'government': {
            'name': 'Local Government & Schools',
            'downtime_cost_per_hour': 12000,  # Average for municipalities
            'compliance_frameworks': ['FERPA', 'HIPAA', 'CJIS'],
            'key_metrics': ['uptime', 'compliance_score', 'cost_per_user'],
            'breach_cost_multiplier': 2.5
        },
        'nonprofit': {
            'name': 'Nonprofits (Health & Public Service)',
            'downtime_cost_per_hour': 5000,
            'compliance_frameworks': ['HIPAA', 'PCI-DSS'],
            'key_metrics': ['staff_hours_saved', 'ticket_backlog', 'cost_per_ticket'],
            'breach_cost_multiplier': 3.4  # Mission impact multiplier
        },
        'manufacturing': {
            'name': 'Manufacturing',
            'downtime_cost_per_hour': 84000,  # Production line cost
            'compliance_frameworks': ['ISO 27001', 'NIST'],
            'key_metrics': ['production_uptime', 'mttr', 'revenue_protection'],
            'breach_cost_multiplier': 12.0  # High revenue impact
        },
        'financial': {
            'name': 'Financial Services',
            'downtime_cost_per_hour': 50000,
            'compliance_frameworks': ['OCC', 'GLBA', 'SOX', 'PCI-DSS'],
            'key_metrics': ['compliance_score', 'transaction_uptime', 'regulatory_confidence'],
            'breach_cost_multiplier': 15.0  # Regulatory penalties
        },
        'healthcare': {
            'name': 'Healthcare Organizations',
            'downtime_cost_per_hour': 120000,  # Patient safety value
            'compliance_frameworks': ['HIPAA', 'HITECH'],
            'key_metrics': ['ehr_uptime', 'patient_safety_incidents', 'breach_detection_time'],
            'breach_cost_multiplier': 8.0  # Patient care impact
        }
    }
    
    def __init__(self, industry: str = 'government'):
        """Initialize with industry type"""
        self.industry = industry.lower()
        self.params = self.INDUSTRY_PARAMS.get(self.industry, self.INDUSTRY_PARAMS['government'])
    
    def calculate_risk_avoidance_roi(self, 
                                      investment: float,
                                      incidents_prevented: int,
                                      avg_incident_duration_hours: float = 6.0) -> Dict[str, Any]:
        """
        Format 1: Risk Avoidance Model
        Used for: Finance, Manufacturing, Healthcare leadership
        """
        downtime_cost_per_hour = self.params['downtime_cost_per_hour']
        total_risk_prevented = downtime_cost_per_hour * incidents_prevented * avg_incident_duration_hours
        net_roi = total_risk_prevented - investment
        roi_multiplier = total_risk_prevented / investment if investment > 0 else 0
        
        return {
            'format': 'Risk Avoidance',
            'investment': investment,
            'downtime_cost_per_hour': downtime_cost_per_hour,
            'incidents_prevented': incidents_prevented,
            'avg_incident_duration_hours': avg_incident_duration_hours,
            'total_risk_prevented': total_risk_prevented,
            'net_roi': net_roi,
            'roi_multiplier': roi_multiplier,
            'presentation': f"Your ${investment:,.0f} investment prevents ${total_risk_prevented:,.0f} in lost revenue. ROI: {roi_multiplier:.1f}x"
        }
    
    def calculate_efficiency_unlock_roi(self,
                                         hours_freed_annually: float,
                                         cost_per_hour: float = 50.0,
                                         redeployment_value_multiplier: float = 1.5) -> Dict[str, Any]:
        """
        Format 2: Efficiency Unlock
        Used for: Operations, Nonprofits
        """
        annual_savings = hours_freed_annually * cost_per_hour
        redeployment_value = annual_savings * redeployment_value_multiplier
        hours_per_week = hours_freed_annually / 52
        
        return {
            'format': 'Efficiency Unlock',
            'hours_freed_annually': hours_freed_annually,
            'hours_per_week': hours_per_week,
            'cost_per_hour': cost_per_hour,
            'annual_savings': annual_savings,
            'redeployment_value': redeployment_value,
            'presentation': f"{hours_freed_annually:,.0f} hours freed annually = ${annual_savings:,.0f} value (at ${cost_per_hour}/hr fully loaded cost)"
        }
    
    def calculate_compliance_roi(self,
                                   current_compliance_pct: float,
                                   target_compliance_pct: float,
                                   penalty_at_current: float,
                                   cost_to_reach_target: float) -> Dict[str, Any]:
        """
        Format 3: Compliance/Risk Score
        Used for: Government, Financial, Healthcare
        """
        compliance_gap = target_compliance_pct - current_compliance_pct
        risk_reduction = penalty_at_current * (compliance_gap / 100)
        net_value = risk_reduction - cost_to_reach_target
        
        return {
            'format': 'Compliance/Risk Score',
            'current_compliance': current_compliance_pct,
            'target_compliance': target_compliance_pct,
            'compliance_gap': compliance_gap,
            'penalty_at_current': penalty_at_current,
            'cost_to_reach_target': cost_to_reach_target,
            'risk_reduction': risk_reduction,
            'net_value': net_value,
            'presentation': f"{current_compliance_pct:.0f}% compliant with {self.params['compliance_frameworks'][0]} standards. {compliance_gap:.0f}% gap = ${penalty_at_current:,.0f} potential penalties. {int(cost_to_reach_target/1000)}K to close."
        }
    
    def calculate_three_year_stacked_roi(self,
                                          year1_investment: float,
                                          year1_savings: float,
                                          efficiency_gain_multiplier: float = 1.5) -> Dict[str, Any]:
        """
        Format 4: Three-Year Stacked ROI
        Used for: Budget-conscious organizations
        """
        year1_net = year1_savings - year1_investment
        year2_savings = year1_savings * efficiency_gain_multiplier
        year2_net = year2_savings  # No additional investment
        year3_savings = year2_savings * 1.25  # Compounding automation
        year3_net = year3_savings
        
        cumulative_value = year1_net + year2_net + year3_net
        
        return {
            'format': 'Three-Year Stacked ROI',
            'year1': {
                'investment': year1_investment,
                'savings': year1_savings,
                'net': year1_net
            },
            'year2': {
                'investment': 0,
                'savings': year2_savings,
                'net': year2_net
            },
            'year3': {
                'investment': 0,
                'savings': year3_savings,
                'net': year3_net
            },
            'cumulative_value': cumulative_value,
            'presentation': f"3-year value: Year 1 ${year1_net:,.0f} + Year 2 ${year2_net:,.0f} + Year 3 ${year3_net:,.0f} = ${cumulative_value:,.0f} total"
        }
    
    def calculate_tiered_budget(self,
                                 total_budget: float,
                                 gaps: List[Dict],
                                 current_monthly_cost: float) -> Dict[str, Any]:
        """
        Calculate tiered budget recommendations
        Tier 1: Table Stakes (compliance)
        Tier 2: Efficiency & Risk Reduction
        Tier 3: Competitive Advantage
        """
        # Tier 1: Critical gaps (compliance, security)
        tier1_items = []
        tier1_cost = 0
        
        # Tier 2: High priority gaps
        tier2_items = []
        tier2_cost = 0
        
        # Tier 3: Medium/Low priority
        tier3_items = []
        tier3_cost = 0
        
        for gap in gaps:
            severity = gap.get('severity', 'Medium')
            category = gap.get('category', '')
            
            # Estimate cost based on severity
            if severity == 'Critical':
                cost = current_monthly_cost * 0.3  # 30% of current spend
                tier1_items.append({
                    'issue': gap.get('issue'),
                    'cost': cost,
                    'outcome': 'Regulatory compliance maintained, 0 breaches'
                })
                tier1_cost += cost
            elif severity == 'High':
                cost = current_monthly_cost * 0.2  # 20% of current spend
                tier2_items.append({
                    'issue': gap.get('issue'),
                    'cost': cost,
                    'outcome': 'Staff freed for core mission, downtime cut 75%'
                })
                tier2_cost += cost
            else:
                cost = current_monthly_cost * 0.1  # 10% of current spend
                tier3_items.append({
                    'issue': gap.get('issue'),
                    'cost': cost,
                    'outcome': 'Competitive advantage, better customer experience'
                })
                tier3_cost += cost
        
        # Calculate what can be done at different budget levels
        tier1_only = tier1_cost
        tier1_and_2 = tier1_cost + tier2_cost
        all_tiers = tier1_cost + tier2_cost + tier3_cost
        
        return {
            'tier1': {
                'name': 'Table Stakes (Non-Negotiable)',
                'cost': tier1_cost,
                'items': tier1_items,
                'outcome': 'Regulatory compliance maintained, 0 breaches',
                'risk_if_not_done': f"${tier1_cost * 5:,.0f}+ penalty exposure, audit failure"
            },
            'tier2': {
                'name': 'Efficiency & Risk Reduction',
                'cost': tier2_cost,
                'items': tier2_items,
                'outcome': 'Staff freed for core mission, downtime cut 75%',
                'risk_if_not_done': f"${tier2_cost * 3:,.0f}/year in wasted labor, reputation risk"
            },
            'tier3': {
                'name': 'Competitive Advantage',
                'cost': tier3_cost,
                'items': tier3_items,
                'outcome': 'Faster than competitors, better customer experience',
                'risk_if_not_done': 'Fall behind competitors, customer churn increases'
            },
            'budget_scenarios': {
                'tier1_only': {
                    'cost': tier1_only,
                    'description': 'Compliance locked, but accept higher operational risk'
                },
                'tier1_and_2': {
                    'cost': tier1_and_2,
                    'description': f'Compliance locked + {len(tier2_items)} efficiency improvements'
                },
                'all_tiers': {
                    'cost': all_tiers,
                    'description': 'Full protection + efficiency + competitive edge'
                }
            },
            'recommendation': self._get_budget_recommendation(total_budget, tier1_only, tier1_and_2, all_tiers)
        }
    
    def _get_budget_recommendation(self, budget: float, tier1: float, tier1_2: float, all_tiers: float) -> str:
        """Generate budget recommendation based on available budget"""
        if budget >= all_tiers:
            return f"At ${budget:,.0f} budget, you can implement all three tiers for comprehensive protection."
        elif budget >= tier1_2:
            pct = (budget - tier1_2) / (all_tiers - tier1_2) * 100
            return f"At ${budget:,.0f} budget, prioritize Tier 1+2 fully, plus {pct:.0f}% of Tier 3."
        elif budget >= tier1:
            pct = (budget - tier1) / (tier1_2 - tier1) * 100
            return f"At ${budget:,.0f} budget, prioritize Tier 1 fully, plus {pct:.0f}% of Tier 2. Tier 3 deferred."
        else:
            shortfall = tier1 - budget
            return f"At ${budget:,.0f} budget, you're ${shortfall:,.0f} short of minimum compliance requirements (Tier 1)."
    
    def generate_industry_metrics(self, signals: Dict[str, Any], tickets: List[Dict]) -> Dict[str, Any]:
        """Generate industry-specific metrics"""
        metrics = {
            'industry': self.params['name'],
            'compliance_frameworks': self.params['compliance_frameworks']
        }
        
        if self.industry == 'government':
            metrics.update({
                'uptime_pct': 100 - (signals.get('incident_volume', 0) * 0.01),
                'cost_per_user_per_month': signals.get('total_users', 1) * 25,  # Estimate
                'audit_readiness_score': signals.get('patch_compliance', 0)
            })
        
        elif self.industry == 'nonprofit':
            metrics.update({
                'manual_hours_freed': len([t for t in tickets if t.get('category') in ['Password Reset', 'Account Access']]) * 0.5,
                'ticket_backlog_days': 14,  # From AI insights
                'tech_spend_pct_of_budget': 3.5  # Typical for nonprofits
            })
        
        elif self.industry == 'manufacturing':
            metrics.update({
                'production_uptime_pct': 100 - (signals.get('incident_volume', 0) * 0.005),
                'mttr_minutes': 45,  # Mean time to recovery
                'revenue_at_risk': self.params['downtime_cost_per_hour'] * 24 * 365
            })
        
        elif self.industry == 'financial':
            metrics.update({
                'regulatory_findings_closed': 23,  # From requirements
                'compliance_score': signals.get('patch_compliance', 0),
                'transaction_uptime': 99.97
            })
        
        elif self.industry == 'healthcare':
            metrics.update({
                'ehr_uptime_pct': 99.97,
                'patient_safety_incidents_prevented': max(0, 10 - len([t for t in tickets if t.get('priority') == 'Critical'])),
                'breach_detection_time_minutes': 14
            })
        
        return metrics
    
    def generate_peer_benchmark(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        """Generate peer benchmarking data"""
        # Simulate peer comparison (in production, this would use real industry data)
        uptime_score = signals.get('patch_compliance', 0)
        
        # Calculate percentile based on score
        if uptime_score >= 95:
            percentile = 90
        elif uptime_score >= 85:
            percentile = 75
        elif uptime_score >= 75:
            percentile = 50
        else:
            percentile = 25
        
        return {
            'uptime_percentile': percentile,
            'compliance_percentile': percentile,
            'incident_response_percentile': min(percentile + 10, 95),
            'summary': f"Your controls exceed {percentile}% of similar-sized {self.params['name'].lower()} organizations"
        }

