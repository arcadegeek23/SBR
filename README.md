# SBR Generator - Strategic Business Review

Automated Strategic Business Review (SBR) generator for Computer Integration Technologies (CIT). This application integrates with HaloPSA to generate comprehensive security assessments aligned with the NIST Cybersecurity Framework.

## Features

- **Automated Data Extraction**: Pulls customer, asset, ticket, and user data from HaloPSA
- **NIST CSF Scoring**: Calculates security posture across all five NIST categories (Identify, Protect, Detect, Respond, Recover)
- **Gap Analysis**: Identifies security gaps and risks based on configurable thresholds
- **Actionable Recommendations**: Generates prioritized, budgeted recommendations
- **Multi-Format Reports**: Exports reports in Markdown, HTML, and PDF formats
- **Modern UI**: Beautiful web interface for generating and viewing reports
- **Mock Data Support**: Test and demo without live Halo API access

## Architecture

### Components

- **Flask Web Application**: REST API and web UI
- **PostgreSQL Database**: Stores report history and metadata
- **HaloPSA Connector**: Integrates with Halo API (with mock data fallback)
- **Signal Processor**: Normalizes raw data into security metrics
- **Scoring Engine**: Calculates NIST CSF scores and identifies gaps
- **Budget Engine**: Estimates costs for remediation recommendations
- **Report Builder**: Generates reports in multiple formats

### Technology Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Database**: PostgreSQL 15
- **PDF Generation**: WeasyPrint
- **Deployment**: Docker, Docker Compose
- **Web Server**: Gunicorn

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (optional)

### Installation

1. **Clone or download the repository**

```bash
git clone <repository-url>
cd sbr
```

2. **Configure environment variables**

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here

# HaloPSA API Configuration (for live data)
HALO_API_URL=https://your-halo-instance.halopsa.com/api
HALO_API_KEY=your-api-key
HALO_CLIENT_ID=your-client-id
HALO_CLIENT_SECRET=your-client-secret
USE_MOCK_DATA=true  # Set to false for live Halo integration

# Unit Costs (customize as needed)
COST_MFA_PER_USER=3.00
COST_EDR_PER_ENDPOINT=5.50
COST_BACKUP_PER_SERVER=45.00
COST_SIEM_PER_USER=6.50

# Thresholds
THRESHOLD_PATCH_COMPLIANCE=95
THRESHOLD_BACKUP_SUCCESS=98
THRESHOLD_EDR_COVERAGE=90
THRESHOLD_SLA_ATTAINMENT=90
```

3. **Start the application**

```bash
docker-compose up -d
```

4. **Access the application**

Open your browser to: **http://localhost:5000**

## Usage

### Web Interface

1. Navigate to http://localhost:5000
2. Enter a Customer ID (any value works with mock data)
3. Click "Generate Review"
4. View, download, or share the generated reports

### API Endpoints

#### Generate Review

```bash
POST /api/generate-review
Content-Type: application/json

{
  "customer_id": "CUST001"
}
```

Response:
```json
{
  "success": true,
  "report_id": 1,
  "customer_name": "Acme Corporation CUST001",
  "overall_score": 0.75,
  "total_monthly_cost": 1250.00,
  "gaps_count": 3,
  "reports": {
    "markdown": "sbr_CUST001_20250118_143022.md",
    "html": "sbr_CUST001_20250118_143022.html",
    "pdf": "sbr_CUST001_20250118_143022.pdf"
  }
}
```

#### List Reports

```bash
GET /api/reports
```

#### Get Specific Report

```bash
GET /api/reports/{report_id}
```

#### Download Report

```bash
GET /api/reports/{report_id}/download/{format}
# format: markdown, html, or pdf
```

#### View Report in Browser

```bash
GET /view/{report_id}
```

#### Health Check

```bash
GET /health
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `development` |
| `SECRET_KEY` | Flask secret key | Required |
| `DATABASE_URL` | PostgreSQL connection string | Auto-configured |
| `HALO_API_URL` | HaloPSA API base URL | Required for live data |
| `HALO_API_KEY` | HaloPSA API key | Required for live data |
| `HALO_CLIENT_ID` | HaloPSA OAuth client ID | Required for live data |
| `HALO_CLIENT_SECRET` | HaloPSA OAuth client secret | Required for live data |
| `USE_MOCK_DATA` | Use mock data instead of live API | `true` |
| `COST_MFA_PER_USER` | Monthly cost per user for MFA | `3.00` |
| `COST_EDR_PER_ENDPOINT` | Monthly cost per endpoint for EDR | `5.50` |
| `COST_BACKUP_PER_SERVER` | Monthly cost per server for backup | `45.00` |
| `COST_SIEM_PER_USER` | Monthly cost per user for SIEM | `6.50` |
| `THRESHOLD_PATCH_COMPLIANCE` | Minimum patch compliance % | `95` |
| `THRESHOLD_BACKUP_SUCCESS` | Minimum backup coverage % | `98` |
| `THRESHOLD_EDR_COVERAGE` | Minimum EDR coverage % | `90` |
| `THRESHOLD_SLA_ATTAINMENT` | Minimum SLA attainment % | `90` |

