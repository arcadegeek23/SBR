# SBR Application - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Ubuntu 22.04 or similar Linux distribution
- Python 3.11+
- PostgreSQL 14+
- Internet connection

### Installation Steps

#### 1. Extract the Application
```bash
tar -xzf sbr-application.tar.gz
cd sbr
```

#### 2. Install PostgreSQL
```bash
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
sudo service postgresql start
```

#### 3. Create Database
```bash
sudo -u postgres psql -c "CREATE DATABASE sbr_db;"
sudo -u postgres psql -c "CREATE USER sbr_user WITH PASSWORD 'sbr_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sbr_db TO sbr_user;"
sudo -u postgres psql -c "ALTER DATABASE sbr_db OWNER TO sbr_user;"
```

#### 4. Install Python Dependencies
```bash
pip3 install -r requirements.txt
```

#### 5. Configure Environment
```bash
# The .env file is already configured for local development
# To use live HaloPSA data, edit .env and set:
# - HALO_API_URL
# - HALO_API_KEY
# - HALO_CLIENT_ID
# - HALO_CLIENT_SECRET
# - USE_MOCK_DATA=false
```

#### 6. Start the Application
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app.main:app
```

#### 7. Access the Application
Open your browser to: **http://localhost:5000**

## 🎯 First Report

1. Enter any Customer ID (e.g., "CUST001")
2. Click "Generate Review"
3. Wait 2-3 seconds for generation
4. View or download the report

## 📱 Using the API

### Generate a Report
```bash
curl -X POST http://localhost:5000/api/generate-review \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "CUST001"}'
```

### List All Reports
```bash
curl http://localhost:5000/api/reports
```

### Download Report
```bash
curl http://localhost:5000/api/reports/1/download/html -o report.html
curl http://localhost:5000/api/reports/1/download/markdown -o report.md
```

## 🐳 Docker Deployment (Alternative)

If you prefer Docker:

```bash
# Make sure Docker and Docker Compose are installed
docker-compose up --build -d

# Access at http://localhost:5000
```

## ⚙️ Configuration

### Using Mock Data (Default)
The application comes pre-configured with mock data enabled. This is perfect for:
- Testing and demonstration
- Training users
- Development

### Switching to Live HaloPSA Data
1. Obtain API credentials from HaloPSA
2. Edit `.env`:
   ```env
   HALO_API_URL=https://your-instance.halopsa.com/api
   HALO_API_KEY=your-api-key
   HALO_CLIENT_ID=your-client-id
   HALO_CLIENT_SECRET=your-client-secret
   USE_MOCK_DATA=false
   ```
3. Restart the application

### Customizing Costs and Thresholds
Edit `.env` to adjust:
- `COST_MFA_PER_USER` - Monthly MFA cost per user
- `COST_EDR_PER_ENDPOINT` - Monthly EDR cost per endpoint
- `COST_BACKUP_PER_SERVER` - Monthly backup cost per server
- `COST_SIEM_PER_USER` - Monthly SIEM cost per user
- `THRESHOLD_PATCH_COMPLIANCE` - Minimum patch compliance %
- `THRESHOLD_BACKUP_SUCCESS` - Minimum backup coverage %
- `THRESHOLD_EDR_COVERAGE` - Minimum EDR coverage %
- `THRESHOLD_SLA_ATTAINMENT` - Minimum SLA attainment %

## 🔍 Troubleshooting

### Application won't start
```bash
# Check if PostgreSQL is running
sudo service postgresql status

# Check if port 5000 is available
netstat -tuln | grep 5000

# View application logs
tail -f /tmp/sbr-error.log
```

### Database connection errors
```bash
# Verify database exists
sudo -u postgres psql -l | grep sbr_db

# Test connection
psql -U sbr_user -d sbr_db -h localhost
```

### Reports not generating
```bash
# Check reports directory permissions
ls -la reports/
chmod 755 reports/

# Verify Python dependencies
pip3 list | grep -E "Flask|psycopg2|weasyprint"
```

## 📚 Documentation

- **README.md** - Comprehensive documentation
- **DEPLOYMENT_GUIDE.md** - Detailed deployment instructions
- **QUICK_START.md** - This file

## 🎉 You're Ready!

The application is now running and ready to generate Strategic Business Reviews. Enjoy!

