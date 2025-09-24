-- Test for healthcare-specific business rule violations
{{ config(severity='warn', tags=['data_quality', 'business_rules']) }}
{{ test_business_rule_violations() }}