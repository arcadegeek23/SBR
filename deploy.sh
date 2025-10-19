#!/bin/bash

# SBR Generator Deployment Script
# This script helps deploy and test the SBR application

set -e

echo "=========================================="
echo "SBR Generator - Deployment Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✓ Docker is installed"

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose plugin."
    exit 1
fi

echo "✓ Docker Compose is available"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✓ Created .env file. Please review and update configuration."
fi

echo ""
echo "=========================================="
echo "Building Docker Images"
echo "=========================================="
docker compose build

echo ""
echo "=========================================="
echo "Starting Services"
echo "=========================================="
docker compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo "✓ Services are running"
else
    echo "❌ Services failed to start. Check logs with: docker compose logs"
    exit 1
fi

echo ""
echo "=========================================="
echo "Service Status"
echo "=========================================="
docker compose ps

echo ""
echo "=========================================="
echo "Testing Application"
echo "=========================================="

# Wait for web service to be ready
echo "Waiting for web application to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:5000/health > /dev/null; then
        echo "✓ Web application is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Web application failed to start"
        docker compose logs web
        exit 1
    fi
    sleep 2
done

# Test health endpoint
echo ""
echo "Testing /health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:5000/health)
echo "Response: $HEALTH_RESPONSE"

if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo "✓ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "Deployment Successful! 🎉"
echo "=========================================="
echo ""
echo "Access the application at: http://localhost:5000"
echo ""
echo "Useful commands:"
echo "  View logs:        docker compose logs -f"
echo "  Stop services:    docker compose down"
echo "  Restart services: docker compose restart"
echo "  View status:      docker compose ps"
echo ""
echo "To test report generation, run:"
echo "  ./test.sh"
echo ""

