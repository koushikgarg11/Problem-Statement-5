import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render(df):
    st.markdown("<h3 style='color: #F8FAFC; font-weight: 800;'>💰 Placement & Salary Analysis Dashboard</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>Detailed Breakdown of Salary Distributions, Time-to-Offer, and Internship Duration Conversion</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Visualizations Row 1: Impact of Number of Internships & Certifications
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<h4 style='color: #FFFFFF !important;'>Placement Rate & Salary vs Number of Internships</h4>", unsafe_allow_html=True)
        multi_int = df.groupby('Number_of_Internships').agg(
            Placement_Rate=('Placement_Status', lambda x: (x == 'Placed').mean() * 100),
            Avg_Salary=('Salary_Package_LPA', lambda x: x[x > 0].mean())
        ).reset_index()
        
        fig_multi_int = go.Figure()
        fig_multi_int.add_trace(go.Bar(
            x=multi_int['Number_of_Internships'],
            y=multi_int['Placement_Rate'],
            name='Placement Rate (%)',
            text=multi_int['Placement_Rate'].round(1),
            textposition='auto',
            marker_color='#0288D1'
        ))
        fig_multi_int.add_trace(go.Scatter(
            x=multi_int['Number_of_Internships'],
            y=multi_int['Avg_Salary'],
            name='Avg Salary (LPA)',
            mode='lines+markers+text',
            text=multi_int['Avg_Salary'].round(2),
            textposition='top center',
            yaxis='y2',
            line=dict(color='#FF6D00', width=3)
        ))
        fig_multi_int.update_layout(
            template='plotly_dark',
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            xaxis=dict(title='Number of Internships Completed', gridcolor='#1E293B'),
            yaxis=dict(title='Placement Rate (%)', range=[0, 115], gridcolor='#1E293B'),
            yaxis2=dict(title='Avg Salary (LPA)', overlaying='y', side='right', range=[0, 20]),
            legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig_multi_int, use_container_width=True)
        
    with c2:
        st.markdown("<h4 style='color: #FFFFFF !important;'>Placement Rate & Salary vs Number of Certifications</h4>", unsafe_allow_html=True)
        multi_cert = df.groupby('Number_of_Certifications').agg(
            Placement_Rate=('Placement_Status', lambda x: (x == 'Placed').mean() * 100),
            Avg_Salary=('Salary_Package_LPA', lambda x: x[x > 0].mean())
        ).reset_index()
        
        fig_multi_cert = go.Figure()
        fig_multi_cert.add_trace(go.Bar(
            x=multi_cert['Number_of_Certifications'],
            y=multi_cert['Placement_Rate'],
            name='Placement Rate (%)',
            text=multi_cert['Placement_Rate'].round(1),
            textposition='auto',
            marker_color='#7B1FA2'
        ))
        fig_multi_cert.add_trace(go.Scatter(
            x=multi_cert['Number_of_Certifications'],
            y=multi_cert['Avg_Salary'],
            name='Avg Salary (LPA)',
            mode='lines+markers+text',
            text=multi_cert['Avg_Salary'].round(2),
            textposition='top center',
            yaxis='y2',
            line=dict(color='#00E676', width=3)
        ))
        fig_multi_cert.update_layout(
            template='plotly_dark',
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            xaxis=dict(title='Number of Certifications Earned', gridcolor='#1E293B'),
            yaxis=dict(title='Placement Rate (%)', range=[0, 115], gridcolor='#1E293B'),
            yaxis2=dict(title='Avg Salary (LPA)', overlaying='y', side='right', range=[0, 20]),
            legend=dict(x=0.01, y=0.99)
        )
        st.plotly_chart(fig_multi_cert, use_container_width=True)

    st.markdown("---")
    
    # Visualizations Row 2: Duration vs PPO Conversion & Time to Offer
    r2_c1, r2_c2 = st.columns(2)
    
    with r2_c1:
        st.markdown("<h4 style='color: #FFFFFF !important;'>Internship Duration (Months) vs PPO Conversion Rate</h4>", unsafe_allow_html=True)
        intern_df = df[df['Number_of_Internships'] > 0]
        dur_df = intern_df.groupby('Internship_Duration_Months').agg(
            Total=('Student_ID', 'count'),
            PPO_Count=('PPO_Conversion_Status', lambda x: (x == 'Direct PPO (Pre-Placement Offer)').sum())
        ).reset_index()
        dur_df['PPO_Conversion_Rate'] = (dur_df['PPO_Count'] / dur_df['Total'] * 100).round(1)
        
        fig_dur = px.bar(
            dur_df,
            x='Internship_Duration_Months',
            y='PPO_Conversion_Rate',
            text='PPO_Conversion_Rate',
            template='plotly_dark',
            labels={'Internship_Duration_Months': 'Internship Duration (Months)', 'PPO_Conversion_Rate': 'PPO Conversion Rate (%)'},
            color='PPO_Conversion_Rate',
            color_continuous_scale='Viridis'
        )
        fig_dur.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_dur.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            yaxis=dict(range=[0, 100], gridcolor='#1E293B'),
            xaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_dur, use_container_width=True)
        
    with r2_c2:
        st.markdown("<h4 style='color: #FFFFFF !important;'>Speed of Job Placement: Days to Offer</h4>", unsafe_allow_html=True)
        placed_df = df[df['Placement_Status'] == 'Placed']
        fig_time = px.histogram(
            placed_df,
            x='Time_to_Offer_Days',
            color='Experience_Profile',
            nbins=20,
            marginal="box",
            template='plotly_dark',
            labels={'Time_to_Offer_Days': 'Days to Job Offer from Graduation'},
            color_discrete_map={
                'Both (Hybrid)': '#00F2FE',
                'Internship Only': '#38BDF8',
                'Certification Only': '#F59E0B',
                'Neither': '#EF4444'
            }
        )
        fig_time.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF"),
            xaxis=dict(gridcolor='#1E293B'),
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_time, use_container_width=True)
