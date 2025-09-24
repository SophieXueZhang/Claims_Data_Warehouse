-- 📊 Claims Data Warehouse - Comprehensive Business Intelligence Report
-- Author: Sophie Zhang
-- Purpose: Generate complete business analysis report showcasing data warehouse capabilities

-- ====================================================================
-- 📈 Section 1: Executive Summary - Key Business Metrics Overview
-- ====================================================================

-- 1.1 Overall Business Performance
WITH executive_summary AS (
    SELECT
        'Claims Processing Overview' as report_section,
        COUNT(DISTINCT beneficiary_key) as total_beneficiaries,
        COUNT(DISTINCT provider_key) as total_providers,
        COUNT(*) as total_claims,
        ROUND(SUM(claim_amount)::decimal, 2) as total_claim_value,
        ROUND(SUM(reimbursement_amount)::decimal, 2) as total_reimbursed,
        ROUND(AVG(claim_amount)::decimal, 2) as avg_claim_amount,
        ROUND(
            COUNT(CASE WHEN is_denied THEN 1 END)::decimal / COUNT(*) * 100,
            2
        ) as overall_denial_rate_pct,
        ROUND(AVG(processing_days)::decimal, 1) as avg_processing_days
    FROM {{ ref('fact_claims') }}
)
SELECT * FROM executive_summary;

-- 1.2 Claims Distribution by Type
WITH claim_type_breakdown AS (
    SELECT
        claim_type,
        COUNT(*) as claim_count,
        ROUND(COUNT(*)::decimal / SUM(COUNT(*)) OVER() * 100, 1) as percentage,
        ROUND(SUM(claim_amount)::decimal, 2) as total_value,
        ROUND(AVG(claim_amount)::decimal, 2) as avg_value,
        ROUND(
            COUNT(CASE WHEN is_denied THEN 1 END)::decimal / COUNT(*) * 100,
            2
        ) as denial_rate_pct
    FROM {{ ref('fact_claims') }}
    GROUP BY claim_type
    ORDER BY claim_count DESC
)
SELECT * FROM claim_type_breakdown;

-- ====================================================================
-- 💰 Section 2: Financial Analysis - Cost and Revenue Insights
-- ====================================================================

-- 2.1 Monthly Financial Trends
WITH monthly_financial_trends AS (
    SELECT
        DATE_TRUNC('month', claim_start_date) as month,
        COUNT(*) as monthly_claims,
        ROUND(SUM(claim_amount)::decimal, 2) as total_claims_value,
        ROUND(SUM(reimbursement_amount)::decimal, 2) as total_reimbursed,
        ROUND(SUM(patient_responsibility)::decimal, 2) as total_patient_cost,
        ROUND(
            SUM(reimbursement_amount)::decimal / SUM(claim_amount) * 100,
            2
        ) as reimbursement_rate_pct,
        ROUND(
            COUNT(CASE WHEN is_denied THEN 1 END)::decimal / COUNT(*) * 100,
            2
        ) as denial_rate_pct
    FROM {{ ref('fact_claims') }}
    GROUP BY DATE_TRUNC('month', claim_start_date)
    ORDER BY month
)
SELECT * FROM monthly_financial_trends;

-- 2.2 High-Cost Claims Analysis
WITH high_cost_claims_analysis AS (
    SELECT
        'High Cost Claims (>$10,000)' as analysis_type,
        COUNT(*) as high_cost_claim_count,
        ROUND(COUNT(*)::decimal / (SELECT COUNT(*) FROM {{ ref('fact_claims') }}) * 100, 2) as pct_of_total_claims,
        ROUND(SUM(claim_amount)::decimal, 2) as high_cost_total_value,
        ROUND(SUM(claim_amount)::decimal / (SELECT SUM(claim_amount) FROM {{ ref('fact_claims') }}) * 100, 2) as pct_of_total_value,
        ROUND(AVG(claim_amount)::decimal, 2) as avg_high_cost_amount,
        ROUND(AVG(processing_days)::decimal, 1) as avg_processing_days
    FROM {{ ref('fact_claims') }}
    WHERE is_high_dollar = true
)
SELECT * FROM high_cost_claims_analysis;

-- ====================================================================
-- 🏥 Section 3: Provider Analysis - Performance and Quality Assessment
-- ====================================================================

