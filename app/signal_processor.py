from typing import Dict, List

class SignalProcessor:
    """Processes raw Halo data into normalized signals"""
    
    @staticmethod
    def derive_signals(customer: Dict, assets: List[Dict], tickets: List[Dict], users: List[Dict]) -> Dict:
        """
        Derive key signals from Halo data
        
        Returns:
            Dict with signals: patch_compliance, backup_status, mfa, edr, response_time_sla, incident_volume
        """
        signals = {}
        
        # Patch Compliance
        if assets:
            compliant_assets = sum(1 for a in assets if a.get('patchstatus') in ['Compliant', 'UpToDate'])
            signals['patch_compliance'] = round(compliant_assets / len(assets) * 100, 2)
        else:
            signals['patch_compliance'] = 0.0
        
        # Backup Status
        if assets:
            servers = [a for a in assets if a.get('type') == 'Server']
            if servers:
                backed_up = sum(1 for s in servers if s.get('backup_enabled') is True)
                signals['backup_status'] = round(backed_up / len(servers) * 100, 2)
            else:
                signals['backup_status'] = 100.0  # No servers to back up
        else:
            signals['backup_status'] = 0.0
        
        # MFA
        mfa_enforced = customer.get('mfa_enforced', False)
        signals['mfa'] = 100.0 if mfa_enforced else 0.0
        
        # EDR (Endpoint Detection and Response)
        if assets:
            endpoints = [a for a in assets if a.get('type') in ['Workstation', 'Laptop', 'Server']]
            if endpoints:
                protected = sum(1 for e in endpoints if e.get('antivirusstatus') in ['Protected', 'Enabled'])
                signals['edr'] = round(protected / len(endpoints) * 100, 2)
            else:
                signals['edr'] = 0.0
        else:
            signals['edr'] = 0.0
        
        # Response Time SLA
        if tickets:
            met_sla = sum(1 for t in tickets if t.get('met_sla') is True)
            signals['response_time_sla'] = round(met_sla / len(tickets) * 100, 2)
        else:
            signals['response_time_sla'] = 100.0  # No tickets = perfect SLA
        
        # Incident Volume (average per month)
        if tickets:
            # Assuming tickets span 90 days (3 months) by default
            signals['incident_volume'] = round(len(tickets) / 3, 2)
        else:
            signals['incident_volume'] = 0.0
        
        # Additional context
        signals['total_assets'] = len(assets)
        signals['total_users'] = len([u for u in users if u.get('active', True)])
        signals['total_servers'] = len([a for a in assets if a.get('type') == 'Server'])
        signals['total_endpoints'] = len([a for a in assets if a.get('type') in ['Workstation', 'Laptop']])
        
        return signals
    
    @staticmethod
    def normalize_signal(value: float, max_value: float = 100.0) -> float:
        """Normalize a signal to 0-1 scale"""
        return min(value / max_value, 1.0)

