{% macro generate_business_report() %}
    /*
    生成综合业务智能报告的宏
    用途: 一键生成完整的业务分析报告
    */

    {% set report_queries = [
        'executive_summary',
        'financial_analysis',
        'provider_performance',
        'member_risk_analysis',
        'operational_efficiency',
        'quality_metrics'
    ] %}

    {{ log("📊 生成综合业务智能报告...", info=true) }}

    -- 创建报告输出表
    {% set report_table = 'business_intelligence_report_' ~ run_started_at.strftime('%Y%m%d') %}

    {{ log("📝 报告将保存到: " ~ report_table, info=true) }}

    -- 执行报告生成
    CREATE TABLE {{ target.schema }}.{{ report_table }} AS (
        {{ ref('analyses', 'business_intelligence_report') }}
    );

    {{ log("✅ 业务报告生成完成!", info=true) }}
    {{ log("📊 报告表名: " ~ target.schema ~ "." ~ report_table, info=true) }}

{% endmacro %}

{% macro export_report_to_csv() %}
    /*
    导出报告数据到 CSV 文件
    */

    {% if execute %}
        {% set export_query %}
            COPY (
                SELECT * FROM {{ ref('analyses', 'business_intelligence_report') }}
            ) TO STDOUT WITH CSV HEADER;
        {% endset %}

        {{ log("💾 执行 CSV 导出查询...", info=true) }}
        {{ log("查询: " ~ export_query, info=true) }}
    {% endif %}

{% endmacro %}

{% macro generate_executive_dashboard() %}
    /*
    生成高管仪表板关键指标
    */

    WITH dashboard_metrics AS (
        SELECT
            'Total Claims Value' as metric_name,
            '$' || ROUND(SUM(claim_amount)/1000000, 1)::text || 'M' as metric_value,
            'Financial' as category
        FROM {{ ref('fact_claims') }}

        UNION ALL

        SELECT
            'Overall Denial Rate' as metric_name,
            ROUND(
                COUNT(CASE WHEN is_denied THEN 1 END)::decimal / COUNT(*) * 100,
                1
            )::text || '%' as metric_value,
            'Quality' as category
        FROM {{ ref('fact_claims') }}

        UNION ALL

        SELECT
            'High Risk Members' as metric_name,
            COUNT(*)::text as metric_value,
            'Risk Management' as category
        FROM {{ ref('metrics_beneficiary_utilization') }}
        WHERE risk_tier = 'High Risk'

        UNION ALL

        SELECT
            'Top Performing Providers' as metric_name,
            COUNT(*)::text as metric_value,
            'Network' as category
        FROM {{ ref('metrics_provider_performance') }}
        WHERE performance_tier = 'Top Performer'

        UNION ALL

        SELECT
            'Avg Processing Days' as metric_name,
            ROUND(AVG(processing_days), 1)::text || ' days' as metric_value,
            'Operations' as category
        FROM {{ ref('fact_claims') }}
    )

    SELECT * FROM dashboard_metrics
    ORDER BY category, metric_name

{% endmacro %}

{% macro generate_monthly_kpi_trend() %}
    /*
    生成月度KPI趋势数据
    */

    WITH monthly_kpis AS (
        SELECT
            DATE_TRUNC('month', claim_start_date) as month,

            -- 财务指标
            ROUND(SUM(claim_amount)/1000000, 2) as total_claim_value_millions,
            ROUND(AVG(claim_amount), 2) as avg_claim_amount,

            -- 质量指标
            ROUND(
                COUNT(CASE WHEN is_denied THEN 1 END)::decimal / COUNT(*) * 100,
                2
            ) as denial_rate_pct,

            -- 效率指标
            ROUND(AVG(processing_days), 1) as avg_processing_days,
            ROUND(
                COUNT(CASE WHEN processing_days <= 7 THEN 1 END)::decimal / COUNT(*) * 100,
                1
            ) as fast_processing_rate_pct,

            -- 量化指标
            COUNT(*) as total_claims,
            COUNT(DISTINCT beneficiary_key) as unique_members,
            COUNT(DISTINCT provider_key) as unique_providers

        FROM {{ ref('fact_claims') }}
        GROUP BY DATE_TRUNC('month', claim_start_date)
        ORDER BY month
    )

    SELECT * FROM monthly_kpis

{% endmacro %}

{% macro generate_risk_stratification_report() %}
    /*
    生成详细的风险分层报告
    */

    WITH risk_analysis AS (
        SELECT
            -- 风险分层
            risk_tier,
            COUNT(*) as member_count,
            ROUND(COUNT(*)::decimal / SUM(COUNT(*)) OVER() * 100, 1) as pct_of_population,

            -- 成本指标
            ROUND(SUM(total_cost), 2) as total_medical_cost,
            ROUND(AVG(total_cost), 2) as avg_cost_per_member,
            ROUND(SUM(total_cost) / SUM(SUM(total_cost)) OVER() * 100, 1) as pct_of_total_cost,

            -- 利用率指标
            ROUND(AVG(total_claims), 1) as avg_claims_per_member,
            ROUND(AVG(inpatient_claims), 1) as avg_inpatient_claims,
            ROUND(AVG(chronic_condition_count), 1) as avg_chronic_conditions,

            -- 护理管理指标
            COUNT(CASE WHEN needs_case_management THEN 1 END) as needs_case_management,
            COUNT(CASE WHEN frequent_admissions THEN 1 END) as frequent_admissions,
            COUNT(CASE WHEN high_cost_member THEN 1 END) as high_cost_members,

            -- 风险评分
            ROUND(AVG(utilization_adjusted_risk_score), 2) as avg_risk_score

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

    SELECT * FROM risk_analysis

{% endmacro %}

{% macro run_all_reports() %}
    /*
    运行所有报告生成宏
    */

    {{ log("🚀 开始生成所有业务报告...", info=true) }}

    -- 生成主报告
    {{ generate_business_report() }}

    -- 生成仪表板数据
    CREATE VIEW {{ target.schema }}.executive_dashboard AS (
        {{ generate_executive_dashboard() }}
    );

    -- 生成趋势分析
    CREATE VIEW {{ target.schema }}.monthly_kpi_trends AS (
        {{ generate_monthly_kpi_trend() }}
    );

    -- 生成风险分析
    CREATE VIEW {{ target.schema }}.risk_stratification_analysis AS (
        {{ generate_risk_stratification_report() }}
    );

    {{ log("✅ 所有报告生成完成!", info=true) }}
    {{ log("📊 生成的对象:", info=true) }}
    {{ log("  - business_intelligence_report_YYYYMMDD (表)", info=true) }}
    {{ log("  - executive_dashboard (视图)", info=true) }}
    {{ log("  - monthly_kpi_trends (视图)", info=true) }}
    {{ log("  - risk_stratification_analysis (视图)", info=true) }}

{% endmacro %}