import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from styles import apply_custom_css

def fix_plotly_dark(fig):
    if fig is not None:
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            margin=dict(l=20, r=20, t=40, b=20)
        )
    return fig

st.set_page_config(
    page_title="ACC Employability Intelligence Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# Load Cached Dataset
@st.cache_data(ttl=3600)
def load_datasets():
    csv_path = os.path.join("data", "employability_dataset.csv")
    if not os.path.exists(csv_path):
        from scripts.generate_data import generate_employability_dataset
        df = generate_employability_dataset()
    else:
        df = pd.read_csv(csv_path)
    return df

df_raw = load_datasets()

# --- SIDEBAR MATCHING REFERENCE DESIGN ---

# 1. Top App Pill Badge
st.sidebar.markdown("""
<div style="background: rgba(0, 230, 118, 0.18); border: 2px solid #00E676; border-radius: 12px; padding: 10px 16px; color: #FFFFFF !important; font-weight: 900; font-size: 1.1rem; margin-bottom: 16px; display: inline-block; box-shadow: 0 0 16px rgba(0,230,118,0.3);">
    app
</div>
""", unsafe_allow_html=True)

# 2. Native Sidebar Radio Navigation
selected_view = st.sidebar.radio(
    "Navigation Options",
    [
        "📌 Executive Summary",
        "⚖️ Internship vs Cert Comparison",
        "📊 Placement & Salary Analytics",
        "🏢 Employer Preference Engine",
        "🎯 Skills Demand Engine",
        "🚀 AI Pathway Advisor & Strategy"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# 3. Middle Brand Card Box
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.9)); border: 1px solid rgba(56, 189, 248, 0.5); border-radius: 16px; padding: 18px; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 14px;">
        <div style="background: rgba(0, 230, 118, 0.2); border: 2px solid #00E676; border-radius: 12px; padding: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 16px rgba(0,230,118,0.4); font-size: 1.4rem;">
            🎓
        </div>
        <div>
            <div style="font-size: 1.15rem; font-weight: 900; color: #FFFFFF !important; letter-spacing: -0.3px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">ACC EMPLOYABILITY CORE</div>
            <div style="font-size: 0.78rem; color: #38BDF8 !important; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px;">💎 ANALYTICS ENGINE</div>
        </div>
    </div>
    <div style="background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(0, 230, 118, 0.4); border-radius: 12px; padding: 12px 14px;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #FFFFFF !important; font-weight: 900; margin-bottom: 6px;">
            <span style="width: 10px; height: 10px; border-radius: 50%; background-color: #00E676; box-shadow: 0 0 12px #00E676; display: inline-block;"></span>
            SYSTEM ONLINE
        </div>
        <div style="font-size: 0.82rem; color: #FFFFFF !important; font-weight: 500; line-height: 1.5;">
            Career decision matrix active with <b>2,500+</b> data points loaded.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Expandable Telemetry & Framework Accordions
with st.sidebar.expander("🎓 System Telemetry & Datasets", expanded=True):
    selected_years = st.multiselect(
        "Graduation Year",
        options=sorted(df_raw['Graduation_Year'].unique()),
        default=sorted(df_raw['Graduation_Year'].unique())
    )

    selected_colleges = st.multiselect(
        "College Category",
        options=sorted(df_raw['College_Name'].unique()),
        default=sorted(df_raw['College_Name'].unique())
    )

    selected_branches = st.multiselect(
        "Course / Branch",
        options=sorted(df_raw['Course_Branch'].unique()),
        default=sorted(df_raw['Course_Branch'].unique())
    )
    
    interns_df_raw = df_raw[df_raw['Number_of_Internships'] > 0]
    placed_count_raw = len(df_raw[df_raw['Placement_Status'] == 'Placed'])
    
    st.markdown(f"""
    <div style="font-size: 0.85rem; color: #FFFFFF !important; line-height: 1.8; margin-top: 10px;">
        <div>🎓 <b>Total Student Records:</b> <span style="color: #00E676 !important;">{len(df_raw):,}</span></div>
        <div>💼 <b>Internship Records:</b> <span style="color: #38BDF8 !important;">{len(interns_df_raw):,}</span></div>
        <div>📜 <b>Certification Records:</b> <span style="color: #FBBF24 !important;">{len(df_raw[df_raw['Number_of_Certifications']>0]):,}</span></div>
        <div>🌟 <b>Placed Students:</b> <span style="color: #C084FC !important;">{placed_count_raw:,}</span></div>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar.expander("🎛️ Active Decision Framework", expanded=False):
    st.markdown("""
    <div style="font-size: 0.82rem; color: #FFFFFF !important; line-height: 1.7;">
        <div>• <b>Ranking Method:</b> MCDA (AHP Weighting + Multi-Attribute Ranking) & Random Forest ML</div>
        <div>• <b>Statistical Engine:</b> Welch T-Test (Salary Premium) & Chi-Square (Placement Rate)</div>
        <div>• <b>Coverage:</b> Pan-India Tech & Business Institutions (2,500 Student Profiles)</div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 8px; font-size: 0.8rem; color: #FFFFFF !important; font-weight: 700;">
    🚀 Powered by <span style="color: #00E676 !important;">ACC Analytics Team</span> | Data Analyst
</div>
""", unsafe_allow_html=True)


# --- DYNAMIC MAIN CONTENT AREA ROUTING ---

df_filtered = df_raw[
    (df_raw['Graduation_Year'].isin(selected_years)) &
    (df_raw['College_Name'].isin(selected_colleges)) &
    (df_raw['Course_Branch'].isin(selected_branches))
]

total_records = len(df_filtered)
placed_count = len(df_filtered[df_filtered['Placement_Status'] == 'Placed'])
overall_placement_rate = (placed_count / total_records * 100) if total_records > 0 else 0
avg_salary = df_filtered[df_filtered['Placement_Status'] == 'Placed']['Salary_Package_LPA'].mean() if placed_count > 0 else 0

interns_df = df_filtered[df_filtered['Number_of_Internships'] > 0]
ppo_count = len(interns_df[interns_df['PPO_Conversion_Status'] == 'Direct PPO (Pre-Placement Offer)'])
ppo_rate = (ppo_count / len(interns_df) * 100) if len(interns_df) > 0 else 0
avg_emp_pref = df_filtered['Employer_Preference_Score'].mean() if len(df_filtered) > 0 else 0

# Header Banner
st.title("🎓 ACC Employability Intelligence & Career Success Platform")
st.markdown("### *Data-driven decision intelligence comparing the value of internships vs certifications for students.*")

st.markdown("---")

# Global 5 KPI Metric Cards Row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Datasets Loaded", f"{total_records:,}", delta="🎓 2.5k Student Scale")
with col2:
    st.metric("Overall Placement Rate", f"{overall_placement_rate:.1f}%", delta="⭐ 98.3% Hybrid Peak")
with col3:
    st.metric("Avg Placed Salary", f"₹{avg_salary:.2f} LPA", delta="🚀 +49.4% Internship Boost")
with col4:
    st.metric("PPO Conversion Rate", f"{ppo_rate:.1f}%", delta="💼 6+ Month Duration")
with col5:
    st.metric("Employer Preference", f"{avg_emp_pref:.1f} / 10", delta="🎯 Internship Priority")

st.markdown("---")

# ROUTING LOGIC
if "📌 Executive Summary" in selected_view:
    st.markdown("""
    <div class="glass-card">
        <h2 style="color: #FFFFFF !important; margin-bottom: 14px;">🚀 Welcome to the Decision Intelligence Platform</h2>
        <p style="color: #FFFFFF !important; margin-bottom: 16px;">This platform integrates multi-source student employability data across universities and job portals to evaluate <b>practical internship outcomes</b>, assess <b>certification effectiveness</b>, and provide <b>explainable personal recommendations</b> for students.</p>
        <ul style="color: #FFFFFF !important; line-height: 1.8;">
            <li><b style="color: #00E676 !important;">📌 Executive Summary</b>: Overview of student placement rates, salary packages, and experience profile breakdown.</li>
            <li><b style="color: #38BDF8 !important;">⚖️ Internship vs Cert Comparison</b>: Direct head-to-head evaluation, scatter distributions, and hypothesis tests.</li>
            <li><b style="color: #FBBF24 !important;">📊 Placement & Salary Analytics</b>: Internship duration impact, PPO conversion rates, and time-to-offer velocity.</li>
            <li><b style="color: #F43F5E !important;">🏢 Employer Preference Engine</b>: Machine learning feature importance rankings and industry preference heatmaps.</li>
            <li><b style="color: #C084FC !important;">🎯 Skills Demand Engine</b>: Top paying & high-volume skills matrix with interactive explorer.</li>
            <li><b style="color: #00E676 !important;">🚀 AI Pathway Advisor & Strategy</b>: Personal AI outcome predictor and 4-phase student career execution roadmap.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    items = [
        "<b>Placement Advantage:</b> Candidates with practical internship experience achieve a <b>97.8% placement rate</b> vs <b>70.0%</b> for certification-only graduates (+27.8% advantage).",
        "<b>Salary Multiplier:</b> Internship experience delivers a <b>+₹4.37 LPA (+49.4%) starting salary boost</b> over certification-only candidates.",
        "<b>Hybrid Synergy:</b> Combining internships with targeted certs yields peak performance: <b>98.3% placement</b> and <b>₹14.37 LPA</b> average package.",
        "<b>PPO Conversion Velocity:</b> Internships <b>≥ 6 months</b> yield a <b>65%+ direct PPO conversion rate</b>, reducing time-to-offer to under 30 days."
    ]
    items_html = "".join([f"<div style='color:#FFFFFF !important; margin-bottom: 10px; font-size: 0.95rem; line-height: 1.5;'>• {i}</div>" for i in items])
    st.markdown(f"""
    <div style="padding:22px; border:1px solid rgba(56,189,248,0.4); border-radius:16px; background:#0F1726; color:#FFFFFF !important; margin-bottom: 24px; box-shadow: 0 8px 25px rgba(0,0,0,0.5);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="color:#FFFFFF !important; margin:0; font-size: 1.25rem;">💡 Executive Platform Insights</h3>
            <span style="background:rgba(0,230,118,0.2); border:1px solid #00E676; color:#00E676 !important; font-size:0.75rem; font-weight:800; padding:5px 12px; border-radius:12px;">💎 ACC DECISION INTELLIGENCE</span>
        </div>
        {items_html}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    from dashboards import employability_impact
    employability_impact.render(df_filtered)

elif "⚖️ Internship vs Cert" in selected_view:
    from dashboards import internship_vs_cert
    internship_vs_cert.render(df_filtered)

elif "📊 Placement & Salary" in selected_view:
    from dashboards import placement_salary
    placement_salary.render(df_filtered)

elif "🏢 Employer Preference" in selected_view:
    from dashboards import employer_preference
    employer_preference.render(df_filtered)

elif "🎯 Skills Demand" in selected_view:
    from dashboards import skills_demand
    skills_demand.render(df_filtered)

elif "🚀 AI Pathway Advisor" in selected_view:
    from dashboards import career_outcomes
    career_outcomes.render(df_filtered)
