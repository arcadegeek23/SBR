# Strategic Business Review
## {{ customer_name }}

**Report Generated:** {{ generated_at }}  
**Review Period:** {{ review_period }}

---

## Executive Summary

This Strategic Business Review provides a comprehensive assessment of {{ customer_name }}'s current IT security and operational posture, aligned to the **NIST Cybersecurity Framework (CSF)**. The analysis is based on operational data extracted from HaloPSA, including asset inventory, ticket history, and security configurations.

### Overall Security Posture Score: {{ "%.1f" | format(overall_score * 100) }}%

{% if overall_score >= 0.9 %}
**Status:** Excellent - Strong security posture with minimal gaps
{% elif overall_score >= 0.75 %}
**Status:** Good - Solid foundation with some areas for improvement
{% elif overall_score >= 0.60 %}
**Status:** Fair - Moderate gaps requiring attention
{% else %}
**Status:** Needs Improvement - Significant security gaps identified
{% endif %}

---

## NIST Cybersecurity Framework Scores

| Category | Score | Status |
|----------|-------|--------|
| **Identify** | {{ "%.1f" | format(nist_scores.Identify * 100) }}% | {% if nist_scores.Identify >= 0.9 %}✓ Strong{% elif nist_scores.Identify >= 0.75 %}→ Good{% else %}⚠ Needs Work{% endif %} |
| **Protect** | {{ "%.1f" | format(nist_scores.Protect * 100) }}% | {% if nist_scores.Protect >= 0.9 %}✓ Strong{% elif nist_scores.Protect >= 0.75 %}→ Good{% else %}⚠ Needs Work{% endif %} |
| **Detect** | {{ "%.1f" | format(nist_scores.Detect * 100) }}% | {% if nist_scores.Detect >= 0.9 %}✓ Strong{% elif nist_scores.Detect >= 0.75 %}→ Good{% else %}⚠ Needs Work{% endif %} |
| **Respond** | {{ "%.1f" | format(nist_scores.Respond * 100) }}% | {% if nist_scores.Respond >= 0.9 %}✓ Strong{% elif nist_scores.Respond >= 0.75 %}→ Good{% else %}⚠ Needs Work{% endif %} |
| **Recover** | {{ "%.1f" | format(nist_scores.Recover * 100) }}% | {% if nist_scores.Recover >= 0.9 %}✓ Strong{% elif nist_scores.Recover >= 0.75 %}→ Good{% else %}⚠ Needs Work{% endif %} |

### Category Definitions

- **Identify:** Asset visibility and inventory management
- **Protect:** Preventive security controls (patching, MFA, EDR)
- **Detect:** Threat detection and monitoring capabilities
- **Respond:** Incident response and SLA performance
- **Recover:** Business continuity and backup capabilities

---

## Key Operational Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Patch Compliance** | {{ "%.1f" | format(signals.patch_compliance) }}% | ≥ 95% | {% if signals.patch_compliance >= 95 %}✓{% else %}⚠{% endif %} |
| **Backup Coverage** | {{ "%.1f" | format(signals.backup_status) }}% | ≥ 98% | {% if signals.backup_status >= 98 %}✓{% else %}⚠{% endif %} |
| **EDR Coverage** | {{ "%.1f" | format(signals.edr) }}% | ≥ 90% | {% if signals.edr >= 90 %}✓{% else %}⚠{% endif %} |
| **SLA Attainment** | {{ "%.1f" | format(signals.response_time_sla) }}% | ≥ 90% | {% if signals.response_time_sla >= 90 %}✓{% else %}⚠{% endif %} |
| **MFA Enforcement** | {% if signals.mfa >= 100 %}Enabled{% else %}Not Enabled{% endif %} | Enabled | {% if signals.mfa >= 100 %}✓{% else %}⚠{% endif %} |
| **Avg. Monthly Incidents** | {{ "%.0f" | format(signals.incident_volume) }} | - | - |

### Environment Summary
- **Total Assets:** {{ signals.total_assets }}
- **Servers:** {{ signals.total_servers }}
- **Endpoints:** {{ signals.total_endpoints }}
- **Active Users:** {{ signals.total_users }}

---

## Identified Gaps and Risks

{% if gaps %}
{% for gap in gaps %}
### {{ loop.index }}. {{ gap.issue }}

**Category:** {{ gap.category }}  
**Severity:** {{ gap.severity }}  
**Current Value:** {{ "%.1f" | format(gap.current_value) }}%  
**Best Practice Threshold:** {{ gap.threshold }}%

**Impact:** {{ gap.impact }}

---
{% endfor %}
{% else %}
No significant gaps identified. Current posture meets or exceeds best practice thresholds.
{% endif %}

---

## Recommendations

{% if recommendations %}
{% for rec in recommendations %}
### {{ loop.index }}. {{ rec.recommendation }}

**Priority:** {{ rec.priority }}  
**NIST Category:** {{ rec.category }}

**Action Items:**
{% for action in rec.action_items %}
- {{ action }}
{% endfor %}

---
{% endfor %}
{% else %}
No immediate recommendations. Continue monitoring and maintaining current security posture.
{% endif %}

---

## Budget Projection

{% if budget.services %}
The following monthly budget estimates address the identified gaps:

| Service | Quantity | Unit Cost | Monthly Cost | Annual Cost |
|---------|----------|-----------|--------------|-------------|
{% for service in budget.services %}
| {{ service.service }} | {{ service.quantity }} {{ service.unit }} | ${{ "%.2f" | format(service.unit_cost) }} | ${{ "%.2f" | format(service.monthly_cost) }} | ${{ "%.2f" | format(service.annual_cost) }} |
{% endfor %}
| **TOTAL** | | | **${{ "%.2f" | format(budget.total_monthly) }}** | **${{ "%.2f" | format(budget.total_annual) }}** |

### Investment Justification

Implementing these recommendations will:
- Reduce security risk exposure by addressing critical gaps
- Improve operational efficiency and incident response times
- Ensure compliance with industry best practices and frameworks
- Provide measurable ROI through reduced breach risk and downtime

{% else %}
No additional budget required at this time. Current investments are adequate for the identified posture.
{% endif %}

---

## Notes and Assumptions

- Data extracted from HaloPSA for the period: {{ review_period }}
- Scoring methodology based on NIST Cybersecurity Framework v1.1
- Budget estimates use industry-standard unit costs and may vary by vendor
- Recommendations prioritized by risk severity and business impact
- This review should be regenerated quarterly to track progress and trends

---

## Next Steps

1. **Review and Validate:** Confirm accuracy of data and identified gaps with technical team
2. **Prioritize Actions:** Align recommendations with business objectives and budget cycles
3. **Create Implementation Plan:** Develop timeline and resource allocation for priority items
4. **Schedule Follow-up:** Plan quarterly review to measure progress and adjust strategy
5. **Customer Communication:** Present findings and recommendations in executive briefing

---

**Report prepared by Computer Integration Technologies**  
*Automated Strategic Business Review Generator*

