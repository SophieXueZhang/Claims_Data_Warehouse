{{ config(
    materialized='view',
    tags=['staging', 'cms', 'beneficiaries']
) }}

with source_data as (
    select
        -- Primary identifiers
        desynpuf_id as beneficiary_id,
        bene_birth_dt as date_of_birth,
        bene_death_dt as date_of_death,
        bene_sex_ident_cd as gender,
        bene_race_cd as race_code,
        bene_esrd_ind as esrd_indicator,
        sp_state_code as state_code,
        bene_county_cd as county_code,

        -- Enrollment dates
        bene_hi_cvrage_tot_mons as hi_coverage_months,
        bene_smi_cvrage_tot_mons as smi_coverage_months,
        bene_hmo_cvrage_tot_mons as hmo_coverage_months,
        plan_cvrg_mos_num as plan_coverage_months,

        -- Chronic conditions flags
        sp_alzhdmta as alzheimer_flag,
        sp_chf as heart_failure_flag,
        sp_chrnkidn as chronic_kidney_flag,
        sp_cncr as cancer_flag,
        sp_copd as copd_flag,
        sp_depressn as depression_flag,
        sp_diabetes as diabetes_flag,
        sp_ischmcht as ischemic_heart_flag,
        sp_osteoprs as osteoporosis_flag,
        sp_ra_oa as arthritis_flag,
        sp_strketia as stroke_flag

    from {{ source('cms_raw', 'beneficiary_summary') }}
),

cleaned as (
    select
        -- Primary identifiers
        beneficiary_id,
        {{ dbt_utils.generate_surrogate_key(['beneficiary_id']) }} as beneficiary_key,

        -- Demographics with cleaning
        case
            when date_of_birth = '19000101' then null
            else cast(date_of_birth as date)
        end as date_of_birth,

        case
            when date_of_death = '00000000' then null
            else cast(date_of_death as date)
        end as date_of_death,

        case
            when gender = '1' then 'M'
            when gender = '2' then 'F'
            else 'U'
        end as gender,

        case
            when race_code = '1' then 'White'
            when race_code = '2' then 'Black'
            when race_code = '3' then 'Other'
            when race_code = '5' then 'Hispanic'
            else 'Unknown'
        end as race_description,

        race_code,
        state_code,
        county_code,

        -- Enrollment information
        hi_coverage_months,
        smi_coverage_months,
        hmo_coverage_months,
        plan_coverage_months,

        -- Calculate enrollment start/end dates (approximated for synthetic data)
        cast('2008-01-01' as date) as enrollment_start_date,
        cast('2009-12-31' as date) as enrollment_end_date,

        -- Chronic conditions
        case when alzheimer_flag = '1' then true else false end as has_alzheimer,
        case when heart_failure_flag = '1' then true else false end as has_heart_failure,
        case when chronic_kidney_flag = '1' then true else false end as has_chronic_kidney,
        case when cancer_flag = '1' then true else false end as has_cancer,
        case when copd_flag = '1' then true else false end as has_copd,
        case when depression_flag = '1' then true else false end as has_depression,
        case when diabetes_flag = '1' then true else false end as has_diabetes,
        case when ischemic_heart_flag = '1' then true else false end as has_ischemic_heart,
        case when osteoporosis_flag = '1' then true else false end as has_osteoporosis,
        case when arthritis_flag = '1' then true else false end as has_arthritis,
        case when stroke_flag = '1' then true else false end as has_stroke,

        -- Calculate chronic condition count
        (case when alzheimer_flag = '1' then 1 else 0 end +
         case when heart_failure_flag = '1' then 1 else 0 end +
         case when chronic_kidney_flag = '1' then 1 else 0 end +
         case when cancer_flag = '1' then 1 else 0 end +
         case when copd_flag = '1' then 1 else 0 end +
         case when depression_flag = '1' then 1 else 0 end +
         case when diabetes_flag = '1' then 1 else 0 end +
         case when ischemic_heart_flag = '1' then 1 else 0 end +
         case when osteoporosis_flag = '1' then 1 else 0 end +
         case when arthritis_flag = '1' then 1 else 0 end +
         case when stroke_flag = '1' then 1 else 0 end) as chronic_condition_count,

        -- Age calculation
        case
            when date_of_birth is not null then
                date_part('year', age(current_date, date_of_birth))
            else null
        end as current_age,

        -- Deceased flag
        case when date_of_death is not null then true else false end as is_deceased,

        -- Metadata
        current_timestamp as loaded_at

    from source_data
)

select * from cleaned