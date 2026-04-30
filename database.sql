-- Run this in your Supabase SQL editor

-- Table: responses
CREATE TABLE IF NOT EXISTS responses (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    sex VARCHAR(20) NOT NULL,
    civil_status VARCHAR(50) NOT NULL,
    duration_of_hospitalization VARCHAR(100) NOT NULL,
    ward VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: survey_responses
CREATE TABLE IF NOT EXISTS survey_responses (
    id BIGSERIAL PRIMARY KEY,
    response_id BIGINT NOT NULL REFERENCES responses(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    question TEXT NOT NULL,
    rating SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: admin_users
CREATE TABLE IF NOT EXISTS admin_users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Default admin (username: admin / password: admin123)
INSERT INTO admin_users (username, password_hash)
VALUES ('admin', 'admin123')
ON CONFLICT (username) DO NOTHING;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_survey_responses_response_id ON survey_responses(response_id);
CREATE INDEX IF NOT EXISTS idx_survey_responses_category ON survey_responses(category);

-- Disable RLS (using service key from backend only)
ALTER TABLE responses DISABLE ROW LEVEL SECURITY;
ALTER TABLE survey_responses DISABLE ROW LEVEL SECURITY;
ALTER TABLE admin_users DISABLE ROW LEVEL SECURITY;
