{{ config(
    materialized='table',
    indexes=[
        {'columns': ['metric_date']},
        {'columns': ['metric_period']},
        {'columns': ['claim_type']},
        {'columns': ['metric_date', 'metric_period']}
    ],
    tags=['analytics', 'metrics', 'claims']
) }}

with daily_metrics as (
    select
        claim_start_date as metric_date,
        'daily' as metric_period,
        claim_type,

        -- Volume metrics
        count(*) as total_claims,
        count(distinct beneficiary_key) as unique_beneficiaries,
        count(distinct provider_key) as unique_providers,

        -- Financial metrics
        sum(claim_amount) as total_claim_amount,
        sum(reimbursement_amount) as total_reimbursement,
        avg(claim_amount) as avg_claim_amount,
        avg(reimbursement_amount) as avg_reimbursement,
        percentile_cont(0.5) within group (order by claim_amount) as median_claim_amount,

        -- Denial metrics
        count(case when is_denied then 1 end) as denied_claims,
        count(case when is_denied then 1 end)::decimal / count(*) as denial_rate,

        -- Processing metrics
        avg(processing_days) as avg_processing_days,
        percentile_cont(0.5) within group (order by processing_days) as median_processing_days,
        avg(case when processing_days <= 14 then processing_days end) as avg_processing_days_fast,

        -- Service utilization
        avg(service_days) as avg_service_days,
        avg(case when length_of_stay > 0 then length_of_stay end) as avg_length_of_stay,

        -- Quality indicators
        count(case when is_high_dollar then 1 end) as high_dollar_claims,
        count(case when is_high_dollar then 1 end)::decimal / count(*) as high_dollar_rate,
        count(case when is_slow_processing then 1 end) as slow_processing_claims,
        count(case when is_slow_processing then 1 end)::decimal / count(*) as slow_processing_rate

    from {{ ref('fact_claims') }}
    group by claim_start_date, claim_type

    union all

    select
        claim_start_date as metric_date,
        'daily' as metric_period,
        'All Types' as claim_type,

        -- Volume metrics
        count(*) as total_claims,
        count(distinct beneficiary_key) as unique_beneficiaries,
        count(distinct provider_key) as unique_providers,

        -- Financial metrics
        sum(claim_amount) as total_claim_amount,
        sum(reimbursement_amount) as total_reimbursement,
        avg(claim_amount) as avg_claim_amount,
        avg(reimbursement_amount) as avg_reimbursement,
        percentile_cont(0.5) within group (order by claim_amount) as median_claim_amount,

        -- Denial metrics
        count(case when is_denied then 1 end) as denied_claims,
        count(case when is_denied then 1 end)::decimal / count(*) as denial_rate,

        -- Processing metrics
        avg(processing_days) as avg_processing_days,
        percentile_cont(0.5) within group (order by processing_days) as median_processing_days,
        avg(case when processing_days <= 14 then processing_days end) as avg_processing_days_fast,

        -- Service utilization
        avg(service_days) as avg_service_days,
        avg(case when length_of_stay > 0 then length_of_stay end) as avg_length_of_stay,

        -- Quality indicators
        count(case when is_high_dollar then 1 end) as high_dollar_claims,
        count(case when is_high_dollar then 1 end)::decimal / count(*) as high_dollar_rate,
        count(case when is_slow_processing then 1 end) as slow_processing_claims,
        count(case when is_slow_processing then 1 end)::decimal / count(*) as slow_processing_rate

    from {{ ref('fact_claims') }}
    group by claim_start_date
),

weekly_metrics as (
    select
        date_trunc('week', claim_start_date)::date as metric_date,
        'weekly' as metric_period,
        claim_type,

        count(*) as total_claims,
        count(distinct beneficiary_key) as unique_beneficiaries,
        count(distinct provider_key) as unique_providers,
        sum(claim_amount) as total_claim_amount,
        sum(reimbursement_amount) as total_reimbursement,
        avg(claim_amount) as avg_claim_amount,
        avg(reimbursement_amount) as avg_reimbursement,
        percentile_cont(0.5) within group (order by claim_amount) as median_claim_amount,
        count(case when is_denied then 1 end) as denied_claims,
        count(case when is_denied then 1 end)::decimal / count(*) as denial_rate,
        avg(processing_days) as avg_processing_days,
        percentile_cont(0.5) within group (order by processing_days) as median_processing_days,
        avg(case when processing_days <= 14 then processing_days end) as avg_processing_days_fast,
        avg(service_days) as avg_service_days,
        avg(case when length_of_stay > 0 then length_of_stay end) as avg_length_of_stay,
        count(case when is_high_dollar then 1 end) as high_dollar_claims,
        count(case when is_high_dollar then 1 end)::decimal / count(*) as high_dollar_rate,
        count(case when is_slow_processing then 1 end) as slow_processing_claims,
        count(case when is_slow_processing then 1 end)::decimal / count(*) as slow_processing_rate

    from {{ ref('fact_claims') }}
    group by date_trunc('week', claim_start_date), claim_type

    union all

    select
        date_trunc('week', claim_start_date)::date as metric_date,
        'weekly' as metric_period,
        'All Types' as claim_type,

        count(*) as total_claims,
        count(distinct beneficiary_key) as unique_beneficiaries,
        count(distinct provider_key) as unique_providers,
        sum(claim_amount) as total_claim_amount,
        sum(reimbursement_amount) as total_reimbursement,
        avg(claim_amount) as avg_claim_amount,
        avg(reimbursement_amount) as avg_reimbursement,
        percentile_cont(0.5) within group (order by claim_amount) as median_claim_amount,
        count(case when is_denied then 1 end) as denied_claims,
        count(case when is_denied then 1 end)::decimal / count(*) as denial_rate,
        avg(processing_days) as avg_processing_days,
        percentile_cont(0.5) within group (order by processing_days) as median_processing_days,
        avg(case when processing_days <= 14 then processing_days end) as avg_processing_days_fast,
        avg(service_days) as avg_service_days,
        avg(case when length_of_stay > 0 then length_of_stay end) as avg_length_of_stay,
        count(case when is_high_dollar then 1 end) as high_dollar_claims,
        count(case when is_high_dollar then 1 end)::decimal / count(*) as high_dollar_rate,
        count(case when is_slow_processing then 1 end) as slow_processing_claims,
        count(case when is_slow_processing then 1 end)::decimal / count(*) as slow_processing_rate

    from {{ ref('fact_claims') }}
    group by date_trunc('week', claim_start_date)
),

