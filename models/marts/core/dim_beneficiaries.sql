{{ config(
    materialized='table',
    indexes=[
        {'columns': ['beneficiary_id'], 'unique': true},
        {'columns': ['state_code']},
        {'columns': ['age_group']},
        {'columns': ['gender']},
        {'columns': ['chronic_condition_count']}
    ],
    tags=['dimension', 'core', 'beneficiaries']
) }}

with beneficiary_claims as (
    select
        beneficiary_id,
        count(*) as total_claims,
        sum(claim_amount) as total_claim_amount,
        sum(reimbursement_amount) as total_reimbursement,
        avg(claim_amount) as avg_claim_amount,
        min(claim_start_date) as first_claim_date,
        max(claim_start_date) as last_claim_date,
        count(distinct provider_id) as unique_providers,
        count(distinct case when claim_type = 'Inpatient' then claim_id end) as inpatient_claims,
        count(distinct case when claim_type = 'Outpatient' then claim_id end) as outpatient_claims,
        count(distinct case when claim_type = 'Carrier' then claim_id end) as carrier_claims,
        count(distinct case when claim_status = 'Denied' then claim_id end) as denied_claims
    from {{ ref('stg_cms_claims') }}
    group by beneficiary_id
),

final as (
    select
        -- Surrogate key
        b.beneficiary_key,

        -- Business key
        b.beneficiary_id,

        -- Demographics
        b.date_of_birth,
        b.date_of_death,
        b.gender,
        b.race_description,
        b.race_code,
        b.current_age,
        b.is_deceased,

        -- Age grouping for analytics
        case
            when b.current_age < 65 then 'Under 65'
            when b.current_age between 65 and 74 then '65-74'
            when b.current_age between 75 and 84 then '75-84'
            when b.current_age >= 85 then '85+'
            else 'Unknown'
        end as age_group,

        -- Geographic information
        b.state_code,
        b.county_code,

        -- Enrollment information
        b.enrollment_start_date,
        b.enrollment_end_date,
        b.hi_coverage_months,
        b.smi_coverage_months,
        b.hmo_coverage_months,
        b.plan_coverage_months,

        -- Chronic conditions
        b.has_alzheimer,
        b.has_heart_failure,
        b.has_chronic_kidney,
        b.has_cancer,
        b.has_copd,
        b.has_depression,
        b.has_diabetes,
        b.has_ischemic_heart,
        b.has_osteoporosis,
        b.has_arthritis,
        b.has_stroke,
        b.chronic_condition_count,

        -- Condition categories
        case
            when b.chronic_condition_count = 0 then 'No Conditions'
            when b.chronic_condition_count between 1 and 2 then 'Low Burden'
            when b.chronic_condition_count between 3 and 5 then 'Moderate Burden'
            when b.chronic_condition_count > 5 then 'High Burden'
        end as condition_burden_category,

        -- Risk scoring based on age, conditions, and claims history
        round((
            -- Base age risk
            case
                when b.current_age < 65 then 1.0
                when b.current_age between 65 and 74 then 2.0
                when b.current_age between 75 and 84 then 3.5
                when b.current_age >= 85 then 5.0
                else 1.0
            end +
            -- Chronic condition multiplier
            (b.chronic_condition_count * 0.3) +
            -- High-risk condition bonus
            case when b.has_cancer then 1.5 else 0 end +
            case when b.has_heart_failure then 1.2 else 0 end +
            case when b.has_chronic_kidney then 1.0 else 0 end +
            -- Claims utilization factor
            case
                when c.total_claims > 50 then 1.0
                when c.total_claims > 20 then 0.5
                else 0
            end
        ), 2) as risk_score,

        -- Claims statistics
        coalesce(c.total_claims, 0) as total_claims,
        coalesce(c.total_claim_amount, 0) as total_claim_amount,
        coalesce(c.total_reimbursement, 0) as total_reimbursement,
        coalesce(c.avg_claim_amount, 0) as avg_claim_amount,
        coalesce(c.unique_providers, 0) as unique_providers,
        coalesce(c.inpatient_claims, 0) as inpatient_claims,
        coalesce(c.outpatient_claims, 0) as outpatient_claims,
        coalesce(c.carrier_claims, 0) as carrier_claims,
        coalesce(c.denied_claims, 0) as denied_claims,

        -- Utilization metrics
        case
            when c.total_claims >= 20 then 'High Utilizer'
            when c.total_claims >= 5 then 'Medium Utilizer'
            when c.total_claims > 0 then 'Low Utilizer'
            else 'No Claims'
        end as utilization_tier,

        case
            when c.total_claims > 0 then
                round(c.denied_claims::decimal / c.total_claims, 4)
            else 0
        end as denial_rate,

        c.first_claim_date,
        c.last_claim_date,

        -- Activity flags
        case when c.last_claim_date >= current_date - interval '90 days' then true else false end as is_recently_active,
        case when c.total_claims > 0 then true else false end as has_claims,

        -- High-risk flags for targeted interventions
        case when b.chronic_condition_count >= 5 then true else false end as high_chronic_burden,
        case when c.total_claim_amount > 100000 then true else false end as high_cost_member,
        case when c.inpatient_claims >= 3 then true else false end as frequent_admissions,

        -- Metadata
        b.loaded_at as source_loaded_at,
        current_timestamp as dim_loaded_at

    from {{ ref('stg_cms_beneficiaries') }} b
    left join beneficiary_claims c
        on b.beneficiary_id = c.beneficiary_id
)

select * from final