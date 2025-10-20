# CIT SBR Framework Implementation Roadmap

## Overview

This document outlines the implementation of the comprehensive CIT SBR Framework based on the Notion requirements. The framework transforms the SBR application into a market-specific, stakeholder-aware business intelligence platform.

---

## ✅ Phase 1: Foundation (COMPLETED)

### 1.1 Industry Segmentation
**Status:** ✅ Implemented

**What was built:**
- Added `industry` field to Customer and ReportRun models
- Support for 5 industry types:
  - Government (Local Government & Schools)
  - Nonprofit (Health & Public Service)
  - Manufacturing
  - Financial Services
  - Healthcare Organizations
- Industry-specific parameters in ROI Engine
- Mock data generator assigns random industries

**Files Modified:**
- `app/models.py` - Added industry fields
- `app/halo_connector.py` - Industry in mock data

### 1.2 ROI Calculation Engine
**Status:** ✅ Implemented

**What was built:**
- `app/roi_engine.py` - Complete ROI calculation module
- 4 ROI presentation formats:
  1. **Risk Avoidance Model** - For Finance/Manufacturing/Healthcare leadership
  2. **Efficiency Unlock** - For Operations/Nonprofits
  3. **Compliance/Risk Score** - For Government/Financial/Healthcare
  4. **Three-Year Stacked ROI** - For budget-conscious organizations

**Key Features:**
- Industry-specific downtime costs
- Compliance framework mapping
- Peer benchmarking calculations
- Tiered budget recommendations

### 1.3 Stakeholder Content Generator
**Status:** ✅ Implemented

**What was built:**
- `app/stakeholder_content.py` - Stakeholder-specific content module
- Content types:
  1. **Executive One-Pager** - 30-second read format
  2. **Board/C-Suite Talking Points** - Pre-written presentation points
  3. **Budget Justification Template** - Internal approval document
  4. **Monthly Accountability Scorecard** - Progress tracking
  5. **Three-Tier Content** - For different audiences

**Key Features:**
- Role-specific language (ops vs. leadership)
- Business impact focus (not technical jargon)
- Specific dollar amounts and ROI calculations
- Before/after comparisons

---

## 🚧 Phase 2: Integration (IN PROGRESS)

### 2.1 Main Application Integration
**Status:** 🚧 Partial

**What needs to be done:**
1. ✅ Import new modules into `main.py`
2. ⏳ Initialize ROI Engine with industry type
3. ⏳ Calculate all 4 ROI formats in generate_review
4. ⏳ Generate stakeholder content
5. ⏳ Store ROI and stakeholder data in database
6. ⏳ Pass to report builder

**Implementation Steps:**
```python
# In generate_review route:

# After Step 1 (Fetch data):
industry = customer.get('industry', 'government')
roi_engine = ROIEngine(industry=industry)
stakeholder_gen = StakeholderContentGenerator()

# After Step 6 (Calculate budget):
# Calculate ROI (all 4 formats)
roi_risk_avoidance = roi_engine.calculate_risk_avoidance_roi(
    investment=budget.get('total_monthly', 0) * 12,
    incidents_prevented=len([t for t in tickets if t.get('priority') == 'Critical']),
    avg_incident_duration_hours=6.0
)

roi_efficiency = roi_engine.calculate_efficiency_unlock_roi(
    hours_freed_annually=ai_insights['ticket_analysis'].get('automation_potential', 0),
    cost_per_hour=50.0
)

roi_compliance = roi_engine.calculate_compliance_roi(
    current_compliance_pct=nist_scores.get('Overall', 0) * 100,
    target_compliance_pct=100,
    penalty_at_current=250000,  # Industry-specific
    cost_to_reach_target=budget.get('total_monthly', 0) * 12
)

roi_three_year = roi_engine.calculate_three_year_stacked_roi(
    year1_investment=budget.get('total_monthly', 0) * 12,
    year1_savings=roi_risk_avoidance['total_risk_prevented'] * 0.3
)

# Generate industry-specific metrics
industry_metrics = roi_engine.generate_industry_metrics(signals, tickets)
peer_benchmark = roi_engine.generate_peer_benchmark(signals)

# Calculate tiered budget
tiered_budget = roi_engine.calculate_tiered_budget(
    total_budget=budget.get('total_monthly', 0) * 12,
    gaps=gaps,
    current_monthly_cost=budget.get('total_monthly', 0)
)

# Generate stakeholder content
executive_onepager = stakeholder_gen.generate_executive_onepager(
    customer_name=customer.get('name'),
    overall_score=nist_scores.get('Overall', 0) * 100,
    roi_data=roi_risk_avoidance,
    top_risks=gaps[:3],
    top_recommendations=recommendations[:3]
)

board_talking_points = stakeholder_gen.generate_board_talking_points(
    customer_name=customer.get('name'),
    industry=industry,
    key_metrics=industry_metrics,
    peer_benchmark=peer_benchmark,
    incidents_prevented=len([t for t in tickets if t.get('priority') == 'Critical'])
)

budget_justification = stakeholder_gen.generate_budget_justification(
    tiered_budget=tiered_budget,
    current_state={'compliance_pct': nist_scores.get('Overall', 0) * 100, 'gap_count': len(gaps)},
    target_state={'compliance_pct': 100, 'gaps_closed': len(gaps)}
)

monthly_scorecard = stakeholder_gen.generate_monthly_scorecard(
    customer_name=customer.get('name'),
    month=datetime.now().strftime('%B %Y'),
    metrics={'uptime_pct': 99.97, 'incidents_blocked': 12},
    targets={'uptime_pct': 99.9, 'incidents_blocked': 8},
    ytd_roi={'total_value': roi_risk_avoidance['total_risk_prevented']}
)

three_tier_content = stakeholder_gen.generate_three_tier_content(
    customer_name=customer.get('name'),
    overall_score=nist_scores.get('Overall', 0) * 100,
    roi_data=roi_risk_avoidance,
    peer_benchmark=peer_benchmark,
    progress_metrics={'incidents_blocked': 12}
)

# Combine all ROI and stakeholder data
roi_data = {
    'risk_avoidance': roi_risk_avoidance,
    'efficiency': roi_efficiency,
    'compliance': roi_compliance,
    'three_year': roi_three_year,
    'industry_metrics': industry_metrics,
    'peer_benchmark': peer_benchmark,
    'tiered_budget': tiered_budget
}

stakeholder_data = {
    'executive_onepager': executive_onepager,
    'board_talking_points': board_talking_points,
    'budget_justification': budget_justification,
    'monthly_scorecard': monthly_scorecard,
    'three_tier_content': three_tier_content
}

# Pass to report builder
report_paths = report_builder.generate_report(
    customer_id=customer_id,
    customer_name=customer.get('name', 'Unknown'),
    signals=signals,
    nist_scores=nist_scores,
    gaps=gaps,
    recommendations=recommendations,
    budget=budget,
    ai_insights=ai_insights,
    roi_data=roi_data,  # NEW
    stakeholder_data=stakeholder_data  # NEW
)
```

