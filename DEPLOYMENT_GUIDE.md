# 🚀 Deployment Guide - Claims Data Warehouse

## Quick Start Deployment

### Prerequisites
- PostgreSQL 13+ database instance
- Python 3.8+ environment
- Git access to this repository
- CMS Medicare Synthetic Claims data

### 1. Environment Setup

```bash
# Clone repository
git clone <your-repo-url>
cd claims-data-warehouse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install dbt packages
dbt deps
```

### 2. Database Configuration

#### Create Databases and Schemas
```sql
-- Connect as superuser and run:
CREATE DATABASE claims_warehouse_dev;
CREATE DATABASE claims_warehouse_staging;
CREATE DATABASE claims_warehouse_prod;

-- Create schemas
\c claims_warehouse_dev;
CREATE SCHEMA raw;
CREATE SCHEMA analytics_dev;

\c claims_warehouse_staging;
CREATE SCHEMA raw;
CREATE SCHEMA analytics_staging;

\c claims_warehouse_prod;
CREATE SCHEMA raw;
CREATE SCHEMA analytics_prod;
```

#### Update Connection Profile
```bash
# Copy template profiles
cp profiles.yml.template ~/.dbt/profiles.yml

# Edit with your database credentials
nano ~/.dbt/profiles.yml
```

### 3. Data Loading

#### Option A: Sample Data (for testing)
```bash
# Create sample data for testing
dbt seed --full-refresh
```

#### Option B: CMS Synthetic Data
1. Download CMS Medicare Synthetic Claims data from [CMS.gov](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs)
2. Load into raw schema using your preferred ETL tool
3. Ensure table names match source definitions in `models/staging/sources.yml`

### 4. Initial Deployment

```bash
# Verify configuration
dbt debug

# Parse project
dbt parse

# Build all models
dbt run

# Run all tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

## Production Deployment

### Infrastructure Requirements

#### Minimum Production Requirements
- **Database**: PostgreSQL 13+ with 4 cores, 16GB RAM
- **Storage**: 500GB+ SSD for data and indexes
- **Network**: Private subnet with bastion host access
- **Backup**: Automated daily backups with point-in-time recovery

#### Recommended Production Setup
- **Database**: PostgreSQL 14+ with 8 cores, 32GB RAM
- **Storage**: 1TB+ NVMe SSD with automated scaling
- **High Availability**: Master-replica setup with failover
- **Monitoring**: Query performance and data quality monitoring

### Security Configuration

#### Database Security
```sql
-- Create dedicated service accounts
CREATE USER dbt_prod WITH PASSWORD 'secure_password_here';
CREATE USER dbt_staging WITH PASSWORD 'secure_password_here';
CREATE USER dbt_dev WITH PASSWORD 'secure_password_here';

-- Grant appropriate permissions
GRANT CONNECT ON DATABASE claims_warehouse_prod TO dbt_prod;
GRANT USAGE, CREATE ON SCHEMA analytics_prod TO dbt_prod;
GRANT SELECT ON ALL TABLES IN SCHEMA raw TO dbt_prod;
```

#### Environment Variables
```bash
# Set in your CI/CD system or .env file
export DBT_USER="dbt_prod"
export DBT_PASSWORD="your_secure_password"
export DBT_PROD_HOST="your-prod-db-host.com"
export DBT_PROD_USER="dbt_prod"
export DBT_PROD_PASSWORD="your_secure_password"
```

### CI/CD Setup

#### GitHub Actions (Included)
The project includes a complete CI/CD pipeline in `.github/workflows/dbt-ci.yml`:

1. **Code Quality**: SQLFluff linting, dbt parsing
2. **Staging Tests**: Full pipeline validation on PR
3. **Production Deploy**: Automated deployment on main branch
4. **Quality Monitoring**: Post-deployment validation

#### GitLab CI (Alternative)
```yaml
# .gitlab-ci.yml example
stages:
  - test
  - deploy

dbt_test:
  stage: test
  script:
    - dbt deps
    - dbt run --target staging
    - dbt test --target staging

dbt_deploy:
  stage: deploy
  script:
    - dbt run --target prod
    - dbt test --target prod
  only:
    - main
```

### Environment Management

#### Development Environment
```yaml
# ~/.dbt/profiles.yml for development
claims_data_warehouse:
  outputs:
    dev:
      type: postgres
      host: localhost
      user: your_username
      password: your_password
      port: 5432
      dbname: claims_warehouse_dev
      schema: analytics_dev
      threads: 4
  target: dev
