{{ config(
    materialized='view',
    tags=['staging', 'cms', 'claims']
) }}

with inpatient_claims as (
    select
        -- Identifiers
        desynpuf_id as beneficiary_id,
        clm_id as claim_id,
        prvdr_num as provider_id,

        -- Claim information
        'Inpatient' as claim_type,
        clm_from_dt as claim_start_date,
        clm_thru_dt as claim_end_date,
        clm_admsn_dt as admission_date,
        nch_bene_dschrg_dt as discharge_date,

        -- Financial amounts
        clm_pmt_amt as reimbursement_amount,
        nch_prmry_pyr_clm_pd_amt as primary_payer_amount,
        nch_ip_ncvrd_chrg_amt as non_covered_amount,
        nch_ip_totl_ddctbl_amt as deductible_amount,
        clm_tot_chrg_amt as claim_amount,

        -- Diagnosis codes
        icd9_dgns_cd_1 as diagnosis_code_1,
        icd9_dgns_cd_2 as diagnosis_code_2,
        icd9_dgns_cd_3 as diagnosis_code_3,

        -- Procedure codes
        icd9_prcdr_cd_1 as procedure_code_1,
        icd9_prcdr_cd_2 as procedure_code_2,
        icd9_prcdr_cd_3 as procedure_code_3

    from {{ source('cms_raw', 'inpatient_claims') }}

    union all

    select
        -- Identifiers
        desynpuf_id as beneficiary_id,
        clm_id as claim_id,
        prvdr_num as provider_id,

        -- Claim information
        'Outpatient' as claim_type,
        clm_from_dt as claim_start_date,
        clm_thru_dt as claim_end_date,
        null as admission_date,
        null as discharge_date,

        -- Financial amounts
        clm_pmt_amt as reimbursement_amount,
        nch_prmry_pyr_clm_pd_amt as primary_payer_amount,
        nch_bene_blood_ddctbl_lblty_am as blood_deductible_amount,
        nch_bene_ptb_ddctbl_amt as part_b_deductible_amount,
        clm_tot_chrg_amt as claim_amount,

        -- Diagnosis codes
        icd9_dgns_cd_1 as diagnosis_code_1,
        icd9_dgns_cd_2 as diagnosis_code_2,
        icd9_dgns_cd_3 as diagnosis_code_3,

        -- Procedure codes
        icd9_prcdr_cd_1 as procedure_code_1,
        icd9_prcdr_cd_2 as procedure_code_2,
        icd9_prcdr_cd_3 as procedure_code_3

    from {{ source('cms_raw', 'outpatient_claims') }}

    union all

    select
        -- Identifiers
        desynpuf_id as beneficiary_id,
        clm_id as claim_id,
        prvdr_npi as provider_id,

        -- Claim information
        'Carrier' as claim_type,
        clm_from_dt as claim_start_date,
        clm_thru_dt as claim_end_date,
        null as admission_date,
        null as discharge_date,

        -- Financial amounts
        clm_pmt_amt as reimbursement_amount,
        nch_prmry_pyr_clm_pd_amt as primary_payer_amount,
        null as non_covered_amount,
        nch_carr_clm_cash_ddctbl_apld_amt as deductible_amount,
        clm_tot_chrg_amt as claim_amount,

        -- Diagnosis codes
        icd9_dgns_cd_1 as diagnosis_code_1,
        icd9_dgns_cd_2 as diagnosis_code_2,
        icd9_dgns_cd_3 as diagnosis_code_3,

        -- Procedure codes - using HCPCS codes for carrier claims
        hcpcs_cd_1 as procedure_code_1,
        hcpcs_cd_2 as procedure_code_2,
        hcpcs_cd_3 as procedure_code_3

    from {{ source('cms_raw', 'carrier_claims') }}
),

cleaned as (
    select
        -- Primary identifiers
        {{ dbt_utils.generate_surrogate_key(['claim_id']) }} as claim_key,
        claim_id,
        beneficiary_id,
        provider_id,

        -- Claim information
        claim_type,
        cast(claim_start_date as date) as claim_start_date,
        cast(claim_end_date as date) as claim_end_date,
        cast(admission_date as date) as admission_date,
        cast(discharge_date as date) as discharge_date,

        -- Financial amounts with cleaning
        coalesce(claim_amount, 0) as claim_amount,
        coalesce(reimbursement_amount, 0) as reimbursement_amount,
        coalesce(primary_payer_amount, 0) as primary_payer_amount,
        coalesce(deductible_amount, 0) as deductible_amount,

        -- Calculate derived financial metrics
        case
            when claim_amount > 0 then reimbursement_amount / claim_amount
            else 0
        end as reimbursement_ratio,

        claim_amount - reimbursement_amount as patient_responsibility,

        case
            when reimbursement_amount > 0 then 'Paid'
            when reimbursement_amount = 0 and claim_amount > 0 then 'Denied'
            else 'Pending'
        end as claim_status,

        -- Service duration
        case
            when claim_end_date >= claim_start_date then
                claim_end_date - claim_start_date + 1
            else 1
        end as service_days,

        -- Length of stay for inpatient claims
        case
            when claim_type = 'Inpatient' and discharge_date >= admission_date then
                discharge_date - admission_date + 1
            else null
        end as length_of_stay,

        -- Diagnosis and procedure codes
        diagnosis_code_1,
        diagnosis_code_2,
        diagnosis_code_3,
        procedure_code_1,
        procedure_code_2,
        procedure_code_3,

        -- Processing timing (synthetic dates for demo)
        claim_start_date + interval '30 days' as processed_at,
        claim_start_date - interval '7 days' as created_at,

        -- Data quality flags
        case when beneficiary_id is null then true else false end as beneficiary_missing,
        case when provider_id is null then true else false end as provider_missing,
        case when claim_amount < 0 then true else false end as negative_amount,
        case when diagnosis_code_1 is null then true else false end as diagnosis_missing,

        -- Metadata
        current_timestamp as loaded_at

    from inpatient_claims
    where claim_id is not null
      and beneficiary_id is not null
      and claim_start_date is not null
)

select * from cleaned