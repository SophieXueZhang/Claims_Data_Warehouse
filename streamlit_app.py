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
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Claims Data Warehouse - BI Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #3498db;
        padding-bottom: 1rem;
    }
    .metric-container {
        background: #ecf0f1;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border-left: 4px solid #3498db;
    }
    .kpi-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #27ae60;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_report_data():
    """Load the business intelligence report data"""
    try:
        report_path = Path("reports/business_report_en_2025-09-24.json")
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
    """Display executive summary metrics"""
    st.header("📈 Executive Dashboard")

    exec_data = data['executive_summary']
    metrics = exec_data['key_metrics']

    # Main KPI metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Claims",
            value=f"{metrics['total_claims']:,}",
            delta="Demo Data"
        )

    with col2:
        st.metric(
            label="Total Claim Value",
            value=f"${metrics['total_claim_value']/1000000:.0f}M",
            delta=f"Avg: ${metrics['avg_claim_amount']:,}"
        )

    with col3:
        st.metric(
            label="Denial Rate",
            value=f"{metrics['overall_denial_rate']:.1%}",
            delta="Industry Leading",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            label="Processing Days",
            value=f"{metrics['avg_processing_days']:.1f}",
            delta="Average"
        )

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
            color_discrete_sequence=['#27ae60', '#2ecc71', '#f39c12', '#e74c3c']
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
                marker_color=['#e74c3c', '#f39c12', '#27ae60'],
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

    col1, col2 = st.columns(2)

    with col1:
        # Claims volume trend
        fig_volume = px.line(
            df_trends,
            x='month',
            y='claims',
            title='Monthly Claims Volume',
            markers=True
        )
        fig_volume.update_layout(height=400)
        st.plotly_chart(fig_volume, use_container_width=True)

    with col2:
        # Denial rate trend
        fig_denial = px.line(
            df_trends,
            x='month',
            y='denial_rate',
            title='Monthly Denial Rate',
            markers=True
        )
        fig_denial.update_yaxis(tickformat='.1%')
        fig_denial.update_layout(height=400)
        st.plotly_chart(fig_denial, use_container_width=True)

    # Seasonal insights
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.subheader("🔍 Seasonal Insights")
    st.write("**Peak Volume:** March shows highest claims volume with enhanced processing efficiency")
    st.write("**Quality Consistency:** Denial rates remain stable across all months (1.8% - 2.2%)")
    st.write("**Processing Trends:** Average processing time varies seasonally but stays within target range")
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
    page = st.sidebar.selectbox(
        "Choose a section:",
        [
            "Executive Summary",
            "KPI Dashboard",
            "Provider Analysis",
            "Risk Analysis",
            "Trends & Patterns",
            "Strategic Recommendations"
        ]
    )

    # Display selected section
    if page == "Executive Summary":
        display_executive_summary(data)
    elif page == "KPI Dashboard":
        display_kpi_dashboard(data)
    elif page == "Provider Analysis":
        display_provider_analysis(data)
    elif page == "Risk Analysis":
        display_risk_analysis(data)
    elif page == "Trends & Patterns":
        display_trends(data)
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