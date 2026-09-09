import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render(df):
    st.markdown("<h3 style='color: #F8FAFC; font-weight: 800;'>🎯 Skills Demand Dashboard</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>Identification of Most Valued Technical & Soft Skills Driving Higher Placements and Top Salaries</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Process Skills
    df_skills = df.assign(Skill=df['Primary_Skills'].str.split(', ')).explode('Skill')
    skills_summary = df_skills.groupby('Skill').agg(
        Total_Students=('Student_ID', 'count'),
        Placed_Students=('Placement_Status', lambda x: (x == 'Placed').sum()),
        Placement_Rate=('Placement_Status', lambda x: (x == 'Placed').mean() * 100),
        Avg_Salary=('Salary_Package_LPA', lambda x: x[x > 0].mean()),
        Avg_Employer_Pref=('Employer_Preference_Score', 'mean')
    ).reset_index()
    
    skills_summary['Avg_Salary'] = skills_summary['Avg_Salary'].round(2)
    skills_summary['Placement_Rate'] = skills_summary['Placement_Rate'].round(1)
    skills_summary['Avg_Employer_Pref'] = skills_summary['Avg_Employer_Pref'].round(2)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<h4 style='color: #FFFFFF !important;'>Top 10 Most Demanded Skills (Placed Volume)</h4>", unsafe_allow_html=True)
        top_by_volume = skills_summary.sort_values(by='Placed_Students', ascending=False).head(10)
        
        fig_vol = px.bar(
            top_by_volume,
            x='Placed_Students',
            y='Skill',
            orientation='h',
            text='Placed_Students',
            color='Placement_Rate',
            template='plotly_dark',
            color_continuous_scale='Blues',
            labels={'Placed_Students': 'Number of Placed Students', 'Skill': 'Skill Name'}
        )
        fig_vol.update_traces(textposition='outside')
        fig_vol.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            xaxis=dict(gridcolor="#1E293B"),
            yaxis=dict(gridcolor="#1E293B")
        )
        st.plotly_chart(fig_vol, use_container_width=True)
        
    with c2:
        st.markdown("<h4 style='color: #FFFFFF !important;'>Top 10 Highest Paying Skills (Avg LPA)</h4>", unsafe_allow_html=True)
        top_by_salary = skills_summary.sort_values(by='Avg_Salary', ascending=False).head(10)
        
        fig_sal_skill = px.bar(
            top_by_salary,
            x='Avg_Salary',
            y='Skill',
            orientation='h',
            text='Avg_Salary',
            color='Avg_Salary',
            template='plotly_dark',
            color_continuous_scale='Viridis',
            labels={'Avg_Salary': 'Avg Salary (LPA)', 'Skill': 'Skill Name'}
        )
        fig_sal_skill.update_traces(texttemplate='₹%{text:.2f} LPA', textposition='outside')
        fig_sal_skill.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            xaxis=dict(gridcolor="#1E293B"),
            yaxis=dict(gridcolor="#1E293B")
        )
        st.plotly_chart(fig_sal_skill, use_container_width=True)

    st.markdown("---")
    
    # Interactive Skill Deep-Dive Explorer
    st.markdown("<h3 style='color: #FFFFFF !important;'>🔍 Skill Performance Matrix & Explorer</h3>", unsafe_allow_html=True)
    
    col_sel, col_empty = st.columns([1, 2])
    with col_sel:
        selected_skill = st.selectbox("Select a Skill to Analyze", sorted(skills_summary['Skill'].unique()))
        
    skill_info = skills_summary[skills_summary['Skill'] == selected_skill].iloc[0]
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Skill Name", selected_skill)
    m2.metric("Total Students with Skill", f"{skill_info['Total_Students']:,}")
    m3.metric("Placement Rate", f"{skill_info['Placement_Rate']:.1f}%")
    m4.metric("Average Salary Boost", f"₹{skill_info['Avg_Salary']:.2f} LPA")
    
    # Skill vs Placement Scatter Bubble Chart (Dark Theme)
    fig_bubble = px.scatter(
        skills_summary,
        x='Placement_Rate',
        y='Avg_Salary',
        size='Total_Students',
        color='Avg_Employer_Pref',
        text='Skill',
        template='plotly_dark',
        labels={'Placement_Rate': 'Placement Rate (%)', 'Avg_Salary': 'Average Salary (LPA)'},
        color_continuous_scale='Plasma'
    )
    fig_bubble.update_traces(textposition='top center')
    fig_bubble.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        xaxis=dict(gridcolor="#1E293B"),
        yaxis=dict(gridcolor="#1E293B")
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
