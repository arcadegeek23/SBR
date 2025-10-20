-- Migration: Add Lifecycle Manager X tables
-- Date: 2025-10-19

-- Client Goals table
CREATE TABLE IF NOT EXISTS client_goals (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    priority VARCHAR(20) DEFAULT 'medium',
    target_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'not_started',
    progress_percentage INTEGER DEFAULT 0,
    linked_initiatives JSONB,
    owner VARCHAR(255),
    stakeholders JSONB,
    success_metrics JSONB,
    current_value VARCHAR(100),
    target_value VARCHAR(100)
);

CREATE INDEX idx_goals_customer ON client_goals(customer_id);
CREATE INDEX idx_goals_status ON client_goals(status);

-- Meetings table
CREATE TABLE IF NOT EXISTS meetings (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    meeting_type VARCHAR(50),
    description TEXT,
    scheduled_date TIMESTAMP NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    location VARCHAR(255),
    google_event_id VARCHAR(255),
    outlook_event_id VARCHAR(255),
    agenda JSONB,
    notes TEXT,
    action_items JSONB,
    decisions JSONB,
    attendees JSONB,
    status VARCHAR(20) DEFAULT 'scheduled',
    recording_url VARCHAR(500),
    attachments JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255)
);

CREATE INDEX idx_meetings_customer ON meetings(customer_id);
CREATE INDEX idx_meetings_date ON meetings(scheduled_date);
CREATE INDEX idx_meetings_status ON meetings(status);

-- Client Agreements table
CREATE TABLE IF NOT EXISTS client_agreements (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    agreement_name VARCHAR(255) NOT NULL,
    agreement_type VARCHAR(50),
    monthly_mrr DECIMAL(10,2) NOT NULL DEFAULT 0.0,
    annual_value DECIMAL(10,2),
    billing_frequency VARCHAR(20) DEFAULT 'monthly',
    start_date DATE NOT NULL,
    end_date DATE,
    renewal_date DATE,
    contract_term_months INTEGER DEFAULT 12,
    status VARCHAR(20) DEFAULT 'active',
    auto_renew BOOLEAN DEFAULT TRUE,
    services JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agreements_customer ON client_agreements(customer_id);
CREATE INDEX idx_agreements_status ON client_agreements(status);

-- Client Segmentation table
CREATE TABLE IF NOT EXISTS client_segmentation (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) UNIQUE NOT NULL,
    tier VARCHAR(20),
    tier_score DECIMAL(5,2),
    total_mrr DECIMAL(10,2) DEFAULT 0.0,
    mrr_trend VARCHAR(20),
    mrr_change_percentage DECIMAL(5,2),
    lifetime_value DECIMAL(10,2),
    customer_since DATE,
    tenure_months INTEGER,
    health_score DECIMAL(5,2),
    health_status VARCHAR(20),
    last_meeting_date TIMESTAMP,
    meetings_per_quarter INTEGER DEFAULT 0,
    last_report_date TIMESTAMP,
    risk_level VARCHAR(20) DEFAULT 'low',
    risk_factors JSONB,
    strategic_account BOOLEAN DEFAULT FALSE,
    growth_potential VARCHAR(20),
    tags JSONB,
    last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calculation_version VARCHAR(20) DEFAULT '1.0'
);

CREATE INDEX idx_segmentation_customer ON client_segmentation(customer_id);
CREATE INDEX idx_segmentation_tier ON client_segmentation(tier);
CREATE INDEX idx_segmentation_health ON client_segmentation(health_status);

-- Action Items table
CREATE TABLE IF NOT EXISTS action_items (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    meeting_id INTEGER REFERENCES meetings(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    assigned_to VARCHAR(255),
    assigned_by VARCHAR(255),
    due_date DATE,
    completed_date DATE,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_action_items_customer ON action_items(customer_id);
CREATE INDEX idx_action_items_meeting ON action_items(meeting_id);
CREATE INDEX idx_action_items_status ON action_items(status);

-- Calendar Integration Config table
CREATE TABLE IF NOT EXISTS calendar_config (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(20) NOT NULL,
    client_id VARCHAR(255),
    client_secret VARCHAR(255),
    redirect_uri VARCHAR(500),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default calendar configs
INSERT INTO calendar_config (provider, enabled) 
VALUES ('microsoft', FALSE), ('gmail', FALSE)
ON CONFLICT DO NOTHING;

COMMENT ON TABLE client_goals IS 'Client business goals and objectives tracking';
COMMENT ON TABLE meetings IS 'Client meetings, QBRs, and check-ins';
COMMENT ON TABLE client_agreements IS 'Client service agreements and MRR tracking';
COMMENT ON TABLE client_segmentation IS 'Auto-calculated client tiers and health scores';
COMMENT ON TABLE action_items IS 'Action items from meetings and reports';
COMMENT ON TABLE calendar_config IS 'Calendar integration configuration';

