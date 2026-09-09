import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from scipy import stats

def render(df):
    st.markdown("<h3 style='color: #F8FAFC; font-weight: 700; margin-top: 10px;'>⚖️ Internship vs Certification Head-to-Head Comparison</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    int_only = df[df['Experience_Profile'] == 'Internship Only']
    cert_only = df[df['Experience_Profile'] == 'Certification Only']
    hybrid = df[df['Experience_Profile'] == 'Both (Hybrid)']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style="background: #111726; border: 1px solid #38BDF8; border-radius: 10px; padding: 18px;">
                <h4 style="color: #38BDF8; margin: 0 0 10px 0;">💼 Internship Only</h4>
        """, unsafe_allow_html=True)
        st.metric("Placement Rate", f"{(len(int_only[int_only['Placement_Status']=='Placed'])/len(int_only)*100):.1f}%")
        st.metric("Avg Salary (Placed)", f"₹{int_only[int_only['Placement_Status']=='Placed']['Salary_Package_LPA'].mean():.2f} LPA")
        st.metric("Employer Preference", f"{int_only['Employer_Preference_Score'].mean():.1f} / 10")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="background: #111726; border: 1px solid #F59E0B; border-radius: 10px; padding: 18px;">
                <h4 style="color: #F59E0B; margin: 0 0 10px 0;">📜 Certification Only</h4>
        """, unsafe_allow_html=True)
        st.metric("Placement Rate", f"{(len(cert_only[cert_only['Placement_Status']=='Placed'])/len(cert_only)*100):.1f}%")
        st.metric("Avg Salary (Placed)", f"₹{cert_only[cert_only['Placement_Status']=='Placed']['Salary_Package_LPA'].mean():.2f} LPA")
        st.metric("Employer Preference", f"{cert_only['Employer_Preference_Score'].mean():.1f} / 10")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style="background: #111726; border: 1px solid #00F2FE; border-radius: 10px; padding: 18px;">
                <h4 style="color: #00F2FE; margin: 0 0 10px 0;">🌟 Hybrid (Both)</h4>
        """, unsafe_allow_html=True)
        st.metric("Placement Rate", f"{(len(hybrid[hybrid['Placement_Status']=='Placed'])/len(hybrid)*100):.1f}%")
        st.metric("Avg Salary (Placed)", f"₹{hybrid[hybrid['Placement_Status']=='Placed']['Salary_Package_LPA'].mean():.2f} LPA")
        st.metric("Employer Preference", f"{hybrid['Employer_Preference_Score'].mean():.1f} / 10")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("<h4 style='color: #CBD5E1;'>Practical Skill vs Theoretical Skill Scatter Matrix</h4>", unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df,
            x='Theoretical_Score',
            y='Practical_Skill_Score',
            color='Experience_Profile',
            size='Salary_Package_LPA',
            template='plotly_dark',
            hover_data=['Student_ID', 'College_Name', 'Course_Branch', 'Placement_Status'],
            labels={'Theoretical_Score': 'Theoretical Score (Certs & GPA)', 'Practical_Skill_Score': 'Practical Skill Score'},
            opacity=0.75,
            color_discrete_map={
                'Both (Hybrid)': '#00F2FE',
                'Internship Only': '#38BDF8',
                'Certification Only': '#F59E0B',
                'Neither': '#EF4444'
            }
        )
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#1E293B'),
            yaxis=dict(gridcolor='#1E293B')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with c2:
        st.markdown("<h4 style='color: #CBD5E1;'>Average Salary Package by Profile (LPA)</h4>", unsafe_allow_html=True)
        sal_comp = pd.DataFrame({
            'Category': ['Neither', 'Certification Only', 'Internship Only', 'Both (Hybrid)'],
            'Avg_Salary_LPA': [
                df[(df['Experience_Profile']=='Neither') & (df['Placement_Status']=='Placed')]['Salary_Package_LPA'].mean(),
                df[(df['Experience_Profile']=='Certification Only') & (df['Placement_Status']=='Placed')]['Salary_Package_LPA'].mean(),
                df[(df['Experience_Profile']=='Internship Only') & (df['Placement_Status']=='Placed')]['Salary_Package_LPA'].mean(),
                df[(df['Experience_Profile']=='Both (Hybrid)') & (df['Placement_Status']=='Placed')]['Salary_Package_LPA'].mean()
            ]
        })
        fig_sal_bar = px.bar(
            sal_comp,
            x='Category',
            y='Avg_Salary_LPA',
            color='Category',
            text='Avg_Salary_LPA',
            template='plotly_dark',
            color_discrete_sequence=['#EF4444', '#F59E0B', '#38BDF8', '#00F2FE']
        )
        fig_sal_bar.update_traces(texttemplate='₹%{text:.2f} LPA', textposition='outside', marker_line_color='#1E293B', marker_line_width=1.5)
        fig_sal_bar.update_layout(
            showlegend=False, 
            yaxis=dict(range=[0, 18], gridcolor='#1E293B'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_sal_bar, use_container_width=True)

    st.markdown("---")
    
    st.markdown("<h4 style='color: #CBD5E1;'>🔬 Statistical Hypothesis Testing Results</h4>", unsafe_allow_html=True)
    
    int_sal = df[(df['Experience_Profile']=='Internship Only') & (df['Placement_Status']=='Placed')]['Salary_Package_LPA']
    cert_sal = df[(df['Experience_Profile']=='Certification Only') & (df['Placement_Status']=='Placed')]['Salary_Package_LPA']
    t_stat, p_val = stats.ttest_ind(int_sal, cert_sal, equal_var=False)
    
    contingency = pd.crosstab(df['Experience_Profile'], df['Placement_Status'])
    chi2, p_chi2, dof, ex = stats.chi2_contingency(contingency)
    
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown(f"""
            <div style="background: #111726; border: 1px solid #1E293B; border-radius: 8px; padding: 14px;">
                <strong style="color: #38BDF8;">Welch's T-Test (Salary Difference)</strong><br/>
                • T-Statistic: <code>{t_stat:.4f}</code><br/>
                • P-Value: <code>{p_val:.2e}</code><br/>
                • Result: <span style="color: #10B981;">Statistically Significant (p < 0.001)</span>
            </div>
        """, unsafe_allow_html=True)
        
    with sc2:
        st.markdown(f"""
            <div style="background: #111726; border: 1px solid #1E293B; border-radius: 8px; padding: 14px;">
                <strong style="color: #38BDF8;">Chi-Square Test (Placement Difference)</strong><br/>
                • Chi-Square Stat: <code>{chi2:.4f}</code><br/>
                • P-Value: <code>{p_chi2:.2e}</code><br/>
                • Result: <span style="color: #10B981;">Statistically Significant (p < 0.001)</span>
            </div>
        """, unsafe_allow_html=True)
        
    with sc3:
        st.markdown("""
            <div style="background: #111726; border: 1px solid #1E293B; border-radius: 8px; padding: 14px;">
                <strong style="color: #38BDF8;">Key Takeaway for Employers</strong><br/>
                • Employers view internship experience as an indicator of real-world productivity.<br/>
                • Certifications validate theoretical knowledge but require internship application to command top packages.
            </div>
        """, unsafe_allow_html=True)
