{{ config(
    materialized='view',
    tags=['staging', 'cms', 'providers']
) }}

with source_data as (
    select
        -- Provider identifiers
        npi,
        nppes_provider_last_org_name as provider_name,
        nppes_provider_first_name as provider_first_name,
        nppes_provider_mi as provider_middle_initial,
        nppes_credentials as credentials,
        nppes_entity_code as entity_code,

        -- Provider classification
        provider_type,
        medicare_participation_indicator,
        place_of_service,

        -- Address information
        nppes_provider_street1 as address_line_1,
        nppes_provider_street2 as address_line_2,
        nppes_provider_city as city,
        nppes_provider_state as state_code,
        nppes_provider_zip as zip_code,
        nppes_provider_country as country_code,

        -- Specialty information
        healthcare_provider_taxonomy_code_1 as primary_taxonomy,
        healthcare_provider_taxonomy_code_2 as secondary_taxonomy,
        healthcare_provider_taxonomy_code_3 as tertiary_taxonomy,
        provider_type as specialty_description

    from {{ source('cms_raw', 'provider_data') }}
),

cleaned as (
    select
        -- Primary identifiers
        {{ dbt_utils.generate_surrogate_key(['npi']) }} as provider_key,
        npi as provider_id,
        npi,

        -- Provider name standardization
        case
            when entity_code = 'I' then
                trim(coalesce(provider_first_name, '') || ' ' ||
                     coalesce(provider_middle_initial, '') || ' ' ||
                     coalesce(provider_name, ''))
            else coalesce(provider_name, 'Unknown Provider')
        end as provider_name,

        provider_first_name,
        provider_name as provider_last_name,
        provider_middle_initial,
        credentials,

        -- Provider type and classification
        case
            when entity_code = 'I' then 'Individual'
            when entity_code = 'O' then 'Organization'
            else 'Unknown'
        end as provider_type,

        entity_code,

        case
            when medicare_participation_indicator = 'Y' then true
            when medicare_participation_indicator = 'N' then false
            else null
        end as participates_in_medicare,

        place_of_service,

        -- Address standardization
        trim(address_line_1) as address_line_1,
        trim(address_line_2) as address_line_2,
        trim(upper(city)) as city,
        trim(upper(state_code)) as state_code,
        trim(zip_code) as zip_code,
        trim(upper(country_code)) as country_code,

        -- Specialty information
        primary_taxonomy as specialty_code,
        case
            when primary_taxonomy like '207%' then 'Medical Doctor'
            when primary_taxonomy like '208%' then 'Pediatric Specialist'
            when primary_taxonomy like '209%' then 'Allopathic & Osteopathic Physician'
            when primary_taxonomy like '163%' then 'Podiatrist'
            when primary_taxonomy like '171%' then 'Audiologist'
            when primary_taxonomy like '172%' then 'Speech Language Pathologist'
            when primary_taxonomy like '173%' then 'Occupational Therapist'
            when primary_taxonomy like '174%' then 'Physical Therapist'
            when primary_taxonomy like '175%' then 'Respiratory Therapist'
            when primary_taxonomy like '176%' then 'Dietitian/Nutritionist'
            when primary_taxonomy like '177%' then 'Other'
            when primary_taxonomy like '193%' then 'Psychologist'
            when primary_taxonomy like '251%' then 'Pharmacist'
            when primary_taxonomy like '261%' then 'Nurse Practitioner'
            when primary_taxonomy like '364%' then 'Nurse Anesthetist'
            when primary_taxonomy like '367%' then 'Physician Assistant'
            else coalesce(specialty_description, 'Other')
        end as specialty_description,

        secondary_taxonomy,
        tertiary_taxonomy,

        -- Data quality flags
        case when provider_name is null or trim(provider_name) = '' then true else false end as name_missing,
        case when address_line_1 is null or trim(address_line_1) = '' then true else false end as address_missing,
        case when state_code is null or trim(state_code) = '' then true else false end as state_missing,

        -- Metadata
        current_timestamp as loaded_at

    from source_data
    where npi is not null
)

select * from cleaned