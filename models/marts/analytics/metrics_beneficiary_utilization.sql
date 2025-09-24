{{ config(
    materialized='table',
    indexes=[
        {'columns': ['beneficiary_key']},
        {'columns': ['age_group']},
        {'columns': ['gender']},
        {'columns': ['state_code']},
        {'columns': ['risk_tier']},
        {'columns': ['total_cost']}
    ],
    tags=['analytics', 'metrics', 'beneficiaries']
) }}

with beneficiary_claims as (
    select
        f.beneficiary_key,
        b.beneficiary_id,
        b.gender,
        b.age_group,
        b.race_description,
        b.state_code,
        b.chronic_condition_count,
        b.condition_burden_category,
        b.risk_score as demographic_risk_score,
        b.is_deceased,

        -- Utilization metrics
        count(*) as total_claims,
        count(distinct f.provider_key) as unique_providers,
        count(distinct date_trunc('month', f.claim_start_date)) as active_months,

        -- Financial metrics
        sum(f.claim_amount) as total_cost,
        sum(f.reimbursement_amount) as total_medicare_paid,
        sum(f.patient_responsibility) as total_patient_responsibility,
        avg(f.claim_amount) as avg_claim_amount,
        percentile_cont(0.5) within group (order by f.claim_amount) as median_claim_amount,
        max(f.claim_amount) as max_claim_amount,

        -- Service utilization
        count(case when f.claim_type = 'Inpatient' then 1 end) as inpatient_claims,
        count(case when f.claim_type = 'Outpatient' then 1 end) as outpatient_claims,
        count(case when f.claim_type = 'Carrier' then 1 end) as carrier_claims,
        sum(case when f.claim_type = 'Inpatient' then f.length_of_stay else 0 end) as total_inpatient_days,
        avg(case when f.claim_type = 'Inpatient' and f.length_of_stay > 0 then f.length_of_stay end) as avg_length_of_stay,

        -- Quality and access metrics
        count(case when f.is_denied then 1 end) as denied_claims,
        count(case when f.is_denied then 1 end)::decimal / count(*) as personal_denial_rate,
        avg(f.processing_days) as avg_processing_days,

        -- High-cost indicators
        count(case when f.is_high_dollar then 1 end) as high_dollar_claims,
        count(case when f.is_high_dollar then 1 end)::decimal / count(*) as high_dollar_rate,

        -- Emergency indicators
        count(case when f.claim_type = 'Inpatient' and f.length_of_stay = 1 then 1 end) as potential_ed_visits,
        count(case when f.claim_type = 'Inpatient' and f.length_of_stay >= 14 then 1 end) as long_stay_admissions,

        -- Date ranges
        min(f.claim_start_date) as first_claim_date,
        max(f.claim_start_date) as last_claim_date

    from {{ ref('fact_claims') }} f
    inner join {{ ref('dim_beneficiaries') }} b
        on f.beneficiary_key = b.beneficiary_key
    group by f.beneficiary_key, b.beneficiary_id, b.gender, b.age_group, b.race_description,
             b.state_code, b.chronic_condition_count, b.condition_burden_category,
             b.risk_score, b.is_deceased
),

utilization_rankings as (
    select
        *,
        -- Overall percentile rankings
        percent_rank() over (order by total_claims) as utilization_percentile,
        percent_rank() over (order by total_cost) as cost_percentile,
        percent_rank() over (order by unique_providers) as provider_diversity_percentile,

        -- Age group benchmarking
        percent_rank() over (partition by age_group order by total_claims) as age_utilization_rank,
        percent_rank() over (partition by age_group order by total_cost) as age_cost_rank,

        -- Gender benchmarking
        percent_rank() over (partition by gender order by total_claims) as gender_utilization_rank,
        percent_rank() over (partition by gender order by total_cost) as gender_cost_rank,

        -- Condition burden benchmarking
        percent_rank() over (partition by condition_burden_category order by total_cost) as condition_cost_rank

    from beneficiary_claims
),

