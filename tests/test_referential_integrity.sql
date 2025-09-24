-- Test for referential integrity violations
{{ config(severity='error', tags=['data_quality', 'referential_integrity']) }}
{{ test_referential_integrity_orphaned_claims() }}