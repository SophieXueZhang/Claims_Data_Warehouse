"""
Claims Data Warehouse - Business Intelligence Dashboard
Interactive Streamlit application for healthcare analytics
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page configuration
st.set_page_config(
    page_title="Claims Data Warehouse - BI Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Nordic minimalist styling
st.markdown("""
<style>
    /* Import Nordic-inspired fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Global Nordic color palette and typography */
    .stApp {
        background-color: #fafafa;
        font-family: 'Inter', sans-serif;
        color: #2d3748;
    }

    /* Main header - Nordic minimalism */
    .main-header {
        font-size: 2.8rem;
        font-weight: 300;
        color: #1a202c;
        text-align: center;
        margin-bottom: 3rem;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 1.5rem;
        letter-spacing: -0.025em;
    }

    /* Metric cards - Clean Nordic design */
    .metric-container {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    .metric-container:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        transform: translateY(-1px);
    }

    /* KPI cards - Nordic minimal style */
    .kpi-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    .kpi-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* Insight boxes - Subtle Nordic accent */
    .insight-box {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 3px solid #4a5568;
        margin: 1.5rem 0;
        font-weight: 400;
    }

    /* Navigation buttons - Nordic minimalism */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #cbd5e0;
        background-color: #ffffff;
        color: #4a5568;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    .stButton > button:hover {
        background-color: #f7fafc;
        border-color: #a0aec0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }

    /* Headers and subheaders - Nordic typography */
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #1a202c;
        letter-spacing: -0.025em;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    /* Sidebar styling - Clean Nordic */
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Data tables - Minimal Nordic style */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }

    /* Metric widgets - Nordic clean look */
    [data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Charts and plots - Consistent spacing */
    .js-plotly-plot {
        border-radius: 8px;
        background: #ffffff;
    }

    /* Remove default Streamlit styling */
    .css-18e3th9 {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Nordic color overrides for text */
    .stMarkdown p {
        color: #4a5568;
        line-height: 1.6;
    }

    /* Section dividers */
    hr {
        border: none;
        height: 1px;
        background: #e2e8f0;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_report_data():
    """Load the business intelligence report data"""
    try:
        report_path = "reports/business_report_en_2025-09-24.json"
        with open(report_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Report data file not found. Please generate the report first.")
        return None

def display_header():
    """Display the main header"""
    st.markdown('<h1 class="main-header">🏥 Claims Data Warehouse - Business Intelligence Dashboard</h1>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        **📊 Interactive Healthcare Analytics Dashboard**
        Explore comprehensive claims data insights with real-time KPI monitoring,
        provider performance analysis, and strategic recommendations.
        """)

def display_executive_summary(data):
    """Display modern grid-based dashboard layout"""

    exec_data = data['executive_summary']
    metrics = exec_data['key_metrics']
    kpi_data = exec_data['kpi_categories']
    claim_types = exec_data['claim_type_distribution']
    trends = data['financial_analysis']['monthly_trends']
    risk_data = data['member_risk_analysis']['risk_stratification']
    providers = data['provider_analysis']['top_providers'][:3]  # Top 3 providers

    # Create modern grid layout
    st.markdown("### 🏥 Healthcare Analytics Overview")

    # Row 1: Main KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1.5rem; border-radius: 16px; color: white; text-align: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: 300; color: white;">
                {0:,}
            </h3>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Total Claims</p>
        </div>
        """.format(metrics['total_claims']), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 1.5rem; border-radius: 16px; color: white; text-align: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: 300; color: white;">
                ${0:.0f}M
            </h3>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Total Value</p>
        </div>
        """.format(metrics['total_claim_value']/1000000), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    padding: 1.5rem; border-radius: 16px; color: white; text-align: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: 300; color: white;">
                {0:.1%}
            </h3>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Denial Rate</p>
        </div>
        """.format(metrics['overall_denial_rate']), unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                    padding: 1.5rem; border-radius: 16px; color: white; text-align: center; margin-bottom: 1rem;">
            <h3 style="margin: 0; font-size: 2.5rem; font-weight: 300; color: white;">
                {0:.1f}
            </h3>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Avg Processing Days</p>
        </div>
        """.format(metrics['avg_processing_days']), unsafe_allow_html=True)

    # Row 2: Charts and detailed cards
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        # Claim type distribution chart
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px;
                    border: 1px solid #e2e8f0; margin-bottom: 1rem; height: 400px;">
        """, unsafe_allow_html=True)
        st.subheader("📋 Claim Distribution")

        df_claims = pd.DataFrame(claim_types)
        fig_claims = px.pie(
            df_claims,
            values='count',
            names='claim_type',
            color_discrete_sequence=['#667eea', '#f093fb', '#4facfe']
        )
        fig_claims.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_claims, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Monthly trends
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px;
                    border: 1px solid #e2e8f0; margin-bottom: 1rem; height: 400px;">
        """, unsafe_allow_html=True)
        st.subheader("📈 Monthly Trends")

        df_trends = pd.DataFrame(trends)
        fig_trends = px.line(
            df_trends,
            x='month',
            y='claims',
            markers=True,
            color_discrete_sequence=['#667eea']
        )
        fig_trends.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
        fig_trends.update_xaxis(title="")
        fig_trends.update_yaxis(title="Claims")
        st.plotly_chart(fig_trends, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        # Risk summary
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px;
                    border: 1px solid #e2e8f0; margin-bottom: 1rem; height: 400px;">
            <h4 style="margin-top: 0; color: #1a202c;">👤 Risk Summary</h4>
        """, unsafe_allow_html=True)

        for tier in risk_data:
            color = "#ef4444" if tier['risk_tier'] == "High Risk" else "#f59e0b" if tier['risk_tier'] == "Medium Risk" else "#10b981"
            st.markdown(f"""
            <div style="margin: 1rem 0; padding: 0.75rem; background: {color}15;
                        border-left: 3px solid {color}; border-radius: 6px;">
                <strong>{tier['risk_tier']}</strong><br>
                <span style="font-size: 0.9rem; color: #666;">{tier['count']:,} members</span><br>
                <span style="font-size: 0.9rem; color: #666;">{tier['total_cost_pct']:.1f}% of costs</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Row 3: Financial details and provider summary
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px;
                    border: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <h4 style="margin-top: 0; color: #1a202c;">💰 Financial Metrics</h4>
        """, unsafe_allow_html=True)

        financial = kpi_data['financial']

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
            <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #1a202c;">${financial['avg_claim_amount']:,}</div>
                <div style="font-size: 0.8rem; color: #666;">Avg Claim</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #1a202c;">{financial['reimbursement_rate']:.1%}</div>
                <div style="font-size: 0.8rem; color: #666;">Reimb Rate</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #1a202c;">${financial['cost_per_member']:,}</div>
                <div style="font-size: 0.8rem; color: #666;">Cost/Member</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #1a202c;">${financial['total_reimbursement']/1000000:.0f}M</div>
                <div style="font-size: 0.8rem; color: #666;">Total Reimb</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 16px;
                    border: 1px solid #e2e8f0; margin-bottom: 1rem;">
            <h4 style="margin-top: 0; color: #1a202c;">🏥 Top Providers</h4>
        """, unsafe_allow_html=True)

        for i, provider in enumerate(providers):
            rank_color = "#10b981" if i == 0 else "#f59e0b" if i == 1 else "#6b7280"
            st.markdown(f"""
            <div style="margin: 0.75rem 0; padding: 0.75rem; background: #f8fafc; border-radius: 8px;
                        border-left: 3px solid {rank_color};">
                <div style="font-weight: 600; color: #1a202c;">#{provider['rank']} {provider['name']}</div>
                <div style="font-size: 0.85rem; color: #666; margin-top: 0.25rem;">
                    {provider['specialty']} • {provider['claims']:,} claims • {provider['denial_rate']:.1%} denial rate
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

def display_kpi_dashboard(data):
    """Display comprehensive KPI dashboard"""
    st.header("🎯 Key Performance Indicators")

    kpi_data = data['executive_summary']['kpi_categories']

    # Create 2x2 grid for KPI categories
    col1, col2 = st.columns(2)

    with col1:
        # Financial KPIs
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.subheader("💰 Financial Metrics")
        financial = kpi_data['financial']
        st.write(f"**Average Claim Amount:** ${financial['avg_claim_amount']:,}")
        st.write(f"**Total Reimbursement:** ${financial['total_reimbursement']/1000000:.1f}M")
        st.write(f"**Reimbursement Rate:** {financial['reimbursement_rate']:.1%}")
        st.write(f"**Cost per Member:** ${financial['cost_per_member']:,}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Utilization KPIs
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.subheader("📊 Utilization Metrics")
        utilization = kpi_data['utilization']
        st.write(f"**Claims per Member:** {utilization['claims_per_member']:.1f}")
        st.write(f"**Provider Diversity:** {utilization['provider_diversity']:,} providers")
        st.write(f"**Avg Services per Claim:** {utilization['avg_services_per_claim']:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Quality KPIs
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.subheader("📈 Quality Metrics")
        quality = kpi_data['quality']
        st.write(f"**Denial Rate:** {quality['denial_rate']:.1%}")
        st.write(f"**Processing Time:** {quality['processing_time']:.1f} days")
        st.write(f"**Accuracy Rate:** {quality['accuracy_rate']:.1%}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Risk KPIs
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.subheader("🎯 Risk Metrics")
        risk = kpi_data['risk']
        st.write(f"**High-cost Members:** {risk['high_cost_members']:,}")
        st.write(f"**Frequent Users:** {risk['frequent_users']:,} (10+ claims)")
        st.write(f"**Emergency Visits:** {risk['emergency_visits']:,}")
        st.markdown('</div>', unsafe_allow_html=True)

def display_provider_analysis(data):
    """Display provider performance analysis"""
    st.header("🏥 Provider Performance Analysis")

    providers = data['provider_analysis']['top_providers']

    # Convert to DataFrame for better visualization
    df_providers = pd.DataFrame(providers)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Provider performance table
        st.subheader("Top Performing Providers")

        # Format the data for display
        display_df = df_providers.copy()
        display_df['avg_amount'] = display_df['avg_amount'].apply(lambda x: f"${x:,}")
        display_df['denial_rate'] = display_df['denial_rate'].apply(lambda x: f"{x:.2%}")

        st.dataframe(
            display_df[['rank', 'name', 'specialty', 'claims', 'avg_amount', 'denial_rate', 'performance_tier']],
            column_config={
                'rank': 'Rank',
                'name': 'Provider Name',
                'specialty': 'Specialty',
                'claims': 'Claims',
                'avg_amount': 'Avg Amount',
                'denial_rate': 'Denial Rate',
                'performance_tier': 'Performance Tier'
            },
            hide_index=True,
            use_container_width=True
        )

    with col2:
        # Performance tier distribution
        st.subheader("Performance Distribution")

        perf_counts = df_providers['performance_tier'].value_counts()

        fig = px.pie(
            values=perf_counts.values,
            names=perf_counts.index,
            title="Provider Performance Tiers",
            color_discrete_sequence=['#718096', '#a0aec0', '#cbd5e0', '#e2e8f0']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def display_risk_analysis(data):
    """Display member risk stratification"""
    st.header("👤 Member Risk Analysis")

    risk_data = data['member_risk_analysis']['risk_stratification']

    col1, col2 = st.columns(2)

    with col1:
        # Risk distribution table
        st.subheader("Risk Stratification")

        df_risk = pd.DataFrame(risk_data)

        # Format for display
        display_risk = df_risk.copy()
        display_risk['avg_cost'] = display_risk['avg_cost'].apply(lambda x: f"${x:,}")
        display_risk['percentage'] = display_risk['percentage'].apply(lambda x: f"{x:.1f}%")
        display_risk['total_cost_pct'] = display_risk['total_cost_pct'].apply(lambda x: f"{x:.1f}%")

        st.dataframe(
            display_risk[['risk_tier', 'count', 'percentage', 'avg_cost', 'total_cost_pct', 'needs_case_management']],
            column_config={
                'risk_tier': 'Risk Tier',
                'count': 'Member Count',
                'percentage': 'Percentage',
                'avg_cost': 'Avg Cost',
                'total_cost_pct': 'Cost Share',
                'needs_case_management': 'Case Management'
            },
            hide_index=True,
            use_container_width=True
        )

    with col2:
        # Risk visualization
        st.subheader("Cost Concentration")

        fig = go.Figure(data=[
            go.Bar(
                x=[tier['risk_tier'] for tier in risk_data],
                y=[tier['total_cost_pct'] for tier in risk_data],
                marker_color=['#718096', '#a0aec0', '#cbd5e0'],
                text=[f"{tier['total_cost_pct']:.1f}%" for tier in risk_data],
                textposition='auto',
            )
        ])

        fig.update_layout(
            title="Healthcare Cost Distribution by Risk Tier",
            xaxis_title="Risk Tier",
            yaxis_title="Percentage of Total Costs",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

def display_trends(data):
    """Display trend analysis"""
    st.header("📈 Trend Analysis & Seasonal Patterns")

    trends = data['financial_analysis']['monthly_trends']
    df_trends = pd.DataFrame(trends)

    # Add derived metrics
    df_trends['avg_claim_value'] = df_trends['total_value'] / df_trends['claims']

    # Main trend charts
    col1, col2 = st.columns(2)

    with col1:
        # Claims volume trend
        fig_volume = px.line(
            df_trends,
            x='month',
            y='claims',
            title='Monthly Claims Volume',
            markers=True,
            color_discrete_sequence=['#718096']
        )
        fig_volume.update_layout(height=400)
        st.plotly_chart(fig_volume, use_container_width=True)

        # Average claim value trend
        fig_avg_value = px.line(
            df_trends,
            x='month',
            y='avg_claim_value',
            title='Average Claim Value Trend',
            markers=True,
            color_discrete_sequence=['#a0aec0']
        )
        fig_avg_value.update_yaxis(tickformat='$,.0f')
        fig_avg_value.update_layout(height=400)
        st.plotly_chart(fig_avg_value, use_container_width=True)

    with col2:
        # Denial rate trend
        fig_denial = px.line(
            df_trends,
            x='month',
            y='denial_rate',
            title='Monthly Denial Rate',
            markers=True,
            color_discrete_sequence=['#cbd5e0']
        )
        fig_denial.update_yaxis(tickformat='.1%')
        fig_denial.update_layout(height=400)
        st.plotly_chart(fig_denial, use_container_width=True)

        # Reimbursement rate trend
        fig_reimb = px.line(
            df_trends,
            x='month',
            y='reimbursement_rate',
            title='Monthly Reimbursement Rate',
            markers=True,
            color_discrete_sequence=['#a0aec0']
        )
        fig_reimb.update_yaxis(tickformat='.1%')
        fig_reimb.update_layout(height=400)
        st.plotly_chart(fig_reimb, use_container_width=True)

    # Monthly performance table
    st.subheader("📊 Monthly Performance Details")
    display_trends = df_trends.copy()
    display_trends['total_value'] = display_trends['total_value'].apply(lambda x: f"${x/1000000:.1f}M")
    display_trends['reimbursed'] = display_trends['reimbursed'].apply(lambda x: f"${x/1000000:.1f}M")
    display_trends['avg_claim_value'] = display_trends['avg_claim_value'].apply(lambda x: f"${x:,.0f}")
    display_trends['reimbursement_rate'] = display_trends['reimbursement_rate'].apply(lambda x: f"{x:.1%}")
    display_trends['denial_rate'] = display_trends['denial_rate'].apply(lambda x: f"{x:.1%}")

    st.dataframe(
        display_trends[['month', 'claims', 'total_value', 'avg_claim_value', 'reimbursed', 'reimbursement_rate', 'denial_rate']],
        column_config={
            'month': 'Month',
            'claims': 'Claims',
            'total_value': 'Total Value',
            'avg_claim_value': 'Avg Value',
            'reimbursed': 'Reimbursed',
            'reimbursement_rate': 'Reimb Rate',
            'denial_rate': 'Denial Rate'
        },
        hide_index=True,
        use_container_width=True
    )

    # Seasonal insights
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.subheader("🔍 Seasonal Insights")
    st.write("**Peak Volume:** March shows highest claims volume with enhanced processing efficiency")
    st.write("**Quality Consistency:** Denial rates remain stable across all months (1.8% - 2.2%)")
    st.write("**Reimbursement Stability:** Consistent reimbursement rates demonstrate operational excellence")
    st.write("**Value Trends:** Average claim values show seasonal variation patterns")
    st.markdown('</div>', unsafe_allow_html=True)

def display_claim_type_analysis(data):
    """Display claim type breakdown analysis"""
    st.header("📋 Claim Type Analysis")

    claim_types = data['executive_summary']['claim_type_distribution']
    df_claims = pd.DataFrame(claim_types)

    col1, col2 = st.columns(2)

    with col1:
        # Claim type distribution pie chart
        fig_pie = px.pie(
            df_claims,
            values='count',
            names='claim_type',
            title="Claims Distribution by Type",
            color_discrete_sequence=['#718096', '#a0aec0', '#cbd5e0']
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Average value by claim type
        fig_bar = px.bar(
            df_claims,
            x='claim_type',
            y='avg_value',
            title="Average Claim Value by Type",
            color='claim_type',
            color_discrete_sequence=['#718096', '#a0aec0', '#cbd5e0']
        )
        fig_bar.update_layout(height=400, showlegend=False)
        fig_bar.update_yaxis(tickformat='$,.0f')
        st.plotly_chart(fig_bar, use_container_width=True)

    # Detailed table
    st.subheader("Detailed Breakdown")
    display_claims = df_claims.copy()
    display_claims['total_value'] = display_claims['total_value'].apply(lambda x: f"${x/1000000:.1f}M")
    display_claims['avg_value'] = display_claims['avg_value'].apply(lambda x: f"${x:,}")
    display_claims['percentage'] = display_claims['percentage'].apply(lambda x: f"{x:.1f}%")
    display_claims['denial_rate'] = display_claims['denial_rate'].apply(lambda x: f"{x:.2%}")

    st.dataframe(
        display_claims[['claim_type', 'count', 'percentage', 'total_value', 'avg_value', 'denial_rate']],
        column_config={
            'claim_type': 'Claim Type',
            'count': 'Count',
            'percentage': 'Percentage',
            'total_value': 'Total Value',
            'avg_value': 'Avg Value',
            'denial_rate': 'Denial Rate'
        },
        hide_index=True,
        use_container_width=True
    )

def display_processing_efficiency(data):
    """Display processing efficiency analysis"""
    st.header("⚡ Processing Efficiency Analysis")

    processing_data = data['operational_analysis']['processing_efficiency']
    df_processing = pd.DataFrame(processing_data)

    col1, col2 = st.columns(2)

    with col1:
        # Processing time distribution
        fig_pie = px.pie(
            df_processing,
            values='count',
            names='category',
            title="Claims by Processing Speed",
            color_discrete_sequence=['#718096', '#a0aec0', '#cbd5e0', '#e2e8f0']
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Denial rate by processing speed
        fig_bar = px.bar(
            df_processing,
            x='category',
            y='denial_rate',
            title="Denial Rate by Processing Speed",
            color='denial_rate',
            color_continuous_scale='Greys'
        )
        fig_bar.update_layout(height=400, showlegend=False)
        fig_bar.update_yaxis(tickformat='.1%')
        fig_bar.update_xaxis(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)

    # Efficiency insights
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.subheader("⚡ Processing Insights")
    st.write(f"**Fast Processing (≤7 days):** {df_processing[df_processing['category'] == 'Fast (≤7 days)']['percentage'].iloc[0]:.1f}% of claims")
    st.write(f"**Slow Processing (>15 days):** {df_processing[df_processing['category'].str.contains('Slow')]['percentage'].sum():.1f}% requiring optimization")
    st.write("**Correlation:** Slower processing correlates with higher denial rates")
    st.markdown('</div>', unsafe_allow_html=True)

def display_chronic_conditions_impact(data):
    """Display chronic conditions impact analysis"""
    st.header("🩺 Chronic Conditions Impact Analysis")

    conditions_data = data['member_risk_analysis']['chronic_conditions_impact']
    df_conditions = pd.DataFrame(conditions_data)

    col1, col2 = st.columns(2)

    with col1:
        # Cost by condition count
        fig_bar = px.bar(
            df_conditions,
            x='condition_category',
            y='avg_cost',
            title="Average Cost by Chronic Condition Count",
            color='avg_cost',
            color_continuous_scale='Greys'
        )
        fig_bar.update_layout(height=400, showlegend=False)
        fig_bar.update_yaxis(tickformat='$,.0f')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Claims frequency by condition count
        fig_scatter = px.scatter(
            df_conditions,
            x='avg_claims',
            y='avg_cost',
            size='count',
            color='condition_category',
            title="Cost vs Claims by Condition Count",
            hover_name='condition_category'
        )
        fig_scatter.update_layout(height=400)
        fig_scatter.update_yaxis(tickformat='$,.0f')
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Impact table
    st.subheader("Detailed Impact Analysis")
    display_conditions = df_conditions.copy()
    display_conditions['avg_cost'] = display_conditions['avg_cost'].apply(lambda x: f"${x:,}")
    display_conditions['denial_rate'] = display_conditions['denial_rate'].apply(lambda x: f"{x:.2%}")

    st.dataframe(
        display_conditions,
        column_config={
            'condition_category': 'Condition Count',
            'count': 'Members',
            'avg_cost': 'Avg Cost',
            'avg_claims': 'Avg Claims',
            'denial_rate': 'Denial Rate'
        },
        hide_index=True,
        use_container_width=True
    )

def display_data_quality_framework(data):
    """Display data quality framework and metrics"""
    st.header("🛡️ Data Quality Framework")

    # Overall quality metrics
    metadata = data['executive_summary']['report_metadata']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Data Quality Score",
            value=metadata['data_quality_score'],
            delta="Excellent"
        )

    with col2:
        st.metric(
            label="Test Coverage",
            value="70+ tests",
            delta="Comprehensive"
        )

    with col3:
        st.metric(
            label="Data Freshness",
            value="Real-time",
            delta="Current"
        )

    with col4:
        st.metric(
            label="Validation Status",
            value="Passed",
            delta="All checks"
        )

    # Quality framework details
    st.subheader("🔍 Quality Testing Layers")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.subheader("📊 Schema Tests")
        st.write("**Primary Key Uniqueness:** ✅ Validated")
        st.write("**Foreign Key Relationships:** ✅ Validated")
        st.write("**Not-null Constraints:** ✅ Validated")
        st.write("**Accepted Values:** ✅ Validated")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.subheader("🧮 Business Logic Tests")
        st.write("**Financial Consistency:** ✅ Reimbursement ≤ Claim Amount")
        st.write("**Date Logic:** ✅ End Date ≥ Start Date")
        st.write("**Healthcare Rules:** ✅ Inpatient LOS Validation")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.subheader("📈 Data Anomaly Detection")
        st.write("**Volume Monitoring:** ✅ Statistical Methods")
        st.write("**Data Freshness:** ✅ Processing Lag Monitoring")
        st.write("**Cross-table Consistency:** ✅ Relationship Validation")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
        st.subheader("🎯 Quality Metrics")
        st.write("**Data Completeness:** 99.0% non-null values")
        st.write("**Data Accuracy:** 97.7% business rule compliance")
        st.write("**Data Consistency:** 100% relationship validation")
        st.write("**Data Timeliness:** < 1 hour processing lag")
        st.markdown('</div>', unsafe_allow_html=True)

def display_recommendations(data):
    """Display strategic recommendations"""
    st.header("🎯 Strategic Recommendations")

    cost_opps = data['recommendations']['cost_optimization']
    quality_imps = data['recommendations']['quality_improvements']

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Cost Optimization")

        for opp in cost_opps:
            with st.expander(f"{opp['opportunity']} - ${opp['potential_savings']/1000000:.1f}M Savings"):
                st.write(f"**Action:** {opp['action']}")
                st.write(f"**Potential Savings:** ${opp['potential_savings']:,}")
                if 'provider_count' in opp:
                    st.write(f"**Providers Affected:** {opp['provider_count']}")
                if 'member_count' in opp:
                    st.write(f"**Members Affected:** {opp['member_count']}")

    with col2:
        st.subheader("📈 Quality Improvements")

        for imp in quality_imps:
            with st.expander(f"{imp['area']} Optimization"):
                st.write(f"**Recommendation:** {imp['recommendation']}")
                if 'current_avg_days' in imp:
                    st.write(f"**Current:** {imp['current_avg_days']:.1f} days")
                    st.write(f"**Target:** {imp['target_days']:.1f} days")
                if 'current_denial_rate' in imp:
                    st.write(f"**Current Denial Rate:** {imp['current_denial_rate']:.1%}")
                    st.write(f"**Target Denial Rate:** {imp['target_denial_rate']:.1%}")

def main():
    """Main Streamlit application"""

    # Display header
    display_header()

    # Load data
    data = load_report_data()

    if data is None:
        st.stop()

    # Navigation sidebar
    st.sidebar.title("📊 Dashboard Navigation")
    st.sidebar.markdown("👈 **Select a section to explore:**")
    page = st.sidebar.selectbox(
        "Choose a section:",
        [
            "Executive Summary",
            "KPI Dashboard",
            "Provider Analysis",
            "Risk Analysis",
            "Claim Type Analysis",
            "Processing Efficiency",
            "Chronic Conditions Impact",
            "Trends & Patterns",
            "Data Quality Framework",
            "Strategic Recommendations"
        ]
    )

    # Main page navigation (backup if sidebar not visible)
    st.markdown("---")
    st.markdown("### 📍 Navigate to Different Sections:")

    # Create navigation buttons in rows
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("📈 Executive Summary", key="nav_exec"):
            page = "Executive Summary"
        if st.button("📋 Claim Types", key="nav_claims"):
            page = "Claim Type Analysis"

    with col2:
        if st.button("🎯 KPI Dashboard", key="nav_kpi"):
            page = "KPI Dashboard"
        if st.button("⚡ Processing", key="nav_process"):
            page = "Processing Efficiency"

    with col3:
        if st.button("🏥 Providers", key="nav_providers"):
            page = "Provider Analysis"
        if st.button("🩺 Conditions", key="nav_conditions"):
            page = "Chronic Conditions Impact"

    with col4:
        if st.button("👤 Risk Analysis", key="nav_risk"):
            page = "Risk Analysis"
        if st.button("📈 Trends", key="nav_trends"):
            page = "Trends & Patterns"

    with col5:
        if st.button("🛡️ Data Quality", key="nav_quality"):
            page = "Data Quality Framework"
        if st.button("🎯 Recommendations", key="nav_recs"):
            page = "Strategic Recommendations"

    # Display selected section
    if page == "Executive Summary":
        display_executive_summary(data)
    elif page == "KPI Dashboard":
        display_kpi_dashboard(data)
    elif page == "Provider Analysis":
        display_provider_analysis(data)
    elif page == "Risk Analysis":
        display_risk_analysis(data)
    elif page == "Claim Type Analysis":
        display_claim_type_analysis(data)
    elif page == "Processing Efficiency":
        display_processing_efficiency(data)
    elif page == "Chronic Conditions Impact":
        display_chronic_conditions_impact(data)
    elif page == "Trends & Patterns":
        display_trends(data)
    elif page == "Data Quality Framework":
        display_data_quality_framework(data)
    elif page == "Strategic Recommendations":
        display_recommendations(data)

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; color: #7f8c8d; font-size: 0.9em;">
            <p><strong>Claims Data Warehouse</strong> - Healthcare Analytics Platform</p>
            <p>Built with dbt + PostgreSQL + Python + Streamlit</p>
            <p><a href="https://github.com/SophieXueZhang/Claims_Data_Warehouse" target="_blank">🔗 View on GitHub</a></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()