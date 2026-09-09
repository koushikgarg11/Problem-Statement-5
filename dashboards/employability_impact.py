import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render(df):
    st.markdown("<h3 style='color: #F8FAFC; font-weight: 700; margin-top: 10px;'>📊 Executive Summary & Employability Overview</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Visualizations Row 1
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<h4 style='color: #CBD5E1;'>Placement Rate by Experience Profile</h4>", unsafe_allow_html=True)
        profile_placed = df.groupby('Experience_Profile').agg(
            Total=('Student_ID', 'count'),
            Placed=('Placement_Status', lambda x: (x == 'Placed').sum()),
            Avg_Salary=('Salary_Package_LPA', lambda x: x[x > 0].mean())
        ).reset_index()
        profile_placed['Placement_Rate'] = (profile_placed['Placed'] / profile_placed['Total'] * 100).round(1)
        
        fig_profile = px.bar(
            profile_placed,
            x='Experience_Profile',
            y='Placement_Rate',
            color='Experience_Profile',
            text='Placement_Rate',
            template='plotly_dark',
            labels={'Placement_Rate': 'Placement Rate (%)', 'Experience_Profile': 'Profile Group'},
            color_discrete_map={
                'Both (Hybrid)': '#00F2FE',
                'Internship Only': '#38BDF8',
                'Certification Only': '#F59E0B',
                'Neither': '#EF4444'
            }
        )
        fig_profile.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_color='#1E293B', marker_line_width=1.5)
        fig_profile.update_layout(
            showlegend=False, 
            yaxis=dict(range=[0, 115], gridcolor='#1E293B'),
            xaxis=dict(gridcolor='#1E293B'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_profile, use_container_width=True)
        
    with c2:
        st.markdown("<h4 style='color: #CBD5E1;'>Salary Package Distribution (LPA)</h4>", unsafe_allow_html=True)
        fig_sal = px.box(
            df[df['Placement_Status'] == 'Placed'],
            x='Experience_Profile',
            y='Salary_Package_LPA',
            color='Experience_Profile',
            points="all",
            template='plotly_dark',
            labels={'Salary_Package_LPA': 'Salary (LPA)', 'Experience_Profile': 'Profile Group'},
            color_discrete_map={
                'Both (Hybrid)': '#00F2FE',
                'Internship Only': '#38BDF8',
                'Certification Only': '#F59E0B',
                'Neither': '#EF4444'
            }
        )
        fig_sal.update_layout(
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_sal, use_container_width=True)
        
    st.markdown("---")
    
    # Visualizations Row 2: College Tier Breakdown & Degree Level
    r2_c1, r2_c2 = st.columns(2)
    
    with r2_c1:
        st.markdown("<h4 style='color: #CBD5E1;'>Placement Success by College Category</h4>", unsafe_allow_html=True)
        tier_df = df.groupby(['College_Name', 'Experience_Profile']).agg(
            Placement_Rate=('Placement_Status', lambda x: (x == 'Placed').mean() * 100)
        ).reset_index()
        
        fig_tier = px.bar(
            tier_df,
            x='College_Name',
            y='Placement_Rate',
            color='Experience_Profile',
            barmode='group',
            template='plotly_dark',
            labels={'Placement_Rate': 'Placement Rate (%)', 'College_Name': 'College Category'},
            color_discrete_map={
                'Both (Hybrid)': '#00F2FE',
                'Internship Only': '#38BDF8',
                'Certification Only': '#F59E0B',
                'Neither': '#EF4444'
            }
        )
        fig_tier.update_layout(
            xaxis_tickangle=-20,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_tier, use_container_width=True)
        
    with r2_c2:
        st.markdown("<h4 style='color: #CBD5E1;'>Placement Status Distribution by Degree</h4>", unsafe_allow_html=True)
        edu_df = df.groupby(['Education_Level', 'Placement_Status']).size().reset_index(name='Count')
        fig_edu = px.sunburst(
            edu_df,
            path=['Education_Level', 'Placement_Status'],
            values='Count',
            color='Placement_Status',
            template='plotly_dark',
            color_discrete_map={'Placed': '#10B981', 'Unplaced': '#EF4444'}
        )
        fig_edu.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_edu, use_container_width=True)
