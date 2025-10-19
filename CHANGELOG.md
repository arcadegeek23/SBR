# Changelog

All notable changes to the SBR Generator project will be documented in this file.

## [1.0.0] - 2025-01-18

### Added
- Initial release of SBR Generator
- Flask web application with REST API
- PostgreSQL database integration
- HaloPSA connector with mock data support
- Signal processor for data normalization
- NIST CSF scoring engine
- Gap analysis and recommendations engine
- Budget estimation engine
- Multi-format report generation (Markdown, HTML, PDF)
- Modern web UI for report generation
- Docker and Docker Compose configuration
- Comprehensive documentation
- Deployment and test scripts

### Features
- **Phase 2 Implementation**: Full Halo API integration with mock data fallback
- **NIST CSF Alignment**: Scoring across all five framework categories
- **Automated Gap Analysis**: Identifies security gaps based on configurable thresholds
- **Budget Projections**: Calculates monthly and annual costs for recommendations
- **Report Persistence**: Stores all generated reports in PostgreSQL
- **Report History**: View and download previous reports
- **Configurable Thresholds**: Customize gap detection via environment variables
- **Configurable Unit Costs**: Adjust pricing models per environment

### Technical Details
- Python 3.11
- Flask 3.0.0
- PostgreSQL 15
- WeasyPrint for PDF generation
- Gunicorn for production deployment
- Docker multi-container architecture
- RESTful API design

### Documentation
- Comprehensive README with installation and usage instructions
- Quick Start Guide for rapid deployment
- API documentation
- Deployment guide
- Troubleshooting section

### Testing
- Automated deployment script
- Comprehensive test suite covering all endpoints
- Health check endpoint
- Error handling validation

## [Planned] - Future Releases

### Phase 3 (Planned)
- Enhanced budget models with per-customer pricing profiles
- Report versioning and historical comparison
- Scheduled auto-generation (weekly/monthly cron jobs)
- Trend analysis and progress tracking

### Phase 4 (Planned)
- CSP MFA data integration (Azure AD, M365)
- Advanced PDF customization and branding
- Lightweight admin UI for configuration management
- Email delivery of reports

### Phase 5 (Planned)
- Interactive dashboard with trend visualization
- Multi-customer comparison and benchmarking
- Natural language query interface
- PowerPoint export
- Teams integration for automated posting

---

For detailed information about each release, see the [README.md](README.md).