final as (
    select
        beneficiary_key,
        beneficiary_id,
        gender,
        age_group,
        race_description,
        state_code,
        chronic_condition_count,
        condition_burden_category,
        is_deceased,

        -- Utilization metrics
        total_claims,
        unique_providers,
        active_months,
        round(total_claims::decimal / nullif(active_months, 0), 1) as avg_claims_per_month,
        round(unique_providers::decimal / nullif(total_claims, 0), 4) as provider_diversity_ratio,

        -- Financial metrics
        round(total_cost, 2) as total_cost,
        round(total_medicare_paid, 2) as total_medicare_paid,
        round(total_patient_responsibility, 2) as total_patient_responsibility,
        round(avg_claim_amount, 2) as avg_claim_amount,
        round(median_claim_amount, 2) as median_claim_amount,
        round(max_claim_amount, 2) as max_claim_amount,
        round(total_medicare_paid / nullif(total_cost, 0), 4) as medicare_coverage_rate,

        -- Service utilization
        inpatient_claims,
        outpatient_claims,
        carrier_claims,
        total_inpatient_days,
        round(avg_length_of_stay, 1) as avg_length_of_stay,

        -- Service mix percentages
        round(inpatient_claims::decimal / nullif(total_claims, 0), 4) as inpatient_utilization_rate,
        round(outpatient_claims::decimal / nullif(total_claims, 0), 4) as outpatient_utilization_rate,
        round(carrier_claims::decimal / nullif(total_claims, 0), 4) as carrier_utilization_rate,

        -- Quality metrics
        denied_claims,
        round(personal_denial_rate, 4) as personal_denial_rate,
        round(avg_processing_days, 1) as avg_processing_days,

        -- Risk indicators
        high_dollar_claims,
        round(high_dollar_rate, 4) as high_dollar_rate,
        potential_ed_visits,
        long_stay_admissions,

        -- Risk scoring (enhanced with utilization patterns)
        round((
            demographic_risk_score +
            -- High utilization bonus
            case when utilization_percentile >= 0.95 then 2.0
                 when utilization_percentile >= 0.90 then 1.5
                 when utilization_percentile >= 0.75 then 1.0
                 else 0 end +
            -- High cost bonus
            case when cost_percentile >= 0.95 then 1.5
                 when cost_percentile >= 0.90 then 1.0
                 else 0 end +
            -- Emergency indicators
            case when potential_ed_visits >= 6 then 1.0 else 0 end +
            case when long_stay_admissions >= 2 then 1.5 else 0 end
        ), 2) as utilization_adjusted_risk_score,

        -- Classification tiers
        case
            when total_cost >= 100000 then 'Very High Cost'
            when total_cost >= 50000 then 'High Cost'
            when total_cost >= 10000 then 'Medium Cost'
            when total_cost > 0 then 'Low Cost'
            else 'No Cost'
        end as cost_tier,

        case
            when total_claims >= 50 then 'Very High Utilizer'
            when total_claims >= 20 then 'High Utilizer'
            when total_claims >= 5 then 'Medium Utilizer'
            when total_claims > 0 then 'Low Utilizer'
            else 'No Utilization'
        end as utilization_tier,

        case
            when cost_percentile >= 0.95 and utilization_percentile >= 0.90 then 'High Risk'
            when cost_percentile >= 0.80 or utilization_percentile >= 0.80 then 'Medium Risk'
            when total_claims > 0 then 'Low Risk'
            else 'No Risk'
        end as risk_tier,

        -- Care management flags
        case when cost_percentile >= 0.95 then true else false end as needs_case_management,
        case when inpatient_claims >= 3 then true else false end as frequent_admissions,
        case when potential_ed_visits >= 6 then true else false end as frequent_ed_user,
        case when unique_providers >= 10 then true else false end as multiple_providers,
        case when personal_denial_rate > 0.15 then true else false end as high_denial_rate,

        -- Benchmarking percentiles
        round(utilization_percentile, 4) as utilization_percentile,
        round(cost_percentile, 4) as cost_percentile,
        round(provider_diversity_percentile, 4) as provider_diversity_percentile,

        -- Age/gender benchmarking
        round(age_utilization_rank, 4) as age_utilization_rank,
        round(age_cost_rank, 4) as age_cost_rank,
        round(gender_utilization_rank, 4) as gender_utilization_rank,
        round(gender_cost_rank, 4) as gender_cost_rank,
        round(condition_cost_rank, 4) as condition_cost_rank,

        -- Activity dates
        first_claim_date,
        last_claim_date,
        current_date - last_claim_date as days_since_last_claim,

        -- Activity flags
        case when last_claim_date >= current_date - interval '90 days' then true else false end as is_recently_active,

        current_timestamp as metrics_calculated_at

    from utilization_rankings
)

select * from final
order by total_cost desc