```

#### Production Environment
```yaml
# Production profile configuration
claims_data_warehouse:
  outputs:
    prod:
      type: postgres
      host: "{{ env_var('DBT_PROD_HOST') }}"
      user: "{{ env_var('DBT_PROD_USER') }}"
      password: "{{ env_var('DBT_PROD_PASSWORD') }}"
      port: 5432
      dbname: claims_warehouse_prod
      schema: analytics_prod
      threads: 8
      keepalives_idle: 0
      search_path: analytics_prod,public
  target: prod
```

## Performance Optimization

### Database Configuration

#### PostgreSQL Settings
```sql
-- postgresql.conf optimizations for analytics workload
shared_buffers = 8GB                    # 25% of total RAM
effective_cache_size = 24GB             # 75% of total RAM
work_mem = 256MB                        # For sort/hash operations
maintenance_work_mem = 2GB              # For VACUUM, CREATE INDEX
random_page_cost = 1.1                  # For SSD storage
effective_io_concurrency = 200          # For SSD
max_parallel_workers_per_gather = 4     # Parallel query execution
```

#### Index Creation
```sql
-- Run after initial deployment for optimal performance
-- Fact table indexes
CREATE INDEX CONCURRENTLY idx_fact_claims_beneficiary
    ON fact_claims USING btree (beneficiary_key);
CREATE INDEX CONCURRENTLY idx_fact_claims_provider
    ON fact_claims USING btree (provider_key);
CREATE INDEX CONCURRENTLY idx_fact_claims_date
    ON fact_claims USING btree (claim_date_key);

-- Composite indexes for common queries
CREATE INDEX CONCURRENTLY idx_fact_claims_date_type
    ON fact_claims USING btree (claim_date_key, claim_type);
```

### dbt Configuration

#### Production Optimizations
```yaml
# dbt_project.yml production settings
models:
  claims_data_warehouse:
    marts:
      core:
        +pre-hook: "SET work_mem = '512MB'"
        +post-hook: [
          "ANALYZE {{ this }}",
          "VACUUM ANALYZE {{ this }}"
        ]
      analytics:
        +pre-hook: "SET work_mem = '1GB'"
        +materialized: table
        +indexes:
          - columns: [metric_date]
            type: btree
```

## Monitoring & Maintenance

### Data Quality Monitoring
```bash
# Daily data quality checks
dbt test --models tag:critical
dbt source freshness

# Weekly comprehensive validation
dbt run-operation generate_data_quality_report
```

### Performance Monitoring
```sql
-- Query to monitor model performance
SELECT
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    last_vacuum,
    last_autovacuum,
    last_analyze
FROM pg_stat_user_tables
WHERE schemaname = 'analytics_prod';
```

### Maintenance Schedule

#### Daily
- Automated data quality tests
- Performance monitoring
- Backup verification

#### Weekly
- Comprehensive test suite
- Performance optimization review
- Data freshness validation

#### Monthly
- Full data quality audit
- Index maintenance and optimization
- Documentation updates
- Security review

## Troubleshooting

### Common Issues

#### Connection Issues
```bash
# Test database connectivity
dbt debug

# Test specific target
dbt debug --target prod
```

#### Performance Issues
```sql
-- Check for missing indexes
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE schemaname = 'analytics_prod' AND n_distinct > 100;

-- Check query performance
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
WHERE query LIKE '%fact_claims%'
ORDER BY total_time DESC;
```

#### Test Failures
```bash
# Run specific failing test
dbt test --select test_name

# Debug test with detailed output
dbt test --select test_name --store-failures
```

### Recovery Procedures

#### Model Failure Recovery
```bash
# Re-run failed model with full refresh
dbt run --select failed_model_name --full-refresh

# Re-run downstream dependencies
dbt run --select failed_model_name+
```

#### Data Corruption Recovery
1. Stop all dbt processes
2. Restore from latest backup
3. Run incremental rebuild from last known good state
4. Validate data quality before resuming normal operations

## Support & Maintenance

### Documentation Maintenance
```bash
# Update documentation after changes
dbt docs generate
dbt docs serve --port 8001
```

### Backup Strategy
- **Frequency**: Daily automated backups
- **Retention**: 30 days full, 1 year monthly
- **Testing**: Monthly restore validation
- **Documentation**: Backup and restore procedures documented

### Version Control
- **Branching**: Feature branches with PR reviews
- **Tagging**: Version tags for production releases
- **Rollback**: Automated rollback capabilities for failed deployments

This deployment guide ensures a smooth transition from development to production with proper monitoring and maintenance procedures.