-- 3.1 Top Provider Performance Rankings
WITH top_providers_performance AS (
    SELECT
        provider_name,
        specialty_description,
        total_claims,
        ROUND(avg_claim_amount, 2) as avg_claim_amount,
        ROUND(denial_rate * 100, 2) as denial_rate_pct,
        performance_tier,
        risk_category,
        RANK() OVER (ORDER BY total_claims DESC) as volume_rank,
        RANK() OVER (ORDER BY denial_rate ASC) as quality_rank
    FROM {{ ref('metrics_provider_performance') }}
    WHERE total_claims >= 5
    ORDER BY total_claims DESC
    LIMIT 10
)
SELECT * FROM top_providers_performance;

-- 3.2 Specialty Performance Comparison
WITH specialty_comparison AS (
    SELECT
        specialty_description,
        COUNT(*) as provider_count,
        ROUND(AVG(total_claims)::decimal, 0) as avg_claims_per_provider,
        ROUND(AVG(avg_claim_amount)::decimal, 2) as avg_claim_amount,
        ROUND(AVG(denial_rate) * 100, 2) as avg_denial_rate_pct,
        COUNT(CASE WHEN performance_tier = 'Top Performer' THEN 1 END) as top_performers,
        COUNT(CASE WHEN performance_tier = 'Needs Improvement' THEN 1 END) as needs_improvement
    FROM {{ ref('metrics_provider_performance') }}
    WHERE specialty_description IS NOT NULL
    GROUP BY specialty_description
    HAVING COUNT(*) >= 2
    ORDER BY avg_claims_per_provider DESC
)
SELECT * FROM specialty_comparison;

-- ====================================================================
-- 👤 Section 4: Member Analysis - Utilization and Risk Management
-- ====================================================================

-- 4.1 Risk Stratification Analysis
WITH risk_stratification_analysis AS (
    SELECT
        risk_tier,
        COUNT(*) as member_count,
        ROUND(COUNT(*)::decimal / SUM(COUNT(*)) OVER() * 100, 1) as percentage,
        ROUND(AVG(total_cost)::decimal, 2) as avg_total_cost,
        ROUND(SUM(total_cost)::decimal, 2) as total_cost_by_tier,
        ROUND(AVG(chronic_condition_count)::decimal, 1) as avg_chronic_conditions,
        ROUND(AVG(total_claims)::decimal, 0) as avg_claims_per_member,
        COUNT(CASE WHEN needs_case_management THEN 1 END) as needs_case_management
    FROM {{ ref('metrics_beneficiary_utilization') }}
    GROUP BY risk_tier
    ORDER BY
        CASE risk_tier
            WHEN 'High Risk' THEN 1
            WHEN 'Medium Risk' THEN 2
            WHEN 'Low Risk' THEN 3
            ELSE 4
        END
)
SELECT * FROM risk_stratification_analysis;

-- 4.2 Chronic Conditions Impact Analysis
WITH chronic_conditions_impact AS (
    SELECT
        CASE
            WHEN chronic_condition_count = 0 THEN '0 conditions'
            WHEN chronic_condition_count BETWEEN 1 AND 2 THEN '1-2 conditions'
            WHEN chronic_condition_count BETWEEN 3 AND 5 THEN '3-5 conditions'
            ELSE '6+ conditions'
        END as condition_category,
        COUNT(*) as member_count,
        ROUND(AVG(total_cost)::decimal, 2) as avg_cost_per_member,
        ROUND(AVG(total_claims)::decimal, 0) as avg_claims_per_member,
        ROUND(AVG(denial_rate) * 100, 2) as avg_denial_rate_pct,
        COUNT(CASE WHEN frequent_admissions THEN 1 END) as frequent_admissions_count
    FROM {{ ref('metrics_beneficiary_utilization') }}
    GROUP BY
        CASE
            WHEN chronic_condition_count = 0 THEN '0 conditions'
            WHEN chronic_condition_count BETWEEN 1 AND 2 THEN '1-2 conditions'
            WHEN chronic_condition_count BETWEEN 3 AND 5 THEN '3-5 conditions'
            ELSE '6+ conditions'
        END
    ORDER BY AVG(total_cost) DESC
)
SELECT * FROM chronic_conditions_impact;

-- ====================================================================
-- 📊 Section 5: Operational Efficiency - Processing Time and Quality
-- ====================================================================