### Switching to Live Halo Data

1. Update `.env` with your HaloPSA credentials:
   ```env
   HALO_API_URL=https://your-instance.halopsa.com/api
   HALO_API_KEY=your-api-key
   HALO_CLIENT_ID=your-client-id
   HALO_CLIENT_SECRET=your-client-secret
   USE_MOCK_DATA=false
   ```

2. Restart the application:
   ```bash
   docker-compose restart web
   ```

## Development

### Running Locally (Without Docker)

1. **Create virtual environment**

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL**

Install and start PostgreSQL, then create database:

```sql
CREATE DATABASE sbr_db;
CREATE USER sbr_user WITH PASSWORD 'sbr_password';
GRANT ALL PRIVILEGES ON DATABASE sbr_db TO sbr_user;
```

4. **Run the application**

```bash
export FLASK_APP=app.main
export FLASK_ENV=development
flask run
```

### Project Structure

```
sbr/
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask application and routes
│   ├── models.py            # Database models
│   ├── config.py            # Configuration
│   ├── halo_connector.py    # HaloPSA API integration
│   ├── signal_processor.py  # Data normalization
│   ├── scoring_engine.py    # NIST CSF scoring
│   ├── budget_engine.py     # Cost estimation
│   └── report_builder.py    # Report generation
├── templates/
│   ├── index.html           # Web UI
│   ├── report_template.md   # Markdown template
│   └── report_template.html # HTML template
├── static/
│   ├── css/
│   └── js/
├── reports/                 # Generated reports
├── .env                     # Environment configuration
├── .env.example             # Example configuration
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration
└── README.md               # This file
```

## NIST CSF Methodology

### Categories and Mappings

| NIST Category | Signals | Weight |
|---------------|---------|--------|
| **Identify** | Asset inventory | 15% |
| **Protect** | Patch compliance, MFA, EDR, Backup | 30% |
| **Detect** | EDR coverage | 20% |
| **Respond** | SLA attainment | 20% |
| **Recover** | Backup coverage | 15% |

### Scoring Logic

- Each signal is normalized to a 0-1 scale
- Category scores are calculated as averages of relevant signals
- Overall score is a weighted average of all categories
- Gaps are identified when signals fall below configured thresholds

### Gap Severity Levels

- **Critical**: MFA disabled, backup coverage < 98%
- **High**: Patch compliance < 95%, EDR coverage < 90%
- **Medium**: SLA attainment < 90%

## Troubleshooting

### Application won't start

```bash
# Check logs
docker-compose logs web

# Verify database is healthy
docker-compose ps
```

### Database connection errors

```bash
# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

### PDF generation fails

WeasyPrint requires system dependencies. If running without Docker, install:

```bash
# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0

# macOS
brew install pango
```

### Reports not saving

```bash
# Check reports directory permissions
ls -la reports/

# Ensure directory exists and is writable
mkdir -p reports
chmod 755 reports
```

## Deployment

### Production Considerations

1. **Change default passwords and secrets**
   - Update `SECRET_KEY` in `.env`
   - Change PostgreSQL password in `docker-compose.yml` and `.env`

2. **Use a reverse proxy**
   - Deploy behind Nginx or Traefik for SSL/TLS
   - Configure proper domain and certificates

3. **Enable backups**
   - Set up automated PostgreSQL backups
   - Back up the `reports/` directory

4. **Monitor resources**
   - Monitor CPU, memory, and disk usage
   - Set up logging and alerting

5. **Scale workers**
   - Adjust Gunicorn workers in `Dockerfile` based on CPU cores
   - Consider load balancing for high traffic

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name sbr.yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Roadmap

### Phase 3 (Planned)
- [ ] Enhanced budget models with per-customer pricing
- [ ] Report versioning and historical comparison
- [ ] Scheduled auto-generation (weekly/monthly)

### Phase 4 (Future)
- [ ] CSP MFA data integration (Azure AD, M365)
- [ ] Advanced PDF customization
- [ ] Lightweight admin UI for configuration

### Phase 5 (Future)
- [ ] Dashboard with trend analysis
- [ ] Multi-customer comparison and benchmarking
- [ ] Export to PowerPoint

## Support

For issues, questions, or feature requests, please contact Computer Integration Technologies support.

## License

Proprietary - Computer Integration Technologies (CIT)

---

**Built with ❤️ by CIT Engineering Team**