### 2.2 Database Schema Updates
**Status:** ⏳ Pending

**What needs to be done:**
1. Add `roi_data` JSON field to ReportRun model
2. Add `stakeholder_data` JSON field to ReportRun model
3. Create database migration script
4. Update to_dict() methods

**Migration Script:**
```python
# migrations/add_roi_stakeholder_fields.py
from app.models import db

def upgrade():
    with db.engine.connect() as conn:
        conn.execute("""
            ALTER TABLE report_runs 
            ADD COLUMN roi_data JSON,
            ADD COLUMN stakeholder_data JSON
        """)

def downgrade():
    with db.engine.connect() as conn:
        conn.execute("""
            ALTER TABLE report_runs 
            DROP COLUMN roi_data,
            DROP COLUMN stakeholder_data
        """)
```

### 2.3 Report Template Updates
**Status:** ⏳ Pending

**What needs to be done:**
1. Add ROI sections to HTML template
2. Add stakeholder content sections
3. Add industry-specific metrics display
4. Add tiered budget visualization
5. Add peer benchmarking charts

**New Template Sections:**
- Industry Overview
- ROI Analysis (4 formats)
- Peer Benchmarking
- Tiered Budget Recommendations
- Executive One-Pager (exportable)
- Monthly Scorecard (exportable)

---

## 📋 Phase 3: UI Enhancements (PLANNED)

### 3.1 Industry Selection
**What needs to be built:**
- Industry dropdown in UI
- Industry-specific branding/colors
- Industry-specific language

### 3.2 Stakeholder View Selector
**What needs to be built:**
- View switcher: Operations | Leadership | Executive
- Role-based content filtering
- Exportable one-pagers

### 3.3 ROI Calculator Widget
**What needs to be built:**
- Interactive ROI calculator
- Budget scenario comparison
- What-if analysis tool

---

## 🎯 Phase 4: Advanced Features (FUTURE)

### 4.1 API Endpoints for Stakeholder Content
```python
@app.route('/api/reports/<int:report_id>/executive-onepager')
def get_executive_onepager(report_id):
    """Get executive one-pager for a report"""
    pass

@app.route('/api/reports/<int:report_id>/board-talking-points')
def get_board_talking_points(report_id):
    """Get board talking points"""
    pass

@app.route('/api/reports/<int:report_id>/monthly-scorecard')
def get_monthly_scorecard(report_id):
    """Get monthly accountability scorecard"""
    pass
```

### 4.2 Export Formats
- Executive One-Pager PDF
- Board Presentation PowerPoint
- Monthly Scorecard Email Template

### 4.3 Benchmarking Database
- Real industry benchmark data
- Peer comparison analytics
- Trend analysis over time

