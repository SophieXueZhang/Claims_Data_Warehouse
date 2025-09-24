{{ config(
    materialized='table',
    indexes=[
        {'columns': ['provider_key']},
        {'columns': ['specialty_description']},
        {'columns': ['state_code']},
        {'columns': ['performance_tier']},
        {'columns': ['total_claims']}
    ],
    tags=['analytics', 'metrics', 'providers']
) }}

with provider_claims as (
    select
        f.provider_key,
        p.provider_name,
        p.provider_type,
        p.specialty_description,
        p.state_code,
        p.participates_in_medicare,

        -- Volume metrics
        count(*) as total_claims,
        count(distinct f.beneficiary_key) as unique_patients,
        count(distinct date_trunc('month', f.claim_start_date)) as active_months,

        -- Financial metrics
        sum(f.claim_amount) as total_claim_amount,
        sum(f.reimbursement_amount) as total_reimbursement,
        avg(f.claim_amount) as avg_claim_amount,
        avg(f.reimbursement_amount) as avg_reimbursement,
        percentile_cont(0.5) within group (order by f.claim_amount) as median_claim_amount,

        -- Efficiency metrics
        avg(f.processing_days) as avg_processing_days,
        percentile_cont(0.5) within group (order by f.processing_days) as median_processing_days,
        avg(f.service_days) as avg_service_days,

        -- Quality metrics
        count(case when f.is_denied then 1 end) as denied_claims,
        count(case when f.is_denied then 1 end)::decimal / count(*) as denial_rate,
        count(case when f.is_partial_payment then 1 end) as partial_payment_claims,
        count(case when f.is_partial_payment then 1 end)::decimal / count(*) as partial_payment_rate,

        -- Utilization patterns
        count(case when f.claim_type = 'Inpatient' then 1 end) as inpatient_claims,
        count(case when f.claim_type = 'Outpatient' then 1 end) as outpatient_claims,
        count(case when f.claim_type = 'Carrier' then 1 end) as carrier_claims,

        -- High-risk indicators
        count(case when f.is_high_dollar then 1 end) as high_dollar_claims,
        count(case when f.is_high_dollar then 1 end)::decimal / count(*) as high_dollar_rate,
        count(case when f.is_slow_processing then 1 end) as slow_processing_claims,
        count(case when f.is_slow_processing then 1 end)::decimal / count(*) as slow_processing_rate,

        -- Length of stay for inpatient providers
        avg(case when f.length_of_stay > 0 then f.length_of_stay end) as avg_length_of_stay,

        -- Date ranges
        min(f.claim_start_date) as first_claim_date,
        max(f.claim_start_date) as last_claim_date

    from {{ ref('fact_claims') }} f
    inner join {{ ref('dim_providers') }} p
        on f.provider_key = p.provider_key
    group by f.provider_key, p.provider_name, p.provider_type, p.specialty_description, p.state_code, p.participates_in_medicare
),

provider_rankings as (
    select
        *,
        -- Percentile rankings for benchmarking
        percent_rank() over (order by total_claims) as volume_percentile,
        percent_rank() over (order by avg_claim_amount) as avg_amount_percentile,
        percent_rank() over (order by denial_rate) as denial_rate_percentile,
        percent_rank() over (order by avg_processing_days) as processing_speed_percentile,

        -- Specialty rankings
        percent_rank() over (partition by specialty_description order by total_claims) as specialty_volume_rank,
        percent_rank() over (partition by specialty_description order by avg_claim_amount) as specialty_amount_rank,
        percent_rank() over (partition by specialty_description order by denial_rate) as specialty_denial_rank,

        -- State rankings
        percent_rank() over (partition by state_code order by total_claims) as state_volume_rank,
        percent_rank() over (partition by state_code order by avg_claim_amount) as state_amount_rank

    from provider_claims
),

final as (
    select
        provider_key,
        provider_name,
        provider_type,
        specialty_description,
        state_code,
        participates_in_medicare,

        -- Volume metrics
        total_claims,
        unique_patients,
        active_months,
        round(total_claims::decimal / active_months, 1) as avg_claims_per_month,
        round(unique_patients::decimal / nullif(total_claims, 0), 4) as patients_per_claim,

        -- Financial metrics
        round(total_claim_amount, 2) as total_claim_amount,
        round(total_reimbursement, 2) as total_reimbursement,
        round(avg_claim_amount, 2) as avg_claim_amount,
        round(avg_reimbursement, 2) as avg_reimbursement,
        round(median_claim_amount, 2) as median_claim_amount,
        round(total_reimbursement / nullif(total_claim_amount, 0), 4) as overall_reimbursement_rate,

        -- Efficiency metrics
        round(avg_processing_days, 1) as avg_processing_days,
        round(median_processing_days, 1) as median_processing_days,
        round(avg_service_days, 1) as avg_service_days,
        round(avg_length_of_stay, 1) as avg_length_of_stay,

        -- Quality metrics
        denied_claims,
        round(denial_rate, 4) as denial_rate,
        partial_payment_claims,
        round(partial_payment_rate, 4) as partial_payment_rate,

        -- Claim mix
        inpatient_claims,
        outpatient_claims,
        carrier_claims,
        round(inpatient_claims::decimal / nullif(total_claims, 0), 4) as inpatient_mix,
        round(outpatient_claims::decimal / nullif(total_claims, 0), 4) as outpatient_mix,
        round(carrier_claims::decimal / nullif(total_claims, 0), 4) as carrier_mix,

        -- Risk indicators
        high_dollar_claims,
        round(high_dollar_rate, 4) as high_dollar_rate,
        slow_processing_claims,
        round(slow_processing_rate, 4) as slow_processing_rate,

        -- Performance classification
        case
            when volume_percentile >= 0.9 and denial_rate <= 0.05 then 'Top Performer'
            when volume_percentile >= 0.7 and denial_rate <= 0.10 then 'High Performer'
            when volume_percentile >= 0.3 and denial_rate <= 0.15 then 'Average Performer'
            when denial_rate > 0.25 or slow_processing_rate > 0.20 then 'Needs Improvement'
            else 'Low Volume'
        end as performance_tier,

        -- Risk classification
        case
            when denial_rate > 0.25 then 'High Risk - High Denials'
            when high_dollar_rate > 0.20 then 'High Risk - High Costs'
            when slow_processing_rate > 0.30 then 'High Risk - Slow Processing'
            when avg_claim_amount > 50000 then 'High Risk - High Average Cost'
            else 'Normal Risk'
        end as risk_category,

        -- Benchmarking percentiles
        round(volume_percentile, 4) as volume_percentile,
        round(avg_amount_percentile, 4) as avg_amount_percentile,
        round(denial_rate_percentile, 4) as denial_rate_percentile,
        round(processing_speed_percentile, 4) as processing_speed_percentile,

        -- Specialty benchmarking
        round(specialty_volume_rank, 4) as specialty_volume_rank,
        round(specialty_amount_rank, 4) as specialty_amount_rank,
        round(specialty_denial_rank, 4) as specialty_denial_rank,

        -- Activity dates
        first_claim_date,
        last_claim_date,
        current_date - last_claim_date as days_since_last_claim,

        -- Flags
        case when last_claim_date >= current_date - interval '90 days' then true else false end as is_recently_active,
        case when total_claims >= 100 then true else false end as is_high_volume,
        case when denial_rate <= 0.05 then true else false end as is_low_denial,
        case when avg_processing_days <= 7 then true else false end as is_fast_processor,

        current_timestamp as metrics_calculated_at

    from provider_rankings
)

select * from final
order by total_claims desc