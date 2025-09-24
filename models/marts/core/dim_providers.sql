{{ config(
    materialized='table',
    indexes=[
        {'columns': ['provider_id'], 'unique': true},
        {'columns': ['state_code']},
        {'columns': ['specialty_description']},
        {'columns': ['provider_type']}
    ],
    tags=['dimension', 'core', 'providers']
) }}

with providers_with_claims as (
    select
        provider_id,
        count(*) as total_claims,
        sum(claim_amount) as total_claim_amount,
        sum(reimbursement_amount) as total_reimbursement,
        min(claim_start_date) as first_claim_date,
        max(claim_start_date) as last_claim_date,
        count(distinct beneficiary_id) as unique_patients
    from {{ ref('stg_cms_claims') }}
    group by provider_id
),

provider_specialties as (
    select
        provider_id,
        specialty_description,
        row_number() over (partition by provider_id order by specialty_description) as specialty_rank
    from {{ ref('stg_cms_providers') }}
    where specialty_description is not null
),

final as (
    select
        -- Surrogate key
        p.provider_key,

        -- Business keys
        p.provider_id,
        p.npi,

        -- Provider information
        p.provider_name,
        p.provider_first_name,
        p.provider_last_name,
        p.provider_middle_initial,
        p.credentials,
        p.provider_type,
        p.entity_code,

        -- Specialty information
        p.specialty_code,
        p.specialty_description,
        ps.specialty_description as primary_specialty,

        -- Geographic information
        p.address_line_1,
        p.address_line_2,
        p.city,
        p.state_code,
        p.zip_code,
        p.country_code,

        -- Medicare participation
        p.participates_in_medicare,

        -- Claims statistics
        coalesce(c.total_claims, 0) as total_claims,
        coalesce(c.total_claim_amount, 0) as total_claim_amount,
        coalesce(c.total_reimbursement, 0) as total_reimbursement,
        coalesce(c.unique_patients, 0) as unique_patients,

        -- Provider activity metrics
        case
            when c.total_claims >= 100 then 'High Volume'
            when c.total_claims >= 25 then 'Medium Volume'
            when c.total_claims > 0 then 'Low Volume'
            else 'No Claims'
        end as volume_tier,

        case
            when c.total_claim_amount > 0 then
                round(c.total_reimbursement / c.total_claim_amount, 4)
            else 0
        end as reimbursement_rate,

        c.first_claim_date,
        c.last_claim_date,

        -- Activity flags
        case when c.last_claim_date >= current_date - interval '90 days' then true else false end as is_recently_active,
        case when c.total_claims > 0 then true else false end as has_claims,
        case when p.participates_in_medicare = true and c.total_claims > 0 then true else false end as is_active,

        -- Data quality flags
        p.name_missing,
        p.address_missing,
        p.state_missing,

        -- Risk classification based on claim patterns
        case
            when c.total_claims > 500 and c.unique_patients < 50 then 'High Risk - High Claims/Low Patients'
            when c.total_claim_amount > 1000000 then 'High Risk - High Dollar Volume'
            when c.total_claims = 0 then 'No Risk - No Claims'
            else 'Normal'
        end as risk_category,

        -- Metadata
        p.loaded_at as source_loaded_at,
        current_timestamp as dim_loaded_at

    from {{ ref('stg_cms_providers') }} p
    left join providers_with_claims c
        on p.provider_id = c.provider_id
    left join provider_specialties ps
        on p.provider_id = ps.provider_id
        and ps.specialty_rank = 1
)

select * from final