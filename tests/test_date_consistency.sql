-- Test for date consistency across all date fields in claims
{{ config(severity='error', tags=['data_quality', 'dates']) }}
{{ test_date_consistency() }}