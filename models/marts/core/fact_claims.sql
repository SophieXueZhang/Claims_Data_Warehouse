{{ config(
    materialized='table',
    indexes=[
        {'columns': ['claim_id'], 'unique': true},
        {'columns': ['beneficiary_key']},
        {'columns': ['provider_key']},
        {'columns': ['claim_date_key']},
        {'columns': ['claim_type']},
        {'columns': ['claim_status']},
        {'columns': ['claim_start_date']},
        {'columns': ['processed_date_key']}
    ],
    tags=['fact', 'core', 'claims']
) }}

with claims_with_keys as (
    select
        c.*,
        b.beneficiary_key,
        p.provider_key,
        cast(to_char(c.claim_start_date, 'YYYYMMDD') as integer) as claim_date_key,
        cast(to_char(c.processed_at, 'YYYYMMDD') as integer) as processed_date_key,
        cast(to_char(c.created_at, 'YYYYMMDD') as integer) as created_date_key
    from {{ ref('stg_cms_claims') }} c
    inner join {{ ref('dim_beneficiaries') }} b
        on c.beneficiary_id = b.beneficiary_id
    inner join {{ ref('dim_providers') }} p
        on c.provider_id = p.provider_id
),

final as (
    select
        -- Primary key
        claim_key,

        -- Business key
        claim_id,

        -- Foreign keys
        beneficiary_key,
        provider_key,
        claim_date_key,
        processed_date_key,
        created_date_key,

        -- Claim details
        claim_type,
        claim_status,
        claim_start_date,
        claim_end_date,
        admission_date,
        discharge_date,
        created_at,
        processed_at,

        -- Financial measures
        claim_amount,
        reimbursement_amount,
        primary_payer_amount,
        deductible_amount,
        patient_responsibility,
        reimbursement_ratio,

        -- Derived financial measures
        case
            when claim_amount > 0 then reimbursement_amount / claim_amount
            else 0
        end as payment_rate,

        case
            when reimbursement_amount = 0 and claim_amount > 0 then true
            else false
        end as is_denied,

        case
            when reimbursement_amount > 0 and reimbursement_amount < claim_amount then true
            else false
        end as is_partial_payment,

        -- Service metrics
        service_days,
        length_of_stay,
        processing_days,

        -- Processing time categories
        case
            when processing_days <= 7 then 'Fast (≤7 days)'
            when processing_days <= 14 then 'Normal (8-14 days)'
            when processing_days <= 30 then 'Slow (15-30 days)'
            when processing_days > 30 then 'Very Slow (>30 days)'
            else 'Unknown'
        end as processing_speed_category,

        -- Claim amount categories
        case
            when claim_amount < 100 then 'Very Low (<$100)'
            when claim_amount < 500 then 'Low ($100-$499)'
            when claim_amount < 1000 then 'Medium ($500-$999)'
            when claim_amount < 5000 then 'High ($1K-$4.9K)'
            when claim_amount < 25000 then 'Very High ($5K-$24.9K)'
            else 'Extremely High (≥$25K)'
        end as claim_amount_category,

        -- Clinical information
        diagnosis_code_1 as primary_diagnosis_code,
        diagnosis_code_2 as secondary_diagnosis_code,
        diagnosis_code_3 as tertiary_diagnosis_code,
        procedure_code_1 as primary_procedure_code,
        procedure_code_2 as secondary_procedure_code,
        procedure_code_3 as tertiary_procedure_code,

        -- Data quality flags
        beneficiary_missing,
        provider_missing,
        negative_amount,
        diagnosis_missing,

        -- Calculated flags for analytics
        case when claim_amount > 10000 then true else false end as is_high_dollar,
        case when length_of_stay > 7 then true else false end as is_long_stay,
        case when processing_days > 30 then true else false end as is_slow_processing,

        -- Year-Month for partitioning/analysis
        extract(year from claim_start_date) as claim_year,
        extract(month from claim_start_date) as claim_month,
        extract(quarter from claim_start_date) as claim_quarter,
        date_trunc('month', claim_start_date) as claim_month_year,

        -- Metadata
        loaded_at as source_loaded_at,
        current_timestamp as fact_loaded_at

    from claims_with_keys
    where not beneficiary_missing
      and not provider_missing
      and not negative_amount
)

select * from final