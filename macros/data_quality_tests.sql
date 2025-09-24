{% macro test_claim_amount_consistency() %}
    /*
    Test that ensures claim amounts are consistent with business rules:
    1. Reimbursement amount should not exceed claim amount
    2. Patient responsibility should equal claim amount minus reimbursement (when not null)
    3. Deductible amount should not exceed claim amount
    */
    select
        claim_id,
        claim_amount,
        reimbursement_amount,
        patient_responsibility,
        deductible_amount,
        'Reimbursement exceeds claim amount' as error_type
    from {{ ref('fact_claims') }}
    where reimbursement_amount > claim_amount

    union all

    select
        claim_id,
        claim_amount,
        reimbursement_amount,
        patient_responsibility,
        deductible_amount,
        'Patient responsibility calculation error' as error_type
    from {{ ref('fact_claims') }}
    where abs(patient_responsibility - (claim_amount - reimbursement_amount)) > 0.01
      and patient_responsibility is not null

    union all

    select
        claim_id,
        claim_amount,
        reimbursement_amount,
        patient_responsibility,
        deductible_amount,
        'Deductible exceeds claim amount' as error_type
    from {{ ref('fact_claims') }}
    where deductible_amount > claim_amount
      and deductible_amount is not null

{% endmacro %}

{% macro test_date_consistency() %}
    /*
    Test that ensures date fields are logically consistent:
    1. Claim end date should be >= claim start date
    2. Discharge date should be >= admission date
    3. Processed date should be >= created date
    */
    select
        claim_id,
        claim_start_date,
        claim_end_date,
        admission_date,
        discharge_date,
        created_at,
        processed_at,
        'Claim end date before start date' as error_type
    from {{ ref('fact_claims') }}
    where claim_end_date < claim_start_date

    union all

    select
        claim_id,
        claim_start_date,
        claim_end_date,
        admission_date,
        discharge_date,
        created_at,
        processed_at,
        'Discharge before admission' as error_type
    from {{ ref('fact_claims') }}
    where discharge_date < admission_date
      and admission_date is not null
      and discharge_date is not null

    union all

    select
        claim_id,
        claim_start_date,
        claim_end_date,
        admission_date,
        discharge_date,
        created_at,
        processed_at,
        'Processed before created' as error_type
    from {{ ref('fact_claims') }}
    where processed_at < created_at

{% endmacro %}

{% macro test_referential_integrity_orphaned_claims() %}
    /*
    Test for orphaned claims that reference non-existent providers or beneficiaries
    */
    select
        'orphaned_provider' as error_type,
        count(*) as error_count
    from {{ ref('stg_cms_claims') }} c
    left join {{ ref('stg_cms_providers') }} p
        on c.provider_id = p.provider_id
    where p.provider_id is null
    having count(*) > 0

    union all

    select
        'orphaned_beneficiary' as error_type,
        count(*) as error_count
    from {{ ref('stg_cms_claims') }} c
    left join {{ ref('stg_cms_beneficiaries') }} b
        on c.beneficiary_id = b.beneficiary_id
    where b.beneficiary_id is null
    having count(*) > 0

{% endmacro %}

{% macro test_business_rule_violations() %}
    /*
    Test for business rule violations specific to healthcare claims:
    1. Inpatient claims should have admission/discharge dates
    2. Length of stay should be reasonable (< 365 days)
    3. Claims should not be processed before service date
    4. Service days should be reasonable
    */
    select
        claim_id,
        claim_type,
        length_of_stay,
        service_days,
        processing_days,
        'Inpatient claim missing admission date' as error_type
    from {{ ref('fact_claims') }}
    where claim_type = 'Inpatient'
      and admission_date is null

    union all

    select
        claim_id,
        claim_type,
        length_of_stay,
        service_days,
        processing_days,
        'Unreasonable length of stay' as error_type
    from {{ ref('fact_claims') }}
    where length_of_stay > 365
      and length_of_stay is not null

    union all

    select
        claim_id,
        claim_type,
        length_of_stay,
        service_days,
        processing_days,
        'Claim processed before service date' as error_type
    from {{ ref('fact_claims') }}
    where processed_at < claim_start_date

    union all

    select
        claim_id,
        claim_type,
        length_of_stay,
        service_days,
        processing_days,
        'Unreasonable service days' as error_type
    from {{ ref('fact_claims') }}
    where service_days > 365
      or service_days < 0

{% endmacro %}

{% macro test_data_freshness_anomalies() %}
    /*
    Test for data freshness and volume anomalies that could indicate data pipeline issues
    */
    with daily_counts as (
        select
            claim_start_date,
            count(*) as daily_claim_count,
            sum(claim_amount) as daily_claim_amount
        from {{ ref('fact_claims') }}
        group by claim_start_date
    ),
    daily_stats as (
        select
            avg(daily_claim_count) as avg_daily_claims,
            stddev(daily_claim_count) as stddev_daily_claims,
            avg(daily_claim_amount) as avg_daily_amount,
            stddev(daily_claim_amount) as stddev_daily_amount
        from daily_counts
    )
    select
        dc.claim_start_date,
        dc.daily_claim_count,
        dc.daily_claim_amount,
        ds.avg_daily_claims,
        'Volume anomaly - too low' as error_type
    from daily_counts dc
    cross join daily_stats ds
    where dc.daily_claim_count < (ds.avg_daily_claims - 2 * ds.stddev_daily_claims)
      and ds.stddev_daily_claims is not null

    union all

    select
        dc.claim_start_date,
        dc.daily_claim_count,
        dc.daily_claim_amount,
        ds.avg_daily_claims,
        'Volume anomaly - too high' as error_type
    from daily_counts dc
    cross join daily_stats ds
    where dc.daily_claim_count > (ds.avg_daily_claims + 2 * ds.stddev_daily_claims)
      and ds.stddev_daily_claims is not null

{% endmacro %}

{% macro generate_data_quality_report() %}
    /*
    Generate a comprehensive data quality report
    */
    select
        'Staging Layer' as layer,
        'stg_cms_claims' as model_name,
        count(*) as total_records,
        count(case when beneficiary_missing then 1 end) as beneficiary_missing_count,
        count(case when provider_missing then 1 end) as provider_missing_count,
        count(case when negative_amount then 1 end) as negative_amount_count,
        count(case when diagnosis_missing then 1 end) as diagnosis_missing_count
    from {{ ref('stg_cms_claims') }}

    union all

    select
        'Mart Layer' as layer,
        'fact_claims' as model_name,
        count(*) as total_records,
        count(case when is_high_dollar then 1 end) as high_dollar_count,
        count(case when is_denied then 1 end) as denied_count,
        count(case when is_slow_processing then 1 end) as slow_processing_count,
        count(case when processing_days > 90 then 1 end) as very_slow_processing_count
    from {{ ref('fact_claims') }}

{% endmacro %}