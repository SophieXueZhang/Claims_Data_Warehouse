-- Comprehensive data quality test suite for Claims Data Warehouse

-- Test 1: Claim Amount Consistency
{{ config(severity='error', tags=['data_quality', 'financial']) }}
{{ test_claim_amount_consistency() }}
