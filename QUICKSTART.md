# Quick Start Guide - SBR Generator

Get up and running with the Strategic Business Review Generator in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- 2GB free disk space
- Ports 5000 and 5432 available

## Installation Steps

### 1. Extract the Application

```bash
unzip sbr.zip
cd sbr
```

### 2. Configure Environment (Optional)

The application works out of the box with mock data. To customize:

```bash
nano .env
```

Key settings:
- `USE_MOCK_DATA=true` - Use mock data (default)
- `SECRET_KEY` - Change for production
- `HALO_API_*` - Configure for live Halo integration

### 3. Deploy the Application

```bash
./deploy.sh
```

This script will:
- Build Docker images
- Start all services
- Run health checks
- Display access information

### 4. Access the Application

Open your browser to: **http://localhost:5000**

## First Report

1. Enter any Customer ID (e.g., `CUST001`)
2. Click "Generate Review"
3. Wait 5-10 seconds for generation
4. View, download, or share the report

## Testing

Run the comprehensive test suite:

```bash
./test.sh
```

This validates all endpoints and functionality.

## Common Commands

### View Logs
```bash
docker compose logs -f web
```

### Restart Services
```bash
docker compose restart
```

### Stop Application
```bash
docker compose down
```

### Start Application
```bash
docker compose up -d
```

### Check Status
```bash
docker compose ps
```

## Troubleshooting

### Port Already in Use

If port 5000 is in use, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # Change 5000 to 8080
```

Then access at: http://localhost:8080

### Database Connection Issues

```bash
# Restart database
docker compose restart db

# View database logs
docker compose logs db
```

### Reports Not Generating

```bash
# Check web service logs
docker compose logs web

# Ensure reports directory is writable
chmod 755 reports/
```

## Using Live Halo Data

1. Edit `.env`:
   ```env
   USE_MOCK_DATA=false
   HALO_API_URL=https://your-instance.halopsa.com/api
   HALO_API_KEY=your-api-key
   HALO_CLIENT_ID=your-client-id
   HALO_CLIENT_SECRET=your-client-secret
   ```

2. Restart the application:
   ```bash
   docker compose restart web
   ```

3. Generate a report with a real customer ID

## API Usage

### Generate Review
```bash
curl -X POST http://localhost:5000/api/generate-review \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "CUST001"}'
```

### List Reports
```bash
curl http://localhost:5000/api/reports
```

### Download Report
```bash
# HTML
curl -O http://localhost:5000/api/reports/1/download/html

# Markdown
curl -O http://localhost:5000/api/reports/1/download/markdown

# PDF
curl -O http://localhost:5000/api/reports/1/download/pdf
```

## Next Steps

- Review the full [README.md](README.md) for detailed documentation
- Customize unit costs and thresholds in `.env`
- Set up automated backups for PostgreSQL
- Configure SSL/TLS for production deployment
- Integrate with your Halo instance

## Support

For issues or questions:
- Check logs: `docker compose logs`
- Review README.md for detailed troubleshooting
- Contact CIT support team

---

**Happy Reviewing! 🎯**

