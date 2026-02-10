-- Initialization script for PostgreSQL
-- This script ensures the user and database are properly configured

-- No need to create database, it's created by POSTGRES_DB env var
-- No need to create user, it's created by POSTGRES_USER env var

-- Just ensure the password is set correctly
ALTER USER medical_user WITH PASSWORD 'medical_pass';

-- Grant all privileges (though superuser already has them)
GRANT ALL PRIVILEGES ON DATABASE medical_db TO medical_user;

-- Create a test table to verify everything works
\c medical_db;

SELECT 'Database initialized successfully!' as status;