-- 5.1 Processing Efficiency Analysis
WITH processing_efficiency_analysis AS (
    SELECT
        processing_speed_category,
        COUNT(*) as claim_count,
        ROUND(COUNT(*)::decimal / SUM(COUNT(*)) OVER() * 100, 1) as percentage,
        ROUND(AVG(processing_days)::decimal, 1) as avg_processing_days,
        ROUND(AVG(claim_amount)::decimal, 2) as avg_claim_amount,
        ROUND(
            COUNT(CASE WHEN is_denied THEN 1 END)::decimal / COUNT(*) * 100,
            2
        ) as denial_rate_pct
    FROM {{ ref('fact_claims') }}
    GROUP BY processing_speed_category
    ORDER BY
        CASE processing_speed_category
            WHEN 'Fast (≤7 days)' THEN 1
            WHEN 'Normal (8-14 days)' THEN 2
            WHEN 'Slow (15-30 days)' THEN 3
            WHEN 'Very Slow (>30 days)' THEN 4
            ELSE 5
        END
)
SELECT * FROM processing_efficiency_analysis;

-- 5.2 Denial Analysis by Claim Type
WITH denial_analysis_by_type AS (
    SELECT
        claim_type,
        COUNT(*) as total_claims,
        COUNT(CASE WHEN is_denied THEN 1 END) as denied_claims,
        ROUND(
            COUNT(CASE WHEN is_denied THEN 1 END)::decimal / COUNT(*) * 100,
            2
        ) as denial_rate_pct,
        ROUND(AVG(CASE WHEN is_denied THEN processing_days END)::decimal, 1) as avg_denial_processing_days,
        ROUND(AVG(CASE WHEN is_denied THEN claim_amount END)::decimal, 2) as avg_denied_claim_amount
    FROM {{ ref('fact_claims') }}
    GROUP BY claim_type
    ORDER BY denial_rate_pct DESC
)
SELECT * FROM denial_analysis_by_type;

-- ====================================================================
-- 🎯 Section 6: Strategic Recommendations - Data-Driven Action Items
-- ====================================================================

-- 6.1 Cost Optimization Opportunities
WITH cost_optimization_opportunities AS (
    SELECT
        'Cost Optimization Opportunities' as analysis_category,
        'High-cost providers with above-average denial rates' as opportunity_type,
        COUNT(*) as provider_count,
        ROUND(SUM(total_claim_amount)::decimal, 2) as potential_savings_target,
        'Provider engagement and quality improvement programs' as recommended_action
    FROM {{ ref('metrics_provider_performance') }}
    WHERE avg_claim_amount > (SELECT AVG(avg_claim_amount) FROM {{ ref('metrics_provider_performance') }})
      AND denial_rate > (SELECT AVG(denial_rate) FROM {{ ref('metrics_provider_performance') }})

    UNION ALL

    SELECT
        'Cost Optimization Opportunities' as analysis_category,
        'High-cost members requiring case management' as opportunity_type,
        COUNT(*) as member_count,
        ROUND(SUM(total_cost)::decimal, 2) as potential_savings_target,
        'Implement proactive case management programs' as recommended_action
    FROM {{ ref('metrics_beneficiary_utilization') }}
    WHERE needs_case_management = true
)
SELECT * FROM cost_optimization_opportunities;

-- 6.2 Quality Improvement Recommendations
WITH quality_improvement_recommendations AS (
    SELECT
        'Processing Efficiency' as improvement_area,
        COUNT(*) as claims_affected,
        'Implement automated pre-authorization for routine procedures' as recommendation,
        ROUND(AVG(processing_days)::decimal, 1) as current_avg_days,
        '7 days' as target_processing_time
    FROM {{ ref('fact_claims') }}
    WHERE processing_speed_category = 'Slow (15-30 days)'
       OR processing_speed_category = 'Very Slow (>30 days)'

    UNION ALL

    SELECT
        'Provider Network Quality' as improvement_area,
        COUNT(*) as providers_affected,
        'Provider education and quality incentive programs' as recommendation,
        ROUND(AVG(denial_rate) * 100, 2) as current_denial_rate_pct,
        '< 5%' as target_denial_rate
    FROM {{ ref('metrics_provider_performance') }}
    WHERE performance_tier = 'Needs Improvement'
)
SELECT * FROM quality_improvement_recommendations;

-- ====================================================================
-- 📋 Section 7: Data Quality Assessment - Technical Metrics
-- ====================================================================

