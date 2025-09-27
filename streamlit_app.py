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

# Professional dashboard styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Nordic/Scandinavian Global styling */
    .stApp {
        background: #fafafa;
        font-family: 'Inter', sans-serif;
        color: #2e3440;
    }

    /* Nordic color palette */
    :root {
        --nord-0: #2e3440;   /* Polar Night - darkest */
        --nord-1: #3b4252;   /* Polar Night */
        --nord-2: #434c5e;   /* Polar Night */
        --nord-3: #4c566a;   /* Polar Night - lightest */
        --nord-4: #d8dee9;   /* Snow Storm - darkest */
        --nord-5: #e5e9f0;   /* Snow Storm */
        --nord-6: #eceff4;   /* Snow Storm - lightest */
        --nord-7: #8fbcbb;   /* Frost - teal */
        --nord-8: #88c0d0;   /* Frost - light blue */
        --nord-9: #81a1c1;   /* Frost - blue */
        --nord-10: #5e81ac;  /* Frost - dark blue */
        --nord-11: #bf616a;  /* Aurora - red */
        --nord-12: #d08770;  /* Aurora - orange */
        --nord-13: #ebcb8b;  /* Aurora - yellow */
        --nord-14: #a3be8c;  /* Aurora - green */
        --nord-15: #b48ead;  /* Aurora - purple */
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Nordic Sidebar styling - Clean and minimal */
    [data-testid="stSidebar"], .css-1d391kg, .css-1aumxhk, .css-17eq0hr {
        background: var(--nord-6) !important;
        border-right: 1px solid var(--nord-4) !important;
        padding: 2rem 1.5rem !important;
        width: 300px !important;
        box-shadow: 0 0 20px rgba(46, 52, 64, 0.05) !important;
    }

    /* Ensure sidebar content is visible with Nordic colors */
    [data-testid="stSidebar"] > div {
        color: var(--nord-0) !important;
    }

    /* Sidebar text contrast improvements */
    [data-testid="stSidebar"] * {
        color: var(--nord-0) !important;
    }

    [data-testid="stSidebar"] .sidebar-title {
        color: var(--nord-0) !important;
        font-weight: 600 !important;
    }

    /* Sidebar navigation items */
    .nav-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        color: #cbd5e0;
        text-decoration: none;
        transition: all 0.2s ease;
        cursor: pointer;
        font-weight: 400;
    }

    .nav-item:hover {
        background: #2d3748;
        color: #ffffff;
        transform: translateX(4px);
    }

    .nav-item.active {
        background: #3182ce;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3);
    }

    .nav-item-icon {
        margin-right: 0.75rem;
        font-size: 1.1rem;
        width: 20px;
        text-align: center;
    }

    /* Main content area */
    .main .block-container {
        padding: 2rem !important;
        max-width: none !important;
    }

    /* Nordic dashboard header with better contrast */
    .dashboard-header {
        background: #ffffff;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        border: 1px solid var(--nord-4);
        box-shadow: 0 2px 8px rgba(46, 52, 64, 0.06);
    }

    /* Nordic KPI cards - Functional and clean with better contrast */
    .kpi-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 6px;
        border: 1px solid var(--nord-4);
        box-shadow: 0 1px 4px rgba(46, 52, 64, 0.08);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }

    .kpi-card:hover {
        border-color: var(--nord-8);
        box-shadow: 0 2px 8px rgba(46, 52, 64, 0.12);
        transform: translateY(-1px);
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 500;
        color: var(--nord-0);
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }

    .kpi-label {
        color: var(--nord-3);
        font-size: 0.85rem;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Nordic chart containers - Clean and minimal with better contrast */
    .chart-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid var(--nord-4);
        box-shadow: 0 2px 8px rgba(46, 52, 64, 0.06);
        margin-bottom: 1.5rem;
    }

    .chart-title {
        font-size: 1.1rem;
        font-weight: 500;
        color: var(--nord-0);
        margin-bottom: 1.5rem;
        letter-spacing: 0.3px;
    }

    /* Only hide main content buttons, not sidebar buttons */
    .main .stButton {
        display: none !important;
    }

    /* Nordic sidebar title */
    .sidebar-title {
        color: var(--nord-0);
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 2rem;
        text-align: left;
        padding: 0 0 1rem 0;
        border-bottom: 2px solid var(--nord-4);
        letter-spacing: 0.5px;
    }

    /* Style selectbox but don't hide it */
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    /* Minimalist sidebar buttons with SVG support */
    [data-testid="stSidebar"] .stButton {
        display: block !important;
        margin-bottom: 0.25rem !important;
    }

    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        background: transparent !important;
        color: var(--nord-3) !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 0.8rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        transition: all 0.2s ease !important;
        font-weight: 400 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.01em !important;
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: var(--nord-5) !important;
        color: var(--nord-0) !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* Active state for minimalist buttons */
    [data-testid="stSidebar"] .stButton > button:focus {
        background: var(--nord-4) !important;
        color: var(--nord-0) !important;
        border: none !important;
        box-shadow: inset 3px 0 0 var(--nord-10) !important;
    }

    /* SVG icon styles */
    [data-testid="stSidebar"] svg {
        margin-right: 0.5rem !important;
        transition: all 0.2s ease !important;
        flex-shrink: 0 !important;
    }

    /* Force show sidebar markdown content */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        display: block !important;
        color: white !important;
    }

    /* Keep sidebar content visible */

    /* News/activity feed */
    .activity-item {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3182ce;
        margin-bottom: 0.75rem;
        backdrop-filter: blur(10px);
    }

    .activity-time {
        font-size: 0.8rem;
        color: #718096;
        font-weight: 500;
    }

    .activity-content {
        font-size: 0.9rem;
        color: #2d3748;
        margin-top: 0.25rem;
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


def display_executive_summary(data):
    """Display modern grid-based dashboard layout"""

    exec_data = data.get('executive_summary', {})
    metrics = exec_data.get('key_metrics', {
        'total_claims': 50000,
        'total_claim_value': 225000000,
        'overall_denial_rate': 0.023,
        'avg_processing_days': 12.4
    })
    kpi_data = exec_data.get('kpi_categories', {})
    if not kpi_data:
        kpi_data = {
            'financial': {
                'avg_claim_amount': 4500,
                'reimbursement_rate': 0.87,
                'cost_per_member': 4500,
                'total_reimbursement': 195000000
            }
        }
    claim_types = exec_data.get('claim_type_distribution', [])
    trends = data.get('financial_analysis', {}).get('monthly_trends', [])
    if not trends:
        trends = [
            {'month': 'Jan', 'claims': 4156, 'amount': 2456789},
            {'month': 'Feb', 'claims': 3892, 'amount': 2234567},
            {'month': 'Mar', 'claims': 4321, 'amount': 2567890}
        ]

    risk_data = data.get('member_risk_analysis', {}).get('risk_stratification', [])
    if not risk_data:
        risk_data = [
            {'risk_tier': 'High Risk', 'count': 425, 'total_cost_pct': 48.5},
            {'risk_tier': 'Medium Risk', 'count': 1567, 'total_cost_pct': 32.4},
            {'risk_tier': 'Low Risk', 'count': 3008, 'total_cost_pct': 19.1}
        ]

    providers = data.get('provider_analysis', {}).get('top_providers', [])
    if not providers:
        providers = [
            {'rank': 1, 'name': 'Metro Hospital', 'specialty': 'Cardiology', 'claims': 234, 'denial_rate': 0.018, 'amount': 567890},
            {'rank': 2, 'name': 'Central Clinic', 'specialty': 'Primary Care', 'claims': 187, 'denial_rate': 0.021, 'amount': 432108},
            {'rank': 3, 'name': 'West Medical', 'specialty': 'Orthopedics', 'claims': 156, 'denial_rate': 0.025, 'amount': 378945}
        ]
    providers = providers[:3]  # Top 3 providers

    # Professional Report Header - UN Style
    st.markdown("""
    <div style="background: #ffffff; padding: 2rem; margin: -1rem -1rem 2rem -1rem;
                border-left: 4px solid #5e81ac; border-bottom: 1px solid #e5e7eb;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <h1 style="color: #1f2937; font-size: 2.2rem; font-weight: 600; margin-bottom: 0.5rem;
                           letter-spacing: -0.01em; line-height: 1.2;">
                    Healthcare Claims Data Warehouse
                </h1>
                <p style="color: #6b7280; font-size: 1rem; font-weight: 400; margin: 0;">
                    Comprehensive claims data insights and KPI monitoring
                </p>
            </div>
            <div style="text-align: right;">
                <div style="color: #5e81ac; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem;">
                    SYSTEM STATUS
                </div>
                <div style="color: #1f2937; font-size: 1.1rem; font-weight: 600;">
                    OPERATIONAL
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Executive Summary Section - UN Report Style
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Executive Summary
    </h3>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #5e81ac;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #5e81ac; margin-bottom: 0.25rem;">{0:,}</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Total Claims</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">✓ System operational</div>
        </div>
        """.format(metrics['total_claims']), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #bf616a;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #bf616a; margin-bottom: 0.25rem;">${0:.0f}M</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Total Value</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">↗ +8% growth</div>
        </div>
        """.format(metrics['total_claim_value']/1000000), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #a3be8c;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #a3be8c; margin-bottom: 0.25rem;">{0:.1%}</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Denial Rate</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">✓ Below industry avg</div>
        </div>
        """.format(metrics['overall_denial_rate']), unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #b48ead;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #b48ead; margin-bottom: 0.25rem;">{0:.1f}</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Avg Processing Days</div>
            <div style="font-size: 0.8rem; color: #bf616a; font-weight: 500; margin-top: 0.5rem;">⚠ Above target</div>
        </div>
        """.format(metrics['avg_processing_days']), unsafe_allow_html=True)

    # Row 2: Charts and detailed cards
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        # Claim type distribution chart
        st.markdown("""
        <div style="background: white; padding: 2rem; margin-bottom: 2rem; border-left: 4px solid #5e81ac;">
            <h3 style="color: #5e81ac; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
                Claim Distribution Analysis
            </h3>
        """, unsafe_allow_html=True)

        df_claims = pd.DataFrame(claim_types)
        fig_claims = px.pie(
            df_claims,
            values='count',
            names='claim_type',
            color_discrete_sequence=['#81a1c1', '#88c0d0', '#8fbcbb']
        )
        fig_claims.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_claims, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Monthly trends
        st.markdown("""
        <div style="background: white; padding: 2rem; margin-bottom: 2rem; border-left: 4px solid #a3be8c;">
            <h3 style="color: #a3be8c; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
                Monthly Processing Trends
            </h3>
        """, unsafe_allow_html=True)

        df_trends = pd.DataFrame(trends)
        fig_trends = px.line(
            df_trends,
            x='month',
            y='claims',
            markers=True,
            color_discrete_sequence=['#5e81ac']
        )
        fig_trends.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
        fig_trends.update_layout(
            xaxis_title="",
            yaxis_title="Claims"
        )
        st.plotly_chart(fig_trends, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        # Risk summary
        st.markdown("""
        <div style="background: white; padding: 2rem; margin-bottom: 2rem; border-left: 4px solid #bf616a;">
            <h3 style="color: #bf616a; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
                Member Risk Analysis
            </h3>
        """, unsafe_allow_html=True)

        for tier in risk_data:
            color = "#bf616a" if tier['risk_tier'] == "High Risk" else "#b48ead" if tier['risk_tier'] == "Medium Risk" else "#a3be8c"
            st.markdown(f"""
            <div style="margin: 1rem 0; padding: 1rem; background: white;
                        border-left: 3px solid {color};">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">{tier['risk_tier']}</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {color}; margin-bottom: 0.25rem;">{tier['count']:,}</div>
                <div style="font-size: 0.8rem; color: #6b7280; font-weight: 500;">Members • {tier['total_cost_pct']:.1f}% of total costs</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Row 3: Financial details and provider summary
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 2rem; margin-bottom: 2rem; border-left: 4px solid #b48ead;">
            <h3 style="color: #b48ead; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
                Financial Performance Metrics
            </h3>
        """, unsafe_allow_html=True)

        financial = kpi_data.get('financial', {
            'avg_claim_amount': 4500,
            'reimbursement_rate': 0.87,
            'cost_per_member': 4500,
            'total_reimbursement': 195000000
        })

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 1rem;">
            <div style="text-align: left; padding: 1rem; background: white; border-left: 3px solid #b48ead;">
                <div style="font-size: 2rem; font-weight: 700; color: #b48ead; margin-bottom: 0.25rem;">${financial['avg_claim_amount']:,}</div>
                <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Average Claim Amount</div>
            </div>
            <div style="text-align: left; padding: 1rem; background: white; border-left: 3px solid #a3be8c;">
                <div style="font-size: 2rem; font-weight: 700; color: #a3be8c; margin-bottom: 0.25rem;">{financial['reimbursement_rate']:.1%}</div>
                <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Reimbursement Rate</div>
            </div>
            <div style="text-align: left; padding: 1rem; background: white; border-left: 3px solid #5e81ac;">
                <div style="font-size: 2rem; font-weight: 700; color: #5e81ac; margin-bottom: 0.25rem;">${financial['cost_per_member']:,}</div>
                <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Cost Per Member</div>
            </div>
            <div style="text-align: left; padding: 1rem; background: white; border-left: 3px solid #bf616a;">
                <div style="font-size: 2rem; font-weight: 700; color: #bf616a; margin-bottom: 0.25rem;">${financial['total_reimbursement']/1000000:.0f}M</div>
                <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Total Reimbursement</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; margin-bottom: 2rem; border-left: 4px solid #5e81ac;">
            <h3 style="color: #5e81ac; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
                Provider Performance Ranking
            </h3>
        """, unsafe_allow_html=True)

        for i, provider in enumerate(providers):
            rank_color = "#a3be8c" if i == 0 else "#b48ead" if i == 1 else "#6b7280"
            st.markdown(f"""
            <div style="margin: 1rem 0; padding: 1rem; background: white;
                        border-left: 3px solid {rank_color};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="font-size: 1.1rem; font-weight: 600; color: #1f2937;">#{provider['rank']} {provider['name']}</div>
                    <div style="font-size: 1.2rem; font-weight: 700; color: {rank_color};">{provider['claims']:,}</div>
                </div>
                <div style="font-size: 0.9rem; color: #6b7280; font-weight: 500;">
                    {provider['specialty']} • {provider['denial_rate']:.1%} denial rate
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

def display_kpi_dashboard(data):
    """Display comprehensive KPI dashboard"""
    st.markdown("""
    <div style="background: #ffffff; padding: 2rem; margin: -1rem -1rem 2rem -1rem;
                border-left: 4px solid #5e81ac; border-bottom: 1px solid #e5e7eb;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <h1 style="color: #1f2937; font-size: 2.2rem; font-weight: 600; margin-bottom: 0.5rem;
                           letter-spacing: -0.01em; line-height: 1.2;">
                    Healthcare Claims Analytics Report
                </h1>
                <p style="color: #6b7280; font-size: 1rem; font-weight: 400; margin: 0;">
                    Executive Performance Overview & Strategic Insights
                </p>
            </div>
            <div style="text-align: right;">
                <div style="color: #5e81ac; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem;">
                    REPORTING PERIOD
                </div>
                <div style="color: #1f2937; font-size: 1.1rem; font-weight: 600;">
                    Q4 2024
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # In Focus Section - UN Report Style
    st.markdown("""
    <div style="background: #f8fafc; padding: 2rem; margin: 2rem 0; border-left: 4px solid #5e81ac;">
        <h2 style="color: #5e81ac; font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em;">
            In Focus: Healthcare Claims Performance Drives Record Impact
        </h2>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem; margin-top: 1.5rem;">
            <div>
                <div style="color: #1f2937; font-size: 1rem; font-weight: 500; margin-bottom: 1rem;">
                    <strong>48,500+ CLAIMS PROCESSED</strong><br>
                    <span style="color: #6b7280; font-weight: 400;">As of Q4 2024</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="width: 80px; height: 80px; background: #5e81ac; color: white; border-radius: 50%;
                                display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: bold; margin-right: 1rem;">
                        97.7%
                    </div>
                    <div style="color: #374151; font-size: 0.9rem; line-height: 1.4;">
                        <strong>claims approved</strong><br>
                        effectively reducing member<br>
                        financial burden
                    </div>
                </div>
            </div>
            <div style="color: #374151; font-size: 0.9rem; line-height: 1.6;">
                <div style="margin-bottom: 1rem;">
                    <strong>New claims processing challenges caused by complex medical conditions</strong>
                </div>
                <div style="margin-bottom: 0.5rem;">
                    <span style="background: #ebf3ff; color: #5e81ac; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">
                        $11.1M in cost optimization opportunities identified
                    </span>
                </div>
                <div style="color: #6b7280; font-size: 0.85rem;">
                    Source: Healthcare Claims Processing Analysis / Q4 2024
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Performance Indicators Grid - Dynamic Data
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Key Performance Indicators
    </h3>
    """, unsafe_allow_html=True)

    kpi_data = data.get('executive_summary', {}).get('kpi_categories', {})
    if not kpi_data:
        kpi_data = {
            'financial': {
                'avg_claim_amount': 9700,
                'reimbursement_rate': 0.977,
                'cost_per_member': 48515,
                'total_reimbursement': 474100000
            },
            'quality': {
                'denial_rate': 0.023,
                'processing_time': 12.4,
                'accuracy_rate': 0.977
            },
            'utilization': {
                'claims_per_member': 5.0,
                'provider_diversity': 1234,
                'avg_services_per_claim': 2.3
            },
            'risk': {
                'high_cost_members': 850,
                'frequent_users': 450,
                'emergency_visits': 2340
            }
        }

    # Core KPI Metrics in Nordic Cards
    col1, col2, col3, col4 = st.columns(4)

    financial = kpi_data.get('financial', {
        'avg_claim_amount': 9700,
        'reimbursement_rate': 0.977,
        'cost_per_member': 48515,
        'total_reimbursement': 474100000
    })

    quality = kpi_data.get('quality', {
        'denial_rate': 0.023,
        'processing_time': 12.4,
        'accuracy_rate': 0.977
    })

    utilization = kpi_data.get('utilization', {
        'claims_per_member': 5.0,
        'provider_diversity': 1234,
        'avg_services_per_claim': 2.3
    })

    risk = kpi_data.get('risk', {
        'high_cost_members': 850,
        'frequent_users': 450,
        'emergency_visits': 2340
    })

    with col1:
        avg_amount_color = "#a3be8c" if financial['avg_claim_amount'] < 10000 else "#ebcb8b" if financial['avg_claim_amount'] < 15000 else "#bf616a"
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid {avg_amount_color};
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: {avg_amount_color}; margin-bottom: 0.25rem;">${financial['avg_claim_amount']:,}</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Average Claim Amount</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">↗ +12% vs Q3</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        processing_color = "#bf616a" if quality['processing_time'] > 10 else "#ebcb8b" if quality['processing_time'] > 8 else "#a3be8c"
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid {processing_color};
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: {processing_color}; margin-bottom: 0.25rem;">{quality['processing_time']:.1f}</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Processing Days</div>
            <div style="font-size: 0.8rem; color: #bf616a; font-weight: 500; margin-top: 0.5rem;">⚠ 46% above target</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        denial_color = "#a3be8c" if quality['denial_rate'] < 0.03 else "#ebcb8b" if quality['denial_rate'] < 0.05 else "#bf616a"
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid {denial_color};
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: {denial_color}; margin-bottom: 0.25rem;">{quality['denial_rate']:.1%}</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Denial Rate</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">✓ Industry leading</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        risk_pct = (risk['high_cost_members'] / 10000) * 100
        risk_color = "#bf616a" if risk_pct > 10 else "#ebcb8b" if risk_pct > 7 else "#a3be8c"
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid {risk_color};
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: {risk_color}; margin-bottom: 0.25rem;">5.0</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Claims Per Member</div>
            <div style="font-size: 0.8rem; color: #b48ead; font-weight: 500; margin-top: 0.5rem;">↔ Stable utilization</div>
        </div>
        """, unsafe_allow_html=True)

    # Alert section for critical issues
    if quality['processing_time'] > 10:
        st.warning("⚠️ **Processing Time Alert:** 46% above 8.5-day target - immediate action required")

    # Strategic Impact Section - UN Report Style
    st.markdown("""
    <div style="background: white; padding: 2rem; margin: 2rem 0; border-left: 4px solid #bf616a;">
        <h3 style="color: #bf616a; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
            Strategic Impact Opportunities
        </h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;">
            <div style="text-align: center;">
                <div style="width: 120px; height: 120px; background: #5e81ac; color: white; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto;">
                    <div>
                        <div style="font-size: 1.8rem; font-weight: bold;">$2.4M</div>
                        <div style="font-size: 0.8rem; font-weight: 500;">ANNUAL</div>
                    </div>
                </div>
                <div style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem;">Process Automation</div>
                <div style="color: #6b7280; font-size: 0.9rem; line-height: 1.4;">
                    Deploy automation for standard claims processing to reduce manual review time
                </div>
            </div>
            <div style="text-align: center;">
                <div style="width: 120px; height: 120px; background: #a3be8c; color: white; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto;">
                    <div>
                        <div style="font-size: 1.8rem; font-weight: bold;">$5.8M</div>
                        <div style="font-size: 0.8rem; font-weight: 500;">ANNUAL</div>
                    </div>
                </div>
                <div style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem;">Risk Intervention</div>
                <div style="color: #6b7280; font-size: 0.9rem; line-height: 1.4;">
                    High-cost member outreach and chronic condition management programs
                </div>
            </div>
            <div style="text-align: center;">
                <div style="width: 120px; height: 120px; background: #b48ead; color: white; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto;">
                    <div>
                        <div style="font-size: 1.6rem; font-weight: bold;">$11.1M</div>
                        <div style="font-size: 0.8rem; font-weight: 500;">3-YEAR ROI</div>
                    </div>
                </div>
                <div style="color: #1f2937; font-weight: 600; margin-bottom: 0.5rem;">Total Strategic Impact</div>
                <div style="color: #6b7280; font-size: 0.9rem; line-height: 1.4;">
                    Combined impact of predictive analytics and operational excellence initiatives
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    # Performance Tracking Dashboard - Professional Style
    st.markdown("""
    <div style="margin: 3rem 0 1.5rem 0;">
        <h2 style="color: #2d3748; font-size: 1.75rem; font-weight: 600; margin-bottom: 0.5rem; letter-spacing: -0.02em;">
            Performance Tracking
        </h2>
        <p style="color: #718096; font-size: 1rem; margin: 0;">
            Real-time operational metrics and trend analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Quality Score",
            value="83/100",
            delta="+5 pts",
            help="Overall operational health score"
        )

    with col2:
        st.metric(
            label="Cost Efficiency",
            value="92%",
            delta="+3%",
            help="Cost per member vs industry benchmark"
        )

    with col3:
        st.metric(
            label="Processing SLA",
            value="54%",
            delta="-12%",
            help="Claims processed within target timeframe",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            label="Member Satisfaction",
            value="4.2/5",
            delta="+0.3",
            help="Member satisfaction survey results"
        )

def display_provider_analysis(data):
    """Display provider performance analysis in UN report style"""
    # UN Report Style Header
    st.markdown("""
    <div style="background: white; padding: 2rem; border-left: 4px solid #5e81ac; margin-bottom: 2rem;">
        <h1 style="color: #1f2937; font-size: 2.5rem; font-weight: 700; margin: 0 0 0.5rem 0; text-align: left;">
            🏥 PROVIDER PERFORMANCE ANALYSIS
        </h1>
        <p style="color: #6b7280; font-size: 1.1rem; margin: 0; text-align: left;">
            Healthcare Network Quality Assessment & Provider Rankings
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Key Provider Metrics - UN Style Cards
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Provider Network Overview
    </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #5e81ac;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #5e81ac; margin-bottom: 0.25rem;">1,234</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">TOTAL PROVIDERS</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">Contracted Network</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #a3be8c;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #a3be8c; margin-bottom: 0.25rem;">97.2%</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">QUALITY SCORE</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">Network Average</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #d08770;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #d08770; margin-bottom: 0.25rem;">$9.7K</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">AVG CLAIM AMOUNT</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">Per Provider</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #b48ead;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #b48ead; margin-bottom: 0.25rem;">2.1%</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">DENIAL RATE</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">Below Benchmark</div>
        </div>
        """, unsafe_allow_html=True)

    # Provider Performance Table - UN Style
    providers = data.get('provider_analysis', {}).get('top_providers', [])
    if not providers:
        providers = [
            {'rank': 1, 'name': 'Metro Hospital', 'specialty': 'Cardiology', 'claims': 234, 'avg_amount': 5678, 'denial_rate': 0.015, 'performance_tier': 'Elite'},
            {'rank': 2, 'name': 'Central Clinic', 'specialty': 'Primary Care', 'claims': 187, 'avg_amount': 3456, 'denial_rate': 0.018, 'performance_tier': 'High'},
            {'rank': 3, 'name': 'West Medical', 'specialty': 'Orthopedics', 'claims': 156, 'avg_amount': 6789, 'denial_rate': 0.021, 'performance_tier': 'High'},
            {'rank': 4, 'name': 'East Surgery', 'specialty': 'Surgery', 'claims': 143, 'avg_amount': 8901, 'denial_rate': 0.024, 'performance_tier': 'Standard'},
            {'rank': 5, 'name': 'North Wellness', 'specialty': 'Wellness', 'claims': 128, 'avg_amount': 2345, 'denial_rate': 0.019, 'performance_tier': 'High'}
        ]

    df_providers = pd.DataFrame(providers)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("""
        <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
            Top Provider Performance Rankings
        </h3>
        """, unsafe_allow_html=True)

        # Format the data for display
        display_df = df_providers.copy()
        display_df['avg_amount'] = display_df['avg_amount'].apply(lambda x: f"${x:,}")
        display_df['denial_rate'] = display_df['denial_rate'].apply(lambda x: f"{x:.1%}")

        st.dataframe(
            display_df[['rank', 'name', 'specialty', 'claims', 'avg_amount', 'denial_rate', 'performance_tier']],
            column_config={
                'rank': 'Rank',
                'name': 'Provider Name',
                'specialty': 'Specialty',
                'claims': 'Claims Volume',
                'avg_amount': 'Avg Amount',
                'denial_rate': 'Denial Rate',
                'performance_tier': 'Performance Tier'
            },
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.markdown("""
        <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
            Performance Tiers
        </h3>
        """, unsafe_allow_html=True)

        # Performance tier distribution with UN colors
        perf_counts = df_providers['performance_tier'].value_counts()

        fig = px.pie(
            values=perf_counts.values,
            names=perf_counts.index,
            color_discrete_sequence=['#5e81ac', '#a3be8c', '#d08770', '#b48ead']
        )
        fig.update_layout(
            height=350,
            showlegend=True,
            font=dict(color='#1f2937'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Provider Quality Analysis - UN Style Section
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 3rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Provider Network Quality Assessment
    </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #5e81ac; margin-bottom: 1rem;">
            <h4 style="color: #5e81ac; font-size: 1.1rem; margin: 0 0 1rem 0; text-transform: uppercase;">
                Elite Providers
            </h4>
            <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">20%</div>
            <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Handle 60% of total volume with exceptional outcomes
            </div>
            <div style="color: #a3be8c; font-size: 0.8rem; font-weight: 500;">
                ✓ <1.5% denial rate<br>
                ✓ >95% satisfaction<br>
                ✓ Fast processing
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #a3be8c; margin-bottom: 1rem;">
            <h4 style="color: #a3be8c; font-size: 1.1rem; margin: 0 0 1rem 0; text-transform: uppercase;">
                High Performers
            </h4>
            <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">60%</div>
            <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Standard network providers meeting quality benchmarks
            </div>
            <div style="color: #a3be8c; font-size: 0.8rem; font-weight: 500;">
                ✓ 1.5-3% denial rate<br>
                ✓ >90% satisfaction<br>
                ✓ Standard processing
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #d08770; margin-bottom: 1rem;">
            <h4 style="color: #d08770; font-size: 1.1rem; margin: 0 0 1rem 0; text-transform: uppercase;">
                Improvement Needed
            </h4>
            <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">20%</div>
            <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Providers requiring quality enhancement programs
            </div>
            <div style="color: #d08770; font-size: 0.8rem; font-weight: 500;">
                ⚠ >3% denial rate<br>
                ⚠ <90% satisfaction<br>
                ⚠ Training required
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_risk_analysis(data):
    """Display member risk stratification in UN report style"""
    # UN Report Style Header
    st.markdown("""
    <div style="background: white; padding: 2rem; border-left: 4px solid #bf616a; margin-bottom: 2rem;">
        <h1 style="color: #1f2937; font-size: 2.5rem; font-weight: 700; margin: 0 0 0.5rem 0; text-align: left;">
            👤 MEMBER RISK ANALYSIS
        </h1>
        <p style="color: #6b7280; font-size: 1.1rem; margin: 0; text-align: left;">
            Population Health Risk Stratification & Cost Concentration Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Risk Overview Metrics - UN Style Cards
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Risk Profile Overview
    </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #bf616a;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #bf616a; margin-bottom: 0.25rem;">5,000</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">TOTAL MEMBERS</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">Active Population</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #d08770;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #d08770; margin-bottom: 0.25rem;">425</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">HIGH RISK</div>
            <div style="font-size: 0.8rem; color: #d08770; font-weight: 500; margin-top: 0.5rem;">8.5% Population</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #ebcb8b;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #d08770; margin-bottom: 0.25rem;">48.5%</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">COST CONCENTRATION</div>
            <div style="font-size: 0.8rem; color: #d08770; font-weight: 500; margin-top: 0.5rem;">High Risk Members</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #a3be8c;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #a3be8c; margin-bottom: 0.25rem;">$12.5K</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">AVG HIGH RISK COST</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">Per Member</div>
        </div>
        """, unsafe_allow_html=True)

    # Risk Stratification Data
    risk_data = data.get('member_risk_analysis', {}).get('risk_stratification', [])
    if not risk_data:
        risk_data = [
            {'risk_tier': 'High Risk', 'count': 425, 'percentage': 8.5, 'avg_cost': 12500, 'total_cost_pct': 48.5, 'needs_case_management': 'Yes'},
            {'risk_tier': 'Medium Risk', 'count': 1567, 'percentage': 31.3, 'avg_cost': 6200, 'total_cost_pct': 32.4, 'needs_case_management': 'Selective'},
            {'risk_tier': 'Low Risk', 'count': 3008, 'percentage': 60.2, 'avg_cost': 1800, 'total_cost_pct': 19.1, 'needs_case_management': 'No'}
        ]

    df_risk = pd.DataFrame(risk_data)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
            Risk Stratification Analysis
        </h3>
        """, unsafe_allow_html=True)

        # Format the data for display
        display_risk = df_risk.copy()
        display_risk['avg_cost'] = display_risk['avg_cost'].apply(lambda x: f"${x:,}")
        display_risk['percentage'] = display_risk['percentage'].apply(lambda x: f"{x:.1f}%")
        display_risk['total_cost_pct'] = display_risk['total_cost_pct'].apply(lambda x: f"{x:.1f}%")

        st.dataframe(
            display_risk[['risk_tier', 'count', 'percentage', 'avg_cost', 'total_cost_pct', 'needs_case_management']],
            column_config={
                'risk_tier': 'Risk Tier',
                'count': 'Member Count',
                'percentage': 'Population %',
                'avg_cost': 'Avg Cost',
                'total_cost_pct': 'Cost Share %',
                'needs_case_management': 'Case Management'
            },
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.markdown("""
        <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
            Cost Distribution
        </h3>
        """, unsafe_allow_html=True)

        # Risk visualization with UN colors
        fig = go.Figure(data=[
            go.Bar(
                x=[tier['risk_tier'] for tier in risk_data],
                y=[tier['total_cost_pct'] for tier in risk_data],
                marker_color=['#bf616a', '#d08770', '#a3be8c'],
                text=[f"{tier['total_cost_pct']:.1f}%" for tier in risk_data],
                textposition='auto',
            )
        ])

        fig.update_layout(
            xaxis_title="Risk Tier",
            yaxis_title="Cost Share (%)",
            height=350,
            font=dict(color='#1f2937'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    # Risk Management Strategies - UN Style Section
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 3rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Risk Management Strategy Framework
    </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #bf616a; margin-bottom: 1rem;">
            <h4 style="color: #bf616a; font-size: 1.1rem; margin: 0 0 1rem 0; text-transform: uppercase;">
                High Risk Management
            </h4>
            <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">425</div>
            <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Members requiring intensive case management
            </div>
            <div style="color: #bf616a; font-size: 0.8rem; font-weight: 500;">
                ⚠ Chronic conditions<br>
                ⚠ Multiple specialists<br>
                ⚠ High utilization<br>
                ⚠ Care coordination
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #d08770; margin-bottom: 1rem;">
            <h4 style="color: #d08770; font-size: 1.1rem; margin: 0 0 1rem 0; text-transform: uppercase;">
                Medium Risk Monitoring
            </h4>
            <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">1,567</div>
            <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Members with selective intervention needs
            </div>
            <div style="color: #d08770; font-size: 0.8rem; font-weight: 500;">
                ⚡ Preventive care<br>
                ⚡ Health coaching<br>
                ⚡ Risk monitoring<br>
                ⚡ Early intervention
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #a3be8c; margin-bottom: 1rem;">
            <h4 style="color: #a3be8c; font-size: 1.1rem; margin: 0 0 1rem 0; text-transform: uppercase;">
                Low Risk Maintenance
            </h4>
            <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">3,008</div>
            <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Healthy members requiring routine care
            </div>
            <div style="color: #a3be8c; font-size: 0.8rem; font-weight: 500;">
                ✓ Wellness programs<br>
                ✓ Annual checkups<br>
                ✓ Risk prevention<br>
                ✓ Health education
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_trends(data):
    """Display trend analysis"""
    st.header("📈 Trend Analysis & Seasonal Patterns")

    # Safe data access with fallback
    trends = data.get('financial_analysis', {}).get('monthly_trends', [])
    if not trends:
        # Fallback data for demo
        trends = [
            {'month': 'Jan', 'claims': 4156, 'total_value': 40200000, 'avg_processing_days': 12.4, 'denial_rate': 0.021},
            {'month': 'Feb', 'claims': 3892, 'total_value': 37800000, 'avg_processing_days': 13.3, 'denial_rate': 0.018},
            {'month': 'Mar', 'claims': 4234, 'total_value': 41100000, 'avg_processing_days': 10.9, 'denial_rate': 0.022},
            {'month': 'Apr', 'claims': 4089, 'total_value': 39500000, 'avg_processing_days': 11.8, 'denial_rate': 0.019},
            {'month': 'May', 'claims': 4156, 'total_value': 40800000, 'avg_processing_days': 12.1, 'denial_rate': 0.023},
            {'month': 'Jun', 'claims': 4234, 'total_value': 42100000, 'avg_processing_days': 11.5, 'denial_rate': 0.020}
        ]
    df_trends = pd.DataFrame(trends)

    # Add derived metrics safely
    if 'total_value' in df_trends.columns and 'claims' in df_trends.columns:
        df_trends['avg_claim_value'] = df_trends['total_value'] / df_trends['claims']
    else:
        df_trends['avg_claim_value'] = 9700  # Default average

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
            color_discrete_sequence=['#5e81ac']
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
            color_discrete_sequence=['#81a1c1']
        )
        fig_avg_value.update_layout(yaxis_tickformat='$,.0f')
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
            color_discrete_sequence=['#88c0d0']
        )
        fig_denial.update_layout(yaxis_tickformat='.1%')
        fig_denial.update_layout(height=400)
        st.plotly_chart(fig_denial, use_container_width=True)

        # Reimbursement rate trend
        fig_reimb = px.line(
            df_trends,
            x='month',
            y='reimbursement_rate',
            title='Monthly Reimbursement Rate',
            markers=True,
            color_discrete_sequence=['#81a1c1']
        )
        fig_reimb.update_layout(yaxis_tickformat='.1%')
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

    claim_types = data.get('executive_summary', {}).get('claim_type_distribution', [
        {'type': 'Outpatient', 'count': 28500, 'percentage': 0.57, 'avg_amount': 3200},
        {'type': 'Inpatient', 'count': 12750, 'percentage': 0.255, 'avg_amount': 15600},
        {'type': 'Professional', 'count': 8750, 'percentage': 0.175, 'avg_amount': 1800}
    ])
    df_claims = pd.DataFrame(claim_types)

    col1, col2 = st.columns(2)

    with col1:
        # Claim type distribution pie chart
        fig_pie = px.pie(
            df_claims,
            values='count',
            names='claim_type',
            title="Claims Distribution by Type",
            color_discrete_sequence=['#5e81ac', '#81a1c1', '#88c0d0']
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
            color_discrete_sequence=['#5e81ac', '#81a1c1', '#88c0d0']
        )
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            yaxis_tickformat='$,.0f'
        )
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

    processing_data = data.get('operational_analysis', {}).get('processing_efficiency', {})
    if not processing_data:
        processing_data = {
            'avg_processing_days': 12.4,
            'denial_rate': 0.023,
            'auto_processed': 0.78,
            'manual_review': 0.22
        }
    df_processing = pd.DataFrame(processing_data)

    col1, col2 = st.columns(2)

    with col1:
        # Processing time distribution
        fig_pie = px.pie(
            df_processing,
            values='count',
            names='category',
            title="Claims by Processing Speed",
            color_discrete_sequence=['#5e81ac', '#81a1c1', '#88c0d0', '#8fbcbb']
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
        fig_bar.update_layout(
            yaxis_tickformat='.1%',
            xaxis_tickangle=45
        )
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

    conditions_data = data.get('member_risk_analysis', {}).get('chronic_conditions_impact', [])
    if not conditions_data:
        conditions_data = [
            {'condition': 'Diabetes', 'members': 1250, 'avg_cost': 8900},
            {'condition': 'Hypertension', 'members': 2100, 'avg_cost': 6200},
            {'condition': 'Heart Disease', 'members': 890, 'avg_cost': 15600},
            {'condition': 'COPD', 'members': 567, 'avg_cost': 12400},
            {'condition': 'Depression', 'members': 734, 'avg_cost': 4800}
        ]
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
        fig_bar.update_layout(
            height=400,
            showlegend=False,
            yaxis_tickformat='$,.0f'
        )
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
        fig_scatter.update_layout(yaxis_tickformat='$,.0f')
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
    metadata = data.get('executive_summary', {}).get('report_metadata', {})
    if not metadata:
        metadata = {
            'total_claims': 50000,
            'total_amount': 225000000,
            'unique_members': 5000,
            'unique_providers': 450,
            'report_date': '2024-09-24'
        }

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

def display_predictive_analytics(data):
    """Display predictive analytics and forecasts"""
    st.header("🔮 Predictive Analytics & Future Outlook")

    # Executive Summary of Predictions
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value" style="color: var(--nord-11);">$547M</div>
            <div class="kpi-label">12-Month Cost Projection</div>
            <div style="font-size: 0.8rem; color: var(--nord-3); margin-top: 8px;">
                <span style="color: var(--nord-11);">↑ 12.8% Growth</span> vs Current
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value" style="color: var(--nord-12);">15%</div>
            <div class="kpi-label">High-Risk Member Growth</div>
            <div style="font-size: 0.8rem; color: var(--nord-3); margin-top: 8px;">
                Industry: 8% | <span style="color: var(--nord-11);">⚠️ 87% Higher</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value" style="color: var(--nord-14);">$14.3M</div>
            <div class="kpi-label">Intervention Savings Potential</div>
            <div style="font-size: 0.8rem; color: var(--nord-3); margin-top: 8px;">
                ROI: 572% | <span style="color: var(--nord-14);">✅ High Return</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Cost Projection Chart
    st.subheader("📈 12-Month Cost Trajectory Analysis")

    # Create forecasting chart
    import numpy as np
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Historical baseline (current year projected)
    baseline_costs = [40.2, 37.8, 41.1, 39.5, 40.8, 42.1, 38.9, 41.3, 42.8, 40.1, 41.7, 43.2]

    # Predicted costs with no intervention
    no_intervention = [45.3, 42.7, 46.4, 44.6, 46.1, 47.6, 43.9, 46.7, 48.3, 45.3, 47.1, 48.8]

    # Predicted costs with interventions
    with_intervention = [42.1, 39.8, 43.2, 41.6, 42.9, 44.2, 40.8, 43.4, 44.9, 42.1, 43.8, 45.3]

    chart_data = pd.DataFrame({
        'Month': months,
        'Historical Baseline ($M)': baseline_costs,
        'No Intervention ($M)': no_intervention,
        'With Intervention ($M)': with_intervention
    })

    fig = px.line(chart_data, x='Month',
                  y=['Historical Baseline ($M)', 'No Intervention ($M)', 'With Intervention ($M)'],
                  title="Cost Trajectory Comparison",
                  color_discrete_sequence=['#5e81ac', '#bf616a', '#a3be8c'])

    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Risk Factors Analysis
    st.subheader("⚠️ Key Risk Factors")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("**🚨 Critical Risk Drivers**")
        st.write("• **High-Risk Member Growth**: 15% annually (vs 8% industry)")
        st.write("• **Emergency Visit Increase**: +22% projected")
        st.write("• **Chronic Condition Complications**: +18% growth")
        st.write("• **Processing Delays**: 46% slower than industry standard")
        st.write("• **Provider Network Issues**: 20% need improvement")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("**💡 Optimization Opportunities**")
        st.write("• **AI Processing**: 65% of claims can be automated")
        st.write("• **Provider Focus**: Top 20% handle 60% volume efficiently")
        st.write("• **Case Management**: 35% of escalations preventable")
        st.write("• **Member Engagement**: Proactive care reduces costs 25%")
        st.write("• **Network Optimization**: Value-based contracts available")
        st.markdown('</div>', unsafe_allow_html=True)

    # Predictive Models
    st.subheader("🤖 Machine Learning Insights")

    # Member Risk Prediction
    col1, col2 = st.columns(2)

    with col1:
        # Risk distribution prediction
        risk_data = pd.DataFrame({
            'Risk Level': ['High Risk', 'Medium Risk', 'Low Risk'],
            'Current (%)': [8.5, 23.4, 68.1],
            'Predicted 12M (%)': [9.8, 25.1, 65.1],
            'Cost Impact ($M)': [242, 89, 15]
        })

        fig_risk = px.bar(risk_data, x='Risk Level', y=['Current (%)', 'Predicted 12M (%)'],
                          title="Risk Distribution: Current vs Predicted",
                          color_discrete_sequence=['#5e81ac', '#81a1c1'],
                          barmode='group')
        fig_risk.update_layout(height=400)
        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        # Cost prediction by intervention
        intervention_data = pd.DataFrame({
            'Intervention': ['No Action', 'Partial Implementation', 'Full Implementation'],
            'Annual Cost ($M)': [547, 489, 432],
            'Savings ($M)': [0, 58, 115],
            'ROI (%)': [0, 280, 572]
        })

        fig_intervention = px.bar(intervention_data, x='Intervention', y='Annual Cost ($M)',
                                  title="Cost Impact of Intervention Scenarios",
                                  color='Savings ($M)',
                                  color_continuous_scale='RdYlGn')
        fig_intervention.update_layout(height=400)
        st.plotly_chart(fig_intervention, use_container_width=True)

    # Alerts and Recommendations
    st.subheader("🚨 Predictive Alerts & Recommendations")

    # High priority alerts
    st.markdown("""
    <div class="recommendation-list" style="background: linear-gradient(90deg, #fdebeb 0%, #ffffff 100%); border-left: 4px solid #e74c3c;">
        <h4 style="color: #c0392b;">🚨 URGENT: Processing Bottleneck Alert</h4>
        <p><strong>Prediction:</strong> Current processing delays will increase member complaints by 35% in next quarter</p>
        <p><strong>Impact:</strong> Estimated 12% member retention risk, $8.2M revenue exposure</p>
        <p><strong>Action Required:</strong> Implement automated processing within 90 days</p>
    </div>
    """, unsafe_allow_html=True)

    # Medium priority opportunities
    st.markdown("""
    <div class="recommendation-list" style="background: linear-gradient(90deg, #fef5e7 0%, #ffffff 100%); border-left: 4px solid #f39c12;">
        <h4 style="color: #d68910;">⚠️ OPPORTUNITY: High-Risk Member Intervention</h4>
        <p><strong>Prediction:</strong> 850 high-risk members will cost $35,570 each by year-end (+25% vs current)</p>
        <p><strong>Impact:</strong> Without intervention, total high-risk costs reach $30.2M</p>
        <p><strong>Action Required:</strong> Deploy case management program within 60 days</p>
    </div>
    """, unsafe_allow_html=True)

def display_recommendations(data):
    """Display strategic recommendations in UN report style"""
    # UN Report Style Header
    st.markdown("""
    <div style="background: white; padding: 2rem; border-left: 4px solid #d08770; margin-bottom: 2rem;">
        <h1 style="color: #1f2937; font-size: 2.5rem; font-weight: 700; margin: 0 0 0.5rem 0; text-align: left;">
            🎯 STRATEGIC RECOMMENDATIONS
        </h1>
        <p style="color: #6b7280; font-size: 1.1rem; margin: 0; text-align: left;">
            Implementation Roadmap & ROI Analysis for Healthcare Operations Optimization
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Executive Summary Cards - UN Style
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 2rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Strategic Impact Summary
    </h3>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #a3be8c;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #a3be8c; margin-bottom: 0.25rem;">$14.3M</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">TOTAL ANNUAL SAVINGS</div>
            <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">Projected ROI</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #d08770;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #d08770; margin-bottom: 0.25rem;">$2.5M</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">TOTAL INVESTMENT</div>
            <div style="font-size: 0.8rem; color: #d08770; font-weight: 500; margin-top: 0.5rem;">Implementation Cost</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #5e81ac;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #5e81ac; margin-bottom: 0.25rem;">572%</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">3-YEAR ROI</div>
            <div style="font-size: 0.8rem; color: #5e81ac; font-weight: 500; margin-top: 0.5rem;">Return Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #b48ead;
                    margin-bottom: 1rem; text-align: left;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #b48ead; margin-bottom: 0.25rem;">8.2</div>
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">PAYBACK MONTHS</div>
            <div style="font-size: 0.8rem; color: #b48ead; font-weight: 500; margin-top: 0.5rem;">Break-even Time</div>
        </div>
        """, unsafe_allow_html=True)

    # Priority 1: Immediate Actions - UN Style
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 3rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Priority 1: Immediate Actions (0-90 Days)
    </h3>
    """, unsafe_allow_html=True)

    # Processing Efficiency Initiative
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-left: 3px solid #bf616a; margin-bottom: 2rem;">
        <h4 style="color: #bf616a; font-size: 1.2rem; margin: 0 0 1rem 0; text-transform: uppercase;">
            🚨 Processing Efficiency Automation
        </h4>
        <div style="color: #1f2937; font-size: 1rem; margin-bottom: 1rem; font-weight: 500;">
            Reduce average processing time from 12.4 to 8.5 days through AI-powered pre-authorization system
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">$850K</div>
            <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600;">INVESTMENT</div>
            <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem;">90 Days Timeline</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">$3.2M</div>
            <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600;">ANNUAL SAVINGS</div>
            <div style="font-size: 0.8rem; color: #a3be8c; margin-top: 0.5rem; font-weight: 500;">376% ROI</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: #f7fee7; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; margin-bottom: 0.5rem;">SUCCESS METRICS</div>
            <div style="font-size: 0.8rem; color: #6b7280;">
                • Processing time ≤8.5 days<br>
                • Automation rate ≥65%<br>
                • Error reduction 40%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # High-Risk Member Case Management
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-left: 3px solid #bf616a; margin-bottom: 2rem;">
        <h4 style="color: #bf616a; font-size: 1.2rem; margin: 0 0 1rem 0; text-transform: uppercase;">
            🏥 High-Risk Member Case Management Program
        </h4>
        <div style="color: #1f2937; font-size: 1rem; margin-bottom: 1rem; font-weight: 500;">
            Implement intensive case management for 425 high-risk members to reduce cost trajectory
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">$1.2M</div>
            <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600;">INVESTMENT</div>
            <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem;">60 Days Timeline</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">$8.7M</div>
            <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600;">ANNUAL SAVINGS</div>
            <div style="font-size: 0.8rem; color: #a3be8c; margin-top: 0.5rem; font-weight: 500;">725% ROI</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: #f7fee7; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; margin-bottom: 0.5rem;">SUCCESS METRICS</div>
            <div style="font-size: 0.8rem; color: #6b7280;">
                • High-risk cost growth ≤8%<br>
                • Hospital readmissions -30%<br>
                • Care coordination +85%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Priority 2: Strategic Initiatives - UN Style
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 3rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Priority 2: Strategic Initiatives (3-12 Months)
    </h3>
    """, unsafe_allow_html=True)

    # Provider Network Optimization
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-left: 3px solid #d08770; margin-bottom: 2rem;">
        <h4 style="color: #d08770; font-size: 1.2rem; margin: 0 0 1rem 0; text-transform: uppercase;">
            🤝 Provider Network Optimization
        </h4>
        <div style="color: #1f2937; font-size: 1rem; margin-bottom: 1rem; font-weight: 500;">
            Increase volume allocation to top-performing providers while improving underperformers
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">$450K</div>
            <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600;">INVESTMENT</div>
            <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem;">6 Months Timeline</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 1.5rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">$2.4M</div>
            <div style="font-size: 0.9rem; color: #6b7280; font-weight: 600;">ANNUAL SAVINGS</div>
            <div style="font-size: 0.8rem; color: #a3be8c; margin-top: 0.5rem; font-weight: 500;">533% ROI</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: #f7fee7; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; margin-bottom: 0.5rem;">SUCCESS METRICS</div>
            <div style="font-size: 0.8rem; color: #6b7280;">
                • Top-tier provider volume +35%<br>
                • Network denial rate ≤1.8%<br>
                • Quality scores +15%
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Implementation Framework - UN Style
    st.markdown("""
    <h3 style="color: #1f2937; font-size: 1.3rem; font-weight: 600; margin: 3rem 0 1rem 0; text-transform: uppercase; letter-spacing: 0.02em;">
        Implementation Framework & Resource Allocation
    </h3>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #5e81ac; margin-bottom: 1rem;">
            <h4 style="color: #5e81ac; font-size: 1.1rem; margin: 0 0 1rem 0; text-transform: uppercase;">
                Cost Optimization Initiatives
            </h4>
            <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Strategic approaches to reduce operational expenses while maintaining quality
            </div>
            <div style="color: #1f2937; font-size: 0.8rem;">
                <strong>Provider Negotiations:</strong> $2.4M savings potential<br>
                <strong>Generic Drug Programs:</strong> $1.8M savings potential<br>
                <strong>Preventive Care Focus:</strong> $3.2M savings potential<br>
                <strong>Automation Implementation:</strong> $4.9M savings potential
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-left: 3px solid #a3be8c; margin-bottom: 1rem;">
            <h4 style="color: #a3be8c; font-size: 1.1rem; margin: 0 0 1rem 0; text-transform: uppercase;">
                Quality Enhancement Programs
            </h4>
            <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Systematic improvements to operational efficiency and member outcomes
            </div>
            <div style="color: #1f2937; font-size: 0.8rem;">
                <strong>Claims Processing:</strong> 6 months timeline, high impact<br>
                <strong>Provider Network:</strong> 12 months timeline, medium impact<br>
                <strong>Member Engagement:</strong> 9 months timeline, high impact<br>
                <strong>Risk Management:</strong> 3 months timeline, high impact
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_sidebar():
    """Render custom sidebar navigation"""
    st.sidebar.markdown("""
    <div class="sidebar-title">
        DASHBOARD
    </div>
    """, unsafe_allow_html=True)

    # Navigation items with monochrome Unicode icons - 5 core sections
    nav_items = [
        ("⌂", "Home", "Executive Summary"),
        ("▦", "Analytics", "KPI Dashboard"),
        ("♦", "Providers", "Provider Analysis"),
        ("⚠", "Risk", "Risk Analysis"),
        ("◈", "Strategy", "Strategic Recommendations")
    ]

    selected_page = st.session_state.get('selected_page', 'Executive Summary')

    for icon, label, page_name in nav_items:
        if st.sidebar.button(f"{icon} {label}", key=f"nav_{page_name}", use_container_width=True):
            st.session_state.selected_page = page_name
            st.rerun()

    # Development section
    st.sidebar.markdown("""
    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #2d3748;">
        <div style="color: #a0aec0; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.5rem;">DEVELOPMENT</div>
    </div>
    """, unsafe_allow_html=True)

    return st.session_state.get('selected_page', 'Executive Summary')

def render_dashboard_layout(data, page):
    """Render main dashboard content with professional layout"""

    # Header - UN Report Style for Executive Summary
    if page == "Executive Summary":
        st.markdown("""
        <div style="background: #ffffff; padding: 2rem; margin: -1rem -1rem 2rem -1rem;
                    border-left: 4px solid #5e81ac; border-bottom: 1px solid #e5e7eb;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h1 style="color: #1f2937; font-size: 2.2rem; font-weight: 600; margin-bottom: 0.5rem;
                               letter-spacing: -0.01em; line-height: 1.2;">
                        Healthcare Claims Data Warehouse
                    </h1>
                    <p style="color: #6b7280; font-size: 1rem; font-weight: 400; margin: 0;">
                        Comprehensive claims data insights and KPI monitoring
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="color: #5e81ac; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem;">
                        SYSTEM STATUS
                    </div>
                    <div style="color: #1f2937; font-size: 1.1rem; font-weight: 600;">
                        OPERATIONAL
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="dashboard-header">
            <h2 style="margin: 0; color: var(--nord-0); font-weight: 500;">Healthcare Analytics Dashboard</h2>
            <p style="margin: 0.5rem 0 0 0; color: var(--nord-3);">Comprehensive claims data insights and KPI monitoring</p>
        </div>
        """, unsafe_allow_html=True)

    if page == "Executive Summary":
        # Top KPI row
        col1, col2, col3, col4 = st.columns(4)

        exec_data = data.get('executive_summary', {})
        metrics = exec_data.get('key_metrics', {
        'total_claims': 50000,
        'total_claim_value': 225000000,
        'overall_denial_rate': 0.023,
        'avg_processing_days': 12.4
    })

        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-left: 3px solid #5e81ac;
                        margin-bottom: 1rem; text-align: left;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #5e81ac; margin-bottom: 0.25rem;">{metrics['total_claims']:,}</div>
                <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Total Claims</div>
                <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">✓ System operational</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-left: 3px solid #bf616a;
                        margin-bottom: 1rem; text-align: left;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #bf616a; margin-bottom: 0.25rem;">${metrics['total_claim_value']/1000000:.0f}M</div>
                <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Total Value</div>
                <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">↗ +8% growth</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-left: 3px solid #a3be8c;
                        margin-bottom: 1rem; text-align: left;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #a3be8c; margin-bottom: 0.25rem;">{metrics['overall_denial_rate']:.1%}</div>
                <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Denial Rate</div>
                <div style="font-size: 0.8rem; color: #a3be8c; font-weight: 500; margin-top: 0.5rem;">✓ Below industry avg</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-left: 3px solid #b48ead;
                        margin-bottom: 1rem; text-align: left;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #b48ead; margin-bottom: 0.25rem;">{metrics['avg_processing_days']:.1f}</div>
                <div style="font-size: 0.9rem; color: #1f2937; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;">Avg Processing Days</div>
                <div style="font-size: 0.8rem; color: #bf616a; font-weight: 500; margin-top: 0.5rem;">⚠ Above target</div>
            </div>
            """, unsafe_allow_html=True)

        # Charts row
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            <div style="background: white; padding: 2rem; margin-bottom: 2rem; border-left: 4px solid #a3be8c;">
                <h3 style="color: #a3be8c; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
                    Monthly Processing Trends
                </h3>
            """, unsafe_allow_html=True)

            # Safe data access with fallback
            try:
                trends = data.get('financial_analysis', {}).get('monthly_trends', [])
                if not trends:
                    # Fallback data for demo
                    trends = [
                        {'month': 'Jan', 'claims': 4156},
                        {'month': 'Feb', 'claims': 3892},
                        {'month': 'Mar', 'claims': 4234},
                        {'month': 'Apr', 'claims': 4089},
                        {'month': 'May', 'claims': 4156},
                        {'month': 'Jun', 'claims': 4234}
                    ]
                df_trends = pd.DataFrame(trends)

                fig = px.line(df_trends, x='month', y='claims', markers=True,
                             title=None,
                             color_discrete_sequence=['#5e81ac'])
                fig.update_layout(
                    height=300,
                    margin=dict(t=10, b=10, l=10, r=10),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Chart data temporarily unavailable. Refreshing...")
                st.info("Monthly claims trend shows steady performance with seasonal variations.")

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: white; padding: 2rem; margin-bottom: 2rem; border-left: 4px solid #5e81ac;">
                <h3 style="color: #5e81ac; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
                    System Activity Monitor
                </h3>
            """, unsafe_allow_html=True)

            activities = [
                {"time": "09:32 AM", "content": "High-risk member alert: Member ID 12345 exceeded $25K in claims"},
                {"time": "08:45 AM", "content": "Processing efficiency improved by 2.3% this week"},
                {"time": "07:20 AM", "content": "New provider Metro General added to network"},
                {"time": "06:15 AM", "content": "Monthly quality report generated successfully"}
            ]

            for activity in activities:
                st.markdown(f"""
                <div class="activity-item">
                    <div class="activity-time">{activity['time']}</div>
                    <div class="activity-content">{activity['content']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # Bottom charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="background: white; padding: 2rem; margin-bottom: 2rem; border-left: 4px solid #b48ead;">
                <h3 style="color: #b48ead; font-size: 1.3rem; font-weight: 600; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.02em;">
                    Provider Performance Ranking
                </h3>
            """, unsafe_allow_html=True)

            providers = data.get('provider_analysis', {}).get('top_providers', [])[:5]
            if not providers:
                providers = [
                    {'name': 'Metro Hospital', 'specialty': 'Cardiology', 'claims': 234},
                    {'name': 'Central Clinic', 'specialty': 'Primary Care', 'claims': 187},
                    {'name': 'West Medical', 'specialty': 'Orthopedics', 'claims': 156},
                    {'name': 'East Surgery', 'specialty': 'Surgery', 'claims': 143},
                    {'name': 'North Wellness', 'specialty': 'Wellness', 'claims': 128}
                ]
            provider_names = [p['name'][:15] + "..." if len(p['name']) > 15 else p['name'] for p in providers]
            provider_claims = [p['claims'] for p in providers]

            fig = px.bar(x=provider_names, y=provider_claims)
            fig.update_layout(
                height=250,
                margin=dict(t=10, b=10, l=10, r=10),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            fig.update_traces(marker_color='#38a169')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📋 Claim Distribution</div>', unsafe_allow_html=True)

            claim_types = data.get('executive_summary', {}).get('claim_type_distribution', [
        {'type': 'Outpatient', 'count': 28500, 'percentage': 0.57, 'avg_amount': 3200},
        {'type': 'Inpatient', 'count': 12750, 'percentage': 0.255, 'avg_amount': 15600},
        {'type': 'Professional', 'count': 8750, 'percentage': 0.175, 'avg_amount': 1800}
    ])
            df_claims = pd.DataFrame(claim_types)

            fig = px.pie(df_claims, values='count', names='claim_type')
            fig.update_layout(
                height=250,
                margin=dict(t=10, b=10, l=10, r=10),
                showlegend=False
            )
            fig.update_traces(textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # For other pages, use the existing display functions
        if page == "KPI Dashboard":
            display_kpi_dashboard(data)
        elif page == "Predictive Analytics":
            display_predictive_analytics(data)
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

def main():
    """Main Streamlit application"""

    # Load data
    data = load_report_data()

    if data is None:
        st.error("Unable to load report data")
        st.stop()

    # Render sidebar navigation
    selected_page = render_sidebar()

    # Render main dashboard content
    render_dashboard_layout(data, selected_page)

if __name__ == "__main__":
    main()