monthly_metrics as (
    select
        date_trunc('month', claim_start_date)::date as metric_date,
        'monthly' as metric_period,
        claim_type,

        count(*) as total_claims,
        count(distinct beneficiary_key) as unique_beneficiaries,
        count(distinct provider_key) as unique_providers,
        sum(claim_amount) as total_claim_amount,
        sum(reimbursement_amount) as total_reimbursement,
        avg(claim_amount) as avg_claim_amount,
        avg(reimbursement_amount) as avg_reimbursement,
        percentile_cont(0.5) within group (order by claim_amount) as median_claim_amount,
        count(case when is_denied then 1 end) as denied_claims,
        count(case when is_denied then 1 end)::decimal / count(*) as denial_rate,
        avg(processing_days) as avg_processing_days,
        percentile_cont(0.5) within group (order by processing_days) as median_processing_days,
        avg(case when processing_days <= 14 then processing_days end) as avg_processing_days_fast,
        avg(service_days) as avg_service_days,
        avg(case when length_of_stay > 0 then length_of_stay end) as avg_length_of_stay,
        count(case when is_high_dollar then 1 end) as high_dollar_claims,
        count(case when is_high_dollar then 1 end)::decimal / count(*) as high_dollar_rate,
        count(case when is_slow_processing then 1 end) as slow_processing_claims,
        count(case when is_slow_processing then 1 end)::decimal / count(*) as slow_processing_rate

    from {{ ref('fact_claims') }}
    group by date_trunc('month', claim_start_date), claim_type

    union all

    select
        date_trunc('month', claim_start_date)::date as metric_date,
        'monthly' as metric_period,
        'All Types' as claim_type,

        count(*) as total_claims,
        count(distinct beneficiary_key) as unique_beneficiaries,
        count(distinct provider_key) as unique_providers,
        sum(claim_amount) as total_claim_amount,
        sum(reimbursement_amount) as total_reimbursement,
        avg(claim_amount) as avg_claim_amount,
        avg(reimbursement_amount) as avg_reimbursement,
        percentile_cont(0.5) within group (order by claim_amount) as median_claim_amount,
        count(case when is_denied then 1 end) as denied_claims,
        count(case when is_denied then 1 end)::decimal / count(*) as denial_rate,
        avg(processing_days) as avg_processing_days,
        percentile_cont(0.5) within group (order by processing_days) as median_processing_days,
        avg(case when processing_days <= 14 then processing_days end) as avg_processing_days_fast,
        avg(service_days) as avg_service_days,
        avg(case when length_of_stay > 0 then length_of_stay end) as avg_length_of_stay,
        count(case when is_high_dollar then 1 end) as high_dollar_claims,
        count(case when is_high_dollar then 1 end)::decimal / count(*) as high_dollar_rate,
        count(case when is_slow_processing then 1 end) as slow_processing_claims,
        count(case when is_slow_processing then 1 end)::decimal / count(*) as slow_processing_rate

    from {{ ref('fact_claims') }}
    group by date_trunc('month', claim_start_date)
),

final as (
    select * from daily_metrics
    union all
    select * from weekly_metrics
    union all
    select * from monthly_metrics
)

select
    metric_date,
    metric_period,
    claim_type,
    total_claims,
    unique_beneficiaries,
    unique_providers,
    total_claim_amount,
    total_reimbursement,
    round(avg_claim_amount, 2) as avg_claim_amount,
    round(avg_reimbursement, 2) as avg_reimbursement,
    round(median_claim_amount, 2) as median_claim_amount,
    denied_claims,
    round(denial_rate, 4) as denial_rate,
    round(avg_processing_days, 1) as avg_processing_days,
    round(median_processing_days, 1) as median_processing_days,
    round(avg_processing_days_fast, 1) as avg_processing_days_fast,
    round(avg_service_days, 1) as avg_service_days,
    round(avg_length_of_stay, 1) as avg_length_of_stay,
    high_dollar_claims,
    round(high_dollar_rate, 4) as high_dollar_rate,
    slow_processing_claims,
    round(slow_processing_rate, 4) as slow_processing_rate,
    current_timestamp as metrics_calculated_at

from final
order by metric_date desc, metric_period, claim_type