"""
Client Segmentation Service
Auto-calculates client tiers based on MRR and other metrics
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class SegmentationService:
    """Auto-calculate client segmentation and tiers based on MRR"""
    
    # MRR Tier Thresholds (configurable)
    TIER_THRESHOLDS = {
        'platinum': 10000,  # $10k+ MRR
        'gold': 5000,       # $5k-$10k MRR
        'silver': 2000,     # $2k-$5k MRR
        'bronze': 0         # <$2k MRR
    }
    
    def __init__(self, db):
        self.db = db
    
    def calculate_segmentation(self, customer_id, agreements, meetings, reports):
        """
        Calculate comprehensive client segmentation
        
        Args:
            customer_id: Customer ID
            agreements: List of client agreements
            meetings: List of client meetings
            reports: List of client reports
        
        Returns:
            dict with segmentation data
        """
        # Calculate MRR metrics
        mrr_data = self._calculate_mrr_metrics(agreements)
        
        # Calculate tier based on MRR
        tier = self._calculate_tier(mrr_data['total_mrr'])
        
        # Calculate health score
        health_data = self._calculate_health_score(agreements, meetings, reports)
        
        # Calculate engagement metrics
        engagement_data = self._calculate_engagement(meetings, reports)
        
        # Calculate risk level
        risk_data = self._calculate_risk(mrr_data, health_data, engagement_data)
        
        # Determine growth potential
        growth_potential = self._calculate_growth_potential(mrr_data, agreements)
        
        # Calculate tenure
        tenure_data = self._calculate_tenure(agreements)
        
        return {
            'customer_id': customer_id,
            'tier': tier,
            'tier_score': self._calculate_tier_score(mrr_data['total_mrr']),
            'total_mrr': mrr_data['total_mrr'],
            'mrr_trend': mrr_data['trend'],
            'mrr_change_percentage': mrr_data['change_percentage'],
            'lifetime_value': mrr_data['total_mrr'] * tenure_data['tenure_months'],
            'customer_since': tenure_data['customer_since'],
            'tenure_months': tenure_data['tenure_months'],
            'health_score': health_data['score'],
            'health_status': health_data['status'],
            'last_meeting_date': engagement_data['last_meeting_date'],
            'meetings_per_quarter': engagement_data['meetings_per_quarter'],
            'last_report_date': engagement_data['last_report_date'],
            'risk_level': risk_data['level'],
            'risk_factors': risk_data['factors'],
            'strategic_account': self._is_strategic_account(mrr_data['total_mrr'], health_data['score']),
            'growth_potential': growth_potential,
            'tags': self._generate_tags(tier, health_data['status'], risk_data['level']),
            'last_calculated': datetime.utcnow(),
            'calculation_version': '1.0'
        }
    
    def _calculate_mrr_metrics(self, agreements):
        """Calculate MRR and trends"""
        if not agreements:
            return {
                'total_mrr': 0.0,
                'trend': 'stable',
                'change_percentage': 0.0
            }
        
        # Sum active agreements
        active_agreements = [a for a in agreements if a.get('status') == 'active']
        total_mrr = sum(a.get('monthly_mrr', 0) for a in active_agreements)
        
        # Simple trend calculation (would use historical data in production)
        # For now, assume stable
        trend = 'stable'
        change_percentage = 0.0
        
        # If we had historical MRR data, we'd calculate trend here
        # trend = 'growing' if current_mrr > previous_mrr else 'declining'
        
        return {
            'total_mrr': total_mrr,
            'trend': trend,
            'change_percentage': change_percentage
        }
    
    def _calculate_tier(self, total_mrr):
        """Calculate tier based on MRR thresholds"""
        if total_mrr >= self.TIER_THRESHOLDS['platinum']:
            return 'platinum'
        elif total_mrr >= self.TIER_THRESHOLDS['gold']:
            return 'gold'
        elif total_mrr >= self.TIER_THRESHOLDS['silver']:
            return 'silver'
        else:
            return 'bronze'
    
    def _calculate_tier_score(self, total_mrr):
        """Calculate numeric tier score (0-100)"""
        # Normalize MRR to 0-100 scale
        max_mrr = 20000  # $20k is 100 score
        score = min(100, (total_mrr / max_mrr) * 100)
        return round(score, 1)
    
    def _calculate_health_score(self, agreements, meetings, reports):
        """Calculate client health score (0-100)"""
        score = 100
        factors = []
        
        # Agreement health (30 points)
        if not agreements or not any(a.get('status') == 'active' for a in agreements):
            score -= 30
            factors.append("No active agreements")
        
        # Meeting engagement (25 points)
        if not meetings or len(meetings) == 0:
            score -= 25
            factors.append("No recent meetings")
        elif len(meetings) < 2:
            score -= 15
            factors.append("Low meeting frequency")
        
        # Report generation (25 points)
        if not reports or len(reports) == 0:
            score -= 25
            factors.append("No reports generated")
        elif len(reports) < 2:
            score -= 10
            factors.append("Infrequent reporting")
        
        # Security posture (20 points)
        if reports:
            latest_report = reports[0]
            security_score = latest_report.get('overall_score', 0)
            if security_score < 50:
                score -= 20
                factors.append("Poor security posture")
            elif security_score < 70:
                score -= 10
                factors.append("Below-average security")
        
        # Determine status
        if score >= 80:
            status = 'excellent'
        elif score >= 60:
            status = 'good'
        elif score >= 40:
            status = 'at_risk'
        else:
            status = 'critical'
        
        return {
            'score': max(0, score),
            'status': status,
            'factors': factors
        }
    
    def _calculate_engagement(self, meetings, reports):
        """Calculate engagement metrics"""
        # Last meeting
        last_meeting_date = None
        if meetings:
            sorted_meetings = sorted(meetings, key=lambda m: m.get('scheduled_date', ''), reverse=True)
            if sorted_meetings:
                last_meeting_date = sorted_meetings[0].get('scheduled_date')
        
        # Meetings per quarter
        three_months_ago = datetime.utcnow() - timedelta(days=90)
        recent_meetings = [
            m for m in meetings 
            if m.get('scheduled_date') and 
            datetime.fromisoformat(m['scheduled_date'].replace('Z', '+00:00')) >= three_months_ago
        ] if meetings else []
        meetings_per_quarter = len(recent_meetings)
        
        # Last report
        last_report_date = None
        if reports:
            sorted_reports = sorted(reports, key=lambda r: r.get('generated_at', ''), reverse=True)
            if sorted_reports:
                last_report_date = sorted_reports[0].get('generated_at')
        
        return {
            'last_meeting_date': last_meeting_date,
            'meetings_per_quarter': meetings_per_quarter,
            'last_report_date': last_report_date
        }
    
    def _calculate_risk(self, mrr_data, health_data, engagement_data):
        """Calculate risk level and factors"""
        risk_score = 0
        factors = []
        
        # MRR risk
        if mrr_data['trend'] == 'declining':
            risk_score += 30
            factors.append("Declining MRR")
        
        if mrr_data['total_mrr'] < 1000:
            risk_score += 20
            factors.append("Low MRR value")
        
        # Health risk
        if health_data['score'] < 50:
            risk_score += 30
            factors.append("Critical health score")
        elif health_data['score'] < 70:
            risk_score += 15
            factors.append("Below-average health")
        
        # Engagement risk
        if engagement_data['meetings_per_quarter'] == 0:
            risk_score += 20
            factors.append("No recent meetings")
        
        # Determine level
        if risk_score >= 60:
            level = 'critical'
        elif risk_score >= 40:
            level = 'high'
        elif risk_score >= 20:
            level = 'medium'
        else:
            level = 'low'
        
        return {
            'level': level,
            'score': risk_score,
            'factors': factors
        }
    
    def _calculate_growth_potential(self, mrr_data, agreements):
        """Calculate growth potential"""
        # Simple heuristic - in production, use more sophisticated analysis
        if mrr_data['trend'] == 'growing':
            return 'high'
        elif mrr_data['total_mrr'] < 5000 and len(agreements) > 0:
            return 'medium'  # Room to grow
        else:
            return 'low'
    
    def _calculate_tenure(self, agreements):
        """Calculate customer tenure"""
        if not agreements:
            return {
                'customer_since': None,
                'tenure_months': 0
            }
        
        # Find earliest agreement start date
        sorted_agreements = sorted(
            [a for a in agreements if a.get('start_date')],
            key=lambda a: a['start_date']
        )
        
        if not sorted_agreements:
            return {
                'customer_since': None,
                'tenure_months': 0
            }
        
        customer_since = sorted_agreements[0]['start_date']
        
        # Calculate months
        if isinstance(customer_since, str):
            customer_since = datetime.fromisoformat(customer_since).date()
        
        today = datetime.utcnow().date()
        tenure_months = (today.year - customer_since.year) * 12 + (today.month - customer_since.month)
        
        return {
            'customer_since': customer_since,
            'tenure_months': max(0, tenure_months)
        }
    
    def _is_strategic_account(self, total_mrr, health_score):
        """Determine if account is strategic"""
        # Strategic if high MRR and good health
        return total_mrr >= 5000 and health_score >= 70
    
    def _generate_tags(self, tier, health_status, risk_level):
        """Generate automatic tags"""
        tags = [tier.upper()]
        
        if health_status == 'excellent':
            tags.append('HEALTHY')
        elif health_status in ['at_risk', 'critical']:
            tags.append('NEEDS_ATTENTION')
        
        if risk_level in ['high', 'critical']:
            tags.append('HIGH_RISK')
        
        return tags
    
    def get_tier_summary(self):
        """Get summary of clients by tier"""
        # This would query the database in production
        return {
            'platinum': {'count': 0, 'total_mrr': 0},
            'gold': {'count': 0, 'total_mrr': 0},
            'silver': {'count': 0, 'total_mrr': 0},
            'bronze': {'count': 0, 'total_mrr': 0}
        }