-- 7.1 Data Completeness and Accuracy Metrics
WITH data_quality_metrics AS (
    SELECT
        'Data Quality Assessment' as metric_category,
        'Total Records Processed' as metric_name,
        COUNT(*)::text as metric_value,
        'records' as unit
    FROM {{ ref('fact_claims') }}

    UNION ALL

    SELECT
        'Data Quality Assessment' as metric_category,
        'Provider Information Completeness' as metric_name,
        ROUND(
            COUNT(CASE WHEN NOT provider_missing THEN 1 END)::decimal / COUNT(*) * 100,
            1
        )::text || '%' as metric_value,
        'percentage' as unit
    FROM {{ ref('fact_claims') }}

    UNION ALL

    SELECT
        'Data Quality Assessment' as metric_category,
        'Diagnosis Information Completeness' as metric_name,
        ROUND(
            COUNT(CASE WHEN NOT diagnosis_missing THEN 1 END)::decimal / COUNT(*) * 100,
            1
        )::text || '%' as metric_value,
        'percentage' as unit
    FROM {{ ref('fact_claims') }}

    UNION ALL

    SELECT
        'Data Quality Assessment' as metric_category,
        'Financial Data Accuracy' as metric_name,
        ROUND(
            COUNT(CASE WHEN NOT negative_amount THEN 1 END)::decimal / COUNT(*) * 100,
            1
        )::text || '%' as metric_value,
        'percentage' as unit
    FROM {{ ref('fact_claims') }}
)
SELECT * FROM data_quality_metrics;

-- ====================================================================
-- 📊 Section 8: Executive Summary - Key Insights and Next Steps
-- ====================================================================

-- 8.1 Key Business Insights Summary
WITH key_business_insights AS (
    SELECT
        'Key Business Insights' as section,
        1 as insight_order,
        'Financial Performance' as insight_category,
        'Total claims value: $' ||
        ROUND(SUM(claim_amount)::decimal, 2)::text ||
        ' with ' ||
        ROUND(AVG(processing_days)::decimal, 1)::text ||
        ' days average processing time' as insight_description
    FROM {{ ref('fact_claims') }}

    UNION ALL

    SELECT
        'Key Business Insights' as section,
        2 as insight_order,
        'Risk Management' as insight_category,
        COUNT(CASE WHEN risk_tier = 'High Risk' THEN 1 END)::text ||
        ' high-risk members identified requiring case management (' ||
        ROUND(
            COUNT(CASE WHEN risk_tier = 'High Risk' THEN 1 END)::decimal /
            COUNT(*) * 100, 1
        )::text || '% of total population)' as insight_description
    FROM {{ ref('metrics_beneficiary_utilization') }}

    UNION ALL

    SELECT
        'Key Business Insights' as section,
        3 as insight_order,
        'Provider Network Quality' as insight_category,
        COUNT(CASE WHEN performance_tier IN ('Top Performer', 'High Performer') THEN 1 END)::text ||
        ' high-performing providers identified for partnership expansion' as insight_description
    FROM {{ ref('metrics_provider_performance') }}

    ORDER BY insight_order
)
SELECT * FROM key_business_insights;

-- ====================================================================
-- 🔍 Section 9: Advanced Analytics - Predictive Insights
-- ====================================================================

-- 9.1 Member Risk Prediction Model Inputs
WITH member_risk_factors AS (
    SELECT
        'Member Risk Modeling' as analysis_type,
        age_group,
        COUNT(*) as member_count,
        ROUND(AVG(total_cost)::decimal, 2) as avg_annual_cost,
        ROUND(AVG(chronic_condition_count)::decimal, 1) as avg_conditions,
        ROUND(AVG(utilization_adjusted_risk_score)::decimal, 2) as avg_risk_score,
        COUNT(CASE WHEN needs_case_management THEN 1 END) as high_risk_candidates
    FROM {{ ref('metrics_beneficiary_utilization') }}
    GROUP BY age_group
    ORDER BY avg_risk_score DESC
)
SELECT * FROM member_risk_factors;

-- 9.2 Provider Performance Correlation Analysis
WITH provider_performance_correlations AS (
    SELECT
        'Provider Performance Correlations' as analysis_type,
        specialty_description,
        COUNT(*) as provider_count,
        ROUND(CORR(total_claims, denial_rate)::decimal, 3) as volume_denial_correlation,
        ROUND(CORR(avg_claim_amount, denial_rate)::decimal, 3) as cost_denial_correlation,
        ROUND(AVG(CASE WHEN performance_tier = 'Top Performer' THEN 1.0 ELSE 0.0 END), 3) as top_performer_rate
    FROM {{ ref('metrics_provider_performance') }}
    WHERE specialty_description IS NOT NULL
    GROUP BY specialty_description
    HAVING COUNT(*) >= 3
    ORDER BY top_performer_rate DESC
)
SELECT * FROM provider_performance_correlations;