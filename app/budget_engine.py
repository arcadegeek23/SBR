from typing import Dict, List

class BudgetEngine:
    """Calculates budget estimates for recommendations"""
    
    def __init__(self, unit_costs: Dict):
        self.unit_costs = unit_costs
    
    def calculate_budget(self, signals: Dict, gaps: List[Dict]) -> Dict:
        """
        Calculate monthly budget for addressing gaps
        
        Returns:
            Dict with service-level costs and total
        """
        budget = {
            'services': [],
            'total_monthly': 0.0,
            'total_annual': 0.0
        }
        
        # Extract counts from signals
        user_count = signals.get('total_users', 0)
        endpoint_count = signals.get('total_endpoints', 0)
        server_count = signals.get('total_servers', 0)
        
        # Check which services are needed based on gaps
        needs_mfa = any(g['signal'] == 'mfa' for g in gaps)
        needs_edr = any(g['signal'] == 'edr' for g in gaps)
        needs_backup = any(g['signal'] == 'backup_status' for g in gaps)
        
        # Calculate MFA cost
        if needs_mfa and user_count > 0:
            mfa_monthly = user_count * self.unit_costs['COST_MFA_PER_USER']
            budget['services'].append({
                'service': 'Multi-Factor Authentication',
                'unit': 'per user',
                'quantity': user_count,
                'unit_cost': self.unit_costs['COST_MFA_PER_USER'],
                'monthly_cost': round(mfa_monthly, 2),
                'annual_cost': round(mfa_monthly * 12, 2)
            })
            budget['total_monthly'] += mfa_monthly
        
        # Calculate EDR cost
        if needs_edr and endpoint_count > 0:
            # Calculate uncovered endpoints
            edr_coverage = signals.get('edr', 0) / 100
            uncovered_endpoints = int(endpoint_count * (1 - edr_coverage))
            
            if uncovered_endpoints > 0:
                edr_monthly = uncovered_endpoints * self.unit_costs['COST_EDR_PER_ENDPOINT']
                budget['services'].append({
                    'service': 'Endpoint Detection & Response',
                    'unit': 'per endpoint',
                    'quantity': uncovered_endpoints,
                    'unit_cost': self.unit_costs['COST_EDR_PER_ENDPOINT'],
                    'monthly_cost': round(edr_monthly, 2),
                    'annual_cost': round(edr_monthly * 12, 2)
                })
                budget['total_monthly'] += edr_monthly
        
        # Calculate Backup cost
        if needs_backup and server_count > 0:
            # Calculate servers without backup
            backup_coverage = signals.get('backup_status', 0) / 100
            uncovered_servers = int(server_count * (1 - backup_coverage))
            
            if uncovered_servers > 0:
                backup_monthly = uncovered_servers * self.unit_costs['COST_BACKUP_PER_SERVER']
                budget['services'].append({
                    'service': 'Server Backup Solution',
                    'unit': 'per server',
                    'quantity': uncovered_servers,
                    'unit_cost': self.unit_costs['COST_BACKUP_PER_SERVER'],
                    'monthly_cost': round(backup_monthly, 2),
                    'annual_cost': round(backup_monthly * 12, 2)
                })
                budget['total_monthly'] += backup_monthly
        
        # Optional: SIEM for comprehensive monitoring (if multiple high-severity gaps)
        high_severity_gaps = sum(1 for g in gaps if g['severity'] in ['High', 'Critical'])
        if high_severity_gaps >= 3 and user_count > 0:
            siem_monthly = user_count * self.unit_costs['COST_SIEM_PER_USER']
            budget['services'].append({
                'service': 'SIEM / Security Monitoring',
                'unit': 'per user',
                'quantity': user_count,
                'unit_cost': self.unit_costs['COST_SIEM_PER_USER'],
                'monthly_cost': round(siem_monthly, 2),
                'annual_cost': round(siem_monthly * 12, 2),
                'note': 'Recommended due to multiple security gaps'
            })
            budget['total_monthly'] += siem_monthly
        
        # Round totals
        budget['total_monthly'] = round(budget['total_monthly'], 2)
        budget['total_annual'] = round(budget['total_monthly'] * 12, 2)
        
        return budget

