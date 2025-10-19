#!/bin/bash

# SBR Generator Test Script
# This script tests all API endpoints and functionality

set -e

BASE_URL="http://localhost:5000"
TEST_CUSTOMER_ID="TEST001"

echo "=========================================="
echo "SBR Generator - Test Suite"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Health Check
echo "Test 1: Health Check Endpoint"
RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL/health")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" -eq 200 ] && echo "$BODY" | grep -q "healthy"; then
    print_result 0 "Health check endpoint"
else
    print_result 1 "Health check endpoint (HTTP $HTTP_CODE)"
fi
echo ""

# Test 2: Generate Review
echo "Test 2: Generate Review"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/generate-review" \
    -H "Content-Type: application/json" \
    -d "{\"customer_id\": \"$TEST_CUSTOMER_ID\"}")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" -eq 200 ] && echo "$BODY" | grep -q "success"; then
    print_result 0 "Generate review endpoint"
    REPORT_ID=$(echo "$BODY" | grep -o '"report_id":[0-9]*' | grep -o '[0-9]*')
    echo "   Generated Report ID: $REPORT_ID"
else
    print_result 1 "Generate review endpoint (HTTP $HTTP_CODE)"
    echo "   Response: $BODY"
fi
echo ""

# Wait a moment for report generation
sleep 2

# Test 3: List Reports
echo "Test 3: List Reports"
RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/reports")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" -eq 200 ] && echo "$BODY" | grep -q "reports"; then
    print_result 0 "List reports endpoint"
    REPORT_COUNT=$(echo "$BODY" | grep -o '"id":' | wc -l)
    echo "   Total reports: $REPORT_COUNT"
else
    print_result 1 "List reports endpoint (HTTP $HTTP_CODE)"
fi
echo ""

# Test 4: Get Specific Report
if [ ! -z "$REPORT_ID" ]; then
    echo "Test 4: Get Specific Report"
    RESPONSE=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/reports/$REPORT_ID")
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    
    if [ "$HTTP_CODE" -eq 200 ] && echo "$BODY" | grep -q "customer_name"; then
        print_result 0 "Get specific report endpoint"
        
        # Extract key metrics
        OVERALL_SCORE=$(echo "$BODY" | grep -o '"overall_score":[0-9.]*' | grep -o '[0-9.]*' | head -1)
        GAPS_COUNT=$(echo "$BODY" | grep -o '"gaps":\[' | wc -l)
        
        echo "   Overall Score: $(echo "$OVERALL_SCORE * 100" | bc)%"
        echo "   Gaps Identified: $GAPS_COUNT"
    else
        print_result 1 "Get specific report endpoint (HTTP $HTTP_CODE)"
    fi
    echo ""
fi

# Test 5: Download Markdown Report
if [ ! -z "$REPORT_ID" ]; then
    echo "Test 5: Download Markdown Report"
    HTTP_CODE=$(curl -s -o /tmp/test_report.md -w "%{http_code}" "$BASE_URL/api/reports/$REPORT_ID/download/markdown")
    
    if [ "$HTTP_CODE" -eq 200 ] && [ -f /tmp/test_report.md ] && [ -s /tmp/test_report.md ]; then
        print_result 0 "Download Markdown report"
        FILE_SIZE=$(wc -c < /tmp/test_report.md)
        echo "   File size: $FILE_SIZE bytes"
    else
        print_result 1 "Download Markdown report (HTTP $HTTP_CODE)"
    fi
    echo ""
fi

# Test 6: Download HTML Report
if [ ! -z "$REPORT_ID" ]; then
    echo "Test 6: Download HTML Report"
    HTTP_CODE=$(curl -s -o /tmp/test_report.html -w "%{http_code}" "$BASE_URL/api/reports/$REPORT_ID/download/html")
    
    if [ "$HTTP_CODE" -eq 200 ] && [ -f /tmp/test_report.html ] && [ -s /tmp/test_report.html ]; then
        print_result 0 "Download HTML report"
        FILE_SIZE=$(wc -c < /tmp/test_report.html)
        echo "   File size: $FILE_SIZE bytes"
    else
        print_result 1 "Download HTML report (HTTP $HTTP_CODE)"
    fi
    echo ""
fi

# Test 7: Download PDF Report
if [ ! -z "$REPORT_ID" ]; then
    echo "Test 7: Download PDF Report"
    HTTP_CODE=$(curl -s -o /tmp/test_report.pdf -w "%{http_code}" "$BASE_URL/api/reports/$REPORT_ID/download/pdf")
    
    if [ "$HTTP_CODE" -eq 200 ] && [ -f /tmp/test_report.pdf ] && [ -s /tmp/test_report.pdf ]; then
        print_result 0 "Download PDF report"
        FILE_SIZE=$(wc -c < /tmp/test_report.pdf)
        echo "   File size: $FILE_SIZE bytes"
    else
        print_result 1 "Download PDF report (HTTP $HTTP_CODE)"
    fi
    echo ""
fi

# Test 8: View Report in Browser
if [ ! -z "$REPORT_ID" ]; then
    echo "Test 8: View Report in Browser"
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/view/$REPORT_ID")
    
    if [ "$HTTP_CODE" -eq 200 ]; then
        print_result 0 "View report in browser"
    else
        print_result 1 "View report in browser (HTTP $HTTP_CODE)"
    fi
    echo ""
fi

# Test 9: Invalid Customer ID
echo "Test 9: Error Handling - Invalid Request"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/generate-review" \
    -H "Content-Type: application/json" \
    -d "{}")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" -eq 400 ] && echo "$BODY" | grep -q "error"; then
    print_result 0 "Error handling for invalid request"
else
    print_result 1 "Error handling for invalid request (HTTP $HTTP_CODE)"
fi
echo ""

# Test 10: Database Persistence
echo "Test 10: Database Persistence"
RESPONSE1=$(curl -s "$BASE_URL/api/reports")
REPORT_COUNT1=$(echo "$RESPONSE1" | grep -o '"id":' | wc -l)

# Generate another report
curl -s -X POST "$BASE_URL/api/generate-review" \
    -H "Content-Type: application/json" \
    -d "{\"customer_id\": \"TEST002\"}" > /dev/null

sleep 2

RESPONSE2=$(curl -s "$BASE_URL/api/reports")
REPORT_COUNT2=$(echo "$RESPONSE2" | grep -o '"id":' | wc -l)

if [ "$REPORT_COUNT2" -gt "$REPORT_COUNT1" ]; then
    print_result 0 "Database persistence"
    echo "   Reports before: $REPORT_COUNT1, after: $REPORT_COUNT2"
else
    print_result 1 "Database persistence"
fi
echo ""

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${YELLOW}Some tests failed. Please review the output above.${NC}"
    exit 1
fi