### 4.4 AI Agent Integration
Implement the 5 AI agents from Notion requirements:
1. **SBR Data Aggregator** - Automated data collection
2. **ROI Calculator & Formatter** - Pre-filled ROI models
3. **Benchmark Comparator** - Real-time peer data
4. **Meeting Prep Advisor** - Personalized slide decks
5. **Budget Optimizer** - Tiered recommendations

---

## 📊 Current Implementation Status

### Completed ✅
- [x] ROI Engine with 4 calculation formats
- [x] Stakeholder Content Generator
- [x] Industry segmentation (5 types)
- [x] Tiered budget calculator
- [x] Peer benchmarking framework
- [x] Industry-specific parameters
- [x] Database schema for industry

### In Progress 🚧
- [ ] Main application integration
- [ ] Report template updates
- [ ] Database migration for ROI/stakeholder fields

### Planned 📋
- [ ] UI enhancements
- [ ] Stakeholder view selector
- [ ] Interactive ROI calculator
- [ ] Export formats (PDF, PPT)
- [ ] API endpoints for stakeholder content

### Future 🎯
- [ ] Real benchmarking database
- [ ] AI agent integration
- [ ] Automated report scheduling
- [ ] Multi-customer comparison
- [ ] Historical trend analysis

---

## 🚀 Quick Start for Developers

### Using the ROI Engine
```python
from app.roi_engine import ROIEngine

# Initialize with industry
roi_engine = ROIEngine(industry='manufacturing')

# Calculate risk avoidance ROI
roi = roi_engine.calculate_risk_avoidance_roi(
    investment=180000,
    incidents_prevented=3,
    avg_incident_duration_hours=6.0
)

print(roi['presentation'])
# Output: "Your $180,000 investment prevents $1,512,000 in lost revenue. ROI: 8.4x"
```

### Using the Stakeholder Content Generator
```python
from app.stakeholder_content import StakeholderContentGenerator

stakeholder_gen = StakeholderContentGenerator()

# Generate executive one-pager
onepager = stakeholder_gen.generate_executive_onepager(
    customer_name="Acme Manufacturing",
    overall_score=74.0,
    roi_data=roi,
    top_risks=gaps[:3],
    top_recommendations=recommendations[:3]
)

print(onepager['what_we_found'])
# Output: List of 3 key findings in executive language
```

---

## 📚 Documentation

### Industry Parameters
Each industry has specific parameters:
- **Downtime cost per hour** - Used in ROI calculations
- **Compliance frameworks** - Relevant standards
- **Key metrics** - Industry-specific KPIs
- **Breach cost multiplier** - Impact factor

### ROI Formats
1. **Risk Avoidance** - Best for manufacturing, finance, healthcare
2. **Efficiency Unlock** - Best for nonprofits, operations teams
3. **Compliance Score** - Best for government, finance, healthcare
4. **Three-Year Stacked** - Best for budget-conscious organizations

### Stakeholder Content Types
1. **Executive One-Pager** - 30-second read, visual + bullets
2. **Board Talking Points** - Pre-written statements
3. **Budget Justification** - Internal approval template
4. **Monthly Scorecard** - Progress tracking
5. **Three-Tier Content** - Role-specific views

---

## 🔧 Configuration

Add to `.env`:
```bash
# Industry-specific settings (optional overrides)
MANUFACTURING_DOWNTIME_COST=84000
FINANCIAL_DOWNTIME_COST=50000
HEALTHCARE_DOWNTIME_COST=120000

# ROI calculation defaults
DEFAULT_COST_PER_HOUR=50
DEFAULT_EFFICIENCY_MULTIPLIER=1.5

# Benchmarking (future)
ENABLE_PEER_BENCHMARKING=false
BENCHMARK_DATA_SOURCE=internal
```

---

## 📈 Success Metrics

### For MSPs
- **Time savings**: 15 hours → 3 hours per SBR (5x efficiency)
- **Customer retention**: Higher engagement through stakeholder content
- **Upsell rate**: Tiered budget recommendations drive expansion

### For Customers
- **Budget approval rate**: Faster approvals with ROI justification
- **Stakeholder satisfaction**: Role-specific content resonates
- **Operational clarity**: Monthly scorecards track progress

---

## 🤝 Contributing

To continue implementation:

1. **Complete Phase 2 Integration**
   - Update `main.py` with ROI and stakeholder generation
   - Add database fields
   - Update report templates

2. **Test with Real Data**
   - Use actual customer data
   - Validate ROI calculations
   - Verify stakeholder content quality

3. **Build UI Enhancements**
   - Industry selector
   - Stakeholder view switcher
   - Interactive ROI calculator

4. **Add Export Capabilities**
   - PDF one-pagers
   - PowerPoint presentations
   - Email templates

---

## 📞 Support

For questions or implementation assistance:
- Review Notion requirements: https://www.notion.so/291189c0dfab81129256edf646b08927
- Check this implementation roadmap
- Review code in `app/roi_engine.py` and `app/stakeholder_content.py`

---

**Last Updated:** October 19, 2025
**Version:** 2.1 (Framework Foundation)
**Status:** Phase 1 Complete, Phase 2 In Progress

