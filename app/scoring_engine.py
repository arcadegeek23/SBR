from typing import Dict, List, Tuple

class ScoringEngine:
    """Calculates NIST CSF scores and identifies gaps"""
    
    # NIST CSF Category Mappings
    NIST_MAPPINGS = {
        'Identify': ['total_assets', 'total_users'],
        'Protect': ['patch_compliance', 'mfa', 'edr', 'backup_status'],
        'Detect': ['edr', 'incident_volume'],
        'Respond': ['response_time_sla', 'incident_volume'],
        'Recover': ['backup_status']
    }
    
    def __init__(self, thresholds: Dict):
        self.thresholds = thresholds
    
    def calculate_nist_scores(self, signals: Dict) -> Dict:
        """
        Calculate NIST CSF category scores
        
        Returns:
            Dict with scores for each NIST category (0-1 scale)
        """
        scores = {}
        
        # Identify - baseline visibility (always 1.0 if we have data)
        scores['Identify'] = 1.0 if signals.get('total_assets', 0) > 0 else 0.0
        
        # Protect - average of security controls
        protect_signals = [
            signals.get('patch_compliance', 0) / 100,
            signals.get('mfa', 0) / 100,
            signals.get('edr', 0) / 100,
            signals.get('backup_status', 0) / 100
        ]
        scores['Protect'] = round(sum(protect_signals) / len(protect_signals), 3)
        
        # Detect - EDR coverage (primary detection mechanism)
        scores['Detect'] = round(signals.get('edr', 0) / 100, 3)
        
        # Respond - SLA performance
        scores['Respond'] = round(signals.get('response_time_sla', 0) / 100, 3)
        
        # Recover - backup status
        scores['Recover'] = round(signals.get('backup_status', 0) / 100, 3)
        
        # Overall score (weighted average)
        overall = (
            scores['Identify'] * 0.15 +
            scores['Protect'] * 0.30 +
            scores['Detect'] * 0.20 +
            scores['Respond'] * 0.20 +
            scores['Recover'] * 0.15
        )
        scores['Overall'] = round(overall, 3)
        
        return scores
    
    def identify_gaps(self, signals: Dict, scores: Dict) -> List[Dict]:
        """
        Identify gaps based on thresholds
        
        Returns:
            List of gap dictionaries with category, issue, severity, and impact
        """
        gaps = []
        
        # Patch Compliance
        if signals.get('patch_compliance', 0) < self.thresholds['THRESHOLD_PATCH_COMPLIANCE']:
            gaps.append({
                'category': 'Protect',
                'signal': 'patch_compliance',
                'current_value': signals.get('patch_compliance', 0),
                'threshold': self.thresholds['THRESHOLD_PATCH_COMPLIANCE'],
                'severity': 'High',
                'issue': 'Patch compliance below best practice threshold',
                'impact': 'Increased vulnerability to known exploits and security breaches'
            })
        
        # Backup Status
        if signals.get('backup_status', 0) < self.thresholds['THRESHOLD_BACKUP_SUCCESS']:
            gaps.append({
                'category': 'Recover',
                'signal': 'backup_status',
                'current_value': signals.get('backup_status', 0),
                'threshold': self.thresholds['THRESHOLD_BACKUP_SUCCESS'],
                'severity': 'Critical',
                'issue': 'Backup coverage below best practice threshold',
                'impact': 'Risk of data loss and extended downtime in disaster scenarios'
            })
        
        # EDR Coverage
        if signals.get('edr', 0) < self.thresholds['THRESHOLD_EDR_COVERAGE']:
            gaps.append({
                'category': 'Protect/Detect',
                'signal': 'edr',
                'current_value': signals.get('edr', 0),
                'threshold': self.thresholds['THRESHOLD_EDR_COVERAGE'],
                'severity': 'High',
                'issue': 'EDR/Antivirus coverage below best practice threshold',
                'impact': 'Limited threat detection and response capabilities'
            })
        
        # SLA Performance
        if signals.get('response_time_sla', 0) < self.thresholds['THRESHOLD_SLA_ATTAINMENT']:
            gaps.append({
                'category': 'Respond',
                'signal': 'response_time_sla',
                'current_value': signals.get('response_time_sla', 0),
                'threshold': self.thresholds['THRESHOLD_SLA_ATTAINMENT'],
                'severity': 'Medium',
                'issue': 'SLA attainment below target',
                'impact': 'Delayed incident response affecting business operations'
            })
        
        # MFA
        if signals.get('mfa', 0) < 100:
            gaps.append({
                'category': 'Protect',
                'signal': 'mfa',
                'current_value': signals.get('mfa', 0),
                'threshold': 100,
                'severity': 'Critical',
                'issue': 'Multi-Factor Authentication not enforced',
                'impact': 'High risk of account compromise and unauthorized access'
            })
        
        return gaps
    
    def generate_recommendations(self, gaps: List[Dict], signals: Dict) -> List[Dict]:
        """
        Generate actionable recommendations based on gaps
        
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        for gap in gaps:
            rec = {
                'category': gap['category'],
                'priority': gap['severity'],
                'issue': gap['issue']
            }
            
            # Generate specific recommendation based on signal
            if gap['signal'] == 'patch_compliance':
                rec['recommendation'] = 'Implement automated patch management solution and establish monthly patching cadence'
                rec['action_items'] = [
                    'Deploy patch management tool across all endpoints',
                    'Create maintenance windows for critical systems',
                    'Establish patch testing and rollback procedures'
                ]
            
            elif gap['signal'] == 'backup_status':
                rec['recommendation'] = 'Deploy enterprise backup solution for all servers with daily backup schedules'
                rec['action_items'] = [
                    'Implement backup solution for uncovered servers',
                    'Configure daily incremental and weekly full backups',
                    'Establish quarterly restore testing procedures'
                ]
            
            elif gap['signal'] == 'edr':
                rec['recommendation'] = 'Deploy EDR solution to all endpoints for comprehensive threat detection'
                rec['action_items'] = [
                    'License and deploy EDR agent to all workstations and servers',
                    'Configure threat detection policies and alerting',
                    'Establish SOC monitoring and response procedures'
                ]
            
            elif gap['signal'] == 'response_time_sla':
                rec['recommendation'] = 'Optimize incident response processes and resource allocation'
                rec['action_items'] = [
                    'Review and adjust ticket prioritization rules',
                    'Implement automated triage and routing',
                    'Increase staffing during peak incident periods'
                ]
            
            elif gap['signal'] == 'mfa':
                rec['recommendation'] = 'Enable and enforce MFA for all user accounts, especially privileged access'
                rec['action_items'] = [
                    'Deploy MFA solution (Azure AD, Duo, etc.)',
                    'Enforce MFA for all administrative accounts immediately',
                    'Roll out MFA to all users with 30-day adoption plan'
                ]
            
            recommendations.append(rec)
        
        return recommendations

