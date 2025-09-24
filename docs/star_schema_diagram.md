# Claims Data Warehouse - Star Schema Design

## Entity Relationship Diagram

```
                    ┌─────────────────────────────────────┐
                    │           dim_date                  │
                    │─────────────────────────────────────│
                    │ • date_key (PK)                     │
                    │   calendar_date                     │
                    │   year                              │
                    │   month                             │
                    │   quarter                           │
                    │   day_of_week                       │
                    │   fiscal_year                       │
                    │   is_holiday                        │
                    │   is_business_day                   │
                    └─────────────────────────────────────┘
                                       │
                                       │
┌─────────────────────────────────────┐│┌─────────────────────────────────────┐
│         dim_providers               │││         dim_beneficiaries           │
│─────────────────────────────────────│││─────────────────────────────────────│
│ • provider_id (PK)                  │││ • beneficiary_id (PK)               │
│   provider_npi                      │││   beneficiary_code                  │
│   provider_name                     │││   date_of_birth                     │
│   provider_type                     │││   date_of_death                     │
│   specialty_code                    │││   gender                            │
│   specialty_description             │││   age                               │
│   provider_state                    │││   age_group                         │
│   provider_city                     │││   chronic_kidney_disease            │
│   is_individual                     │││   alzheimers_dementia               │
│   claims_volume_tier                │││   heart_failure                     │
│   avg_claim_amount                  │││   chronic_lung_disease              │
│   performance_tier                  │││   depression                        │
│   risk_classification               │││   diabetes                          │
└─────────────────────────────────────┘││   ischemic_heart_disease            │
                 │                     ││   osteoporosis                      │
                 │                     ││   rheumatoid_arthritis              │
                 │                     ││   stroke                            │
                 │                     ││   chronic_condition_count           │
                 │                     ││   risk_score                        │
                 │                     ││   risk_tier                         │
                 │                     │└─────────────────────────────────────┘
                 │                     │                   │
                 │                     │                   │
                 └─────────────────────┼───────────────────┘
                                       │
                   ┌───────────────────────────────────────────────────┐
                   │                fact_claims                        │
                   │───────────────────────────────────────────────────│
                   │ • claim_id (PK)                                   │
                   │ • beneficiary_id (FK) → dim_beneficiaries         │
                   │ • provider_id (FK) → dim_providers                │
                   │ • claim_start_date_key (FK) → dim_date            │
                   │ • claim_end_date_key (FK) → dim_date              │
                   │ • admission_date_key (FK) → dim_date              │
                   │ • discharge_date_key (FK) → dim_date              │
                   │                                                   │
                   │ MEASURES:                                         │
                   │   claim_payment_amount                            │
                   │   reimbursement_amount                            │
                   │   patient_responsibility_amount                   │
                   │   claim_total_charge_amount                       │
                   │   processing_days                                 │
                   │   service_days                                    │
                   │   length_of_stay                                  │
                   │                                                   │
                   │ DIMENSIONS:                                       │
                   │   claim_type                                      │
                   │   service_type_code                               │
                   │   diagnosis_code_1                                │
                   │   diagnosis_code_2                                │
                   │   diagnosis_code_3                                │
                   │   procedure_code_1                                │
                   │   procedure_code_2                                │
                   │   procedure_code_3                                │
                   │                                                   │
                   │ FLAGS:                                            │
                   │   is_denied                                       │
                   │   is_high_cost                                    │
                   │   is_emergency                                    │
                   │   has_complications                               │
                   └───────────────────────────────────────────────────┘
```

## Key Design Principles

### 1. Star Schema Benefits
- **Query Performance**: Simplified joins between fact and dimension tables
- **Business Intelligence**: Intuitive structure for analytics tools
- **Scalability**: Efficient for large-scale healthcare data processing
- **Maintainability**: Clear separation of business entities

### 2. Fact Table Design
- **Grain**: One row per claim transaction
- **Measures**: Financial and operational metrics
- **Foreign Keys**: Links to all dimension tables
- **Additive Measures**: Claim amounts, processing days, service days
- **Semi-Additive**: Counts and flags for analysis

### 3. Dimension Design
- **Slowly Changing Dimensions**: Type 2 for provider and beneficiary changes
- **Business Keys**: Natural keys preserved alongside surrogate keys
- **Hierarchies**: Geographic, temporal, and clinical hierarchies
- **Rich Attributes**: Comprehensive business context for analysis

## Business Intelligence Queries

### Sample Analytics Enabled by This Design

```sql
-- Provider Performance Analysis
SELECT
    p.specialty_description,
    p.provider_state,
    COUNT(*) as claim_count,
    AVG(f.claim_payment_amount) as avg_claim_amount,
    AVG(f.processing_days) as avg_processing_days,
    SUM(CASE WHEN f.is_denied THEN 1 ELSE 0 END)::float / COUNT(*) as denial_rate
FROM fact_claims f
JOIN dim_providers p ON f.provider_id = p.provider_id
JOIN dim_date d ON f.claim_start_date_key = d.date_key
WHERE d.year = 2009
GROUP BY p.specialty_description, p.provider_state;

-- Member Risk Analysis
SELECT
    b.age_group,
    b.risk_tier,
    COUNT(DISTINCT b.beneficiary_id) as member_count,
    SUM(f.claim_payment_amount) as total_cost,
    AVG(f.claim_payment_amount) as avg_cost_per_claim,
    AVG(b.chronic_condition_count) as avg_conditions
FROM fact_claims f
JOIN dim_beneficiaries b ON f.beneficiary_id = b.beneficiary_id
GROUP BY b.age_group, b.risk_tier;

-- Time Series Analysis
SELECT
    d.year,
    d.month,
    f.claim_type,
    COUNT(*) as claim_volume,
    SUM(f.claim_payment_amount) as total_payments,
    AVG(f.processing_days) as avg_processing_time
FROM fact_claims f
JOIN dim_date d ON f.claim_start_date_key = d.date_key
GROUP BY d.year, d.month, f.claim_type
ORDER BY d.year, d.month, f.claim_type;
```

## Data Model Cardinalities

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| dim_beneficiaries ↔ fact_claims | 1:M | One beneficiary can have many claims |
| dim_providers ↔ fact_claims | 1:M | One provider can process many claims |
| dim_date ↔ fact_claims | 1:M | Multiple date relationships per claim |

## Performance Optimizations

### Indexing Strategy
```sql
-- Fact table indexes
CREATE INDEX idx_fact_claims_beneficiary ON fact_claims(beneficiary_id);
CREATE INDEX idx_fact_claims_provider ON fact_claims(provider_id);
CREATE INDEX idx_fact_claims_dates ON fact_claims(claim_start_date_key, claim_end_date_key);
CREATE INDEX idx_fact_claims_type ON fact_claims(claim_type);

-- Dimension table indexes
CREATE INDEX idx_dim_providers_specialty ON dim_providers(specialty_code);
CREATE INDEX idx_dim_beneficiaries_risk ON dim_beneficiaries(risk_tier);
CREATE INDEX idx_dim_date_year_month ON dim_date(year, month);
```

### Partitioning Strategy
```sql
-- Partition fact table by date for improved query performance
CREATE TABLE fact_claims (
    -- columns...
) PARTITION BY RANGE (claim_start_date_key);

-- Create monthly partitions
CREATE TABLE fact_claims_2009_01 PARTITION OF fact_claims
    FOR VALUES FROM (20090101) TO (20090201);
```

This star schema design enables efficient analytics across multiple business dimensions while maintaining query performance and data integrity.