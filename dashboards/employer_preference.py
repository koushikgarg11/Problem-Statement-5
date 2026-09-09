import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

def render(df):
    st.title("🏢 Employer Preference Dashboard")
    st.markdown("##### Analytical Insights into Recruiting Panel Preferences and What Employers Value Most")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    avg_int_pref = df[df['Number_of_Internships'] > 0]['Employer_Preference_Score'].mean()
    avg_cert_pref = df[df['Number_of_Certifications'] > 0]['Employer_Preference_Score'].mean()
    avg_hybrid_pref = df[df['Experience_Profile'] == 'Both (Hybrid)']['Employer_Preference_Score'].mean()
    
    col1.metric("Employer Score (Internships)", f"{avg_int_pref:.2f} / 10")
    col2.metric("Employer Score (Certifications)", f"{avg_cert_pref:.2f} / 10")
    col3.metric("Employer Score (Hybrid Profile)", f"{avg_hybrid_pref:.2f} / 10", f"+{avg_hybrid_pref - avg_cert_pref:.2f} vs Cert Only")
    
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Employer Rating Distribution across Domains")
        domain_pref = df[df['Internship_Domain'] != 'None'].groupby('Internship_Domain')['Employer_Preference_Score'].mean().reset_index()
        domain_pref = domain_pref.sort_values(by='Employer_Preference_Score', ascending=True)
        
        fig_dom = px.bar(
            domain_pref,
            x='Employer_Preference_Score',
            y='Internship_Domain',
            orientation='h',
            text=domain_pref['Employer_Preference_Score'].round(2),
            color='Employer_Preference_Score',
            color_continuous_scale='Teal',
            labels={'Employer_Preference_Score': 'Avg Employer Preference (1-10)', 'Internship_Domain': 'Domain'}
        )
        fig_dom.update_traces(textposition='outside')
        st.plotly_chart(fig_dom, use_container_width=True)
        
    with c2:
        st.subheader("Machine Learning Feature Importance (What Employers Value Most)")
        
        try:
            with open("data/summary_metrics.json", "r") as f:
                metrics_data = json.load(f)
            top_drivers = pd.DataFrame(metrics_data['top_placement_drivers'])
            top_drivers['Importance_Pct'] = (top_drivers['Importance'] * 100).round(1)
            top_drivers['Feature_Clean'] = top_drivers['Feature'].str.replace('_', ' ')
            top_drivers = top_drivers.sort_values(by='Importance_Pct', ascending=True)
            
            fig_imp = px.bar(
                top_drivers,
                x='Importance_Pct',
                y='Feature_Clean',
                orientation='h',
                text='Importance_Pct',
                color='Importance_Pct',
                color_continuous_scale='Magma',
                labels={'Importance_Pct': 'Importance Score (%)', 'Feature_Clean': 'Candidate Attribute'}
            )
            fig_imp.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig_imp, use_container_width=True)
        except Exception:
            st.info("Feature importance data loading...")

    st.markdown("---")
    
    st.subheader("Employer Score Heatmap: Internship Domain vs Certification Provider")
    heatmap_df = df[(df['Internship_Domain'] != 'None') & (df['Certification_Provider'] != 'None')]
    
    # Explode certification providers for multi-provider strings
    heatmap_df = heatmap_df.assign(Provider=heatmap_df['Certification_Provider'].str.split('; ')).explode('Provider')
    heatmap_df = heatmap_df[heatmap_df['Provider'] != 'None']
    
    pivot_heat = heatmap_df.pivot_table(
        index='Internship_Domain', 
        columns='Provider', 
        values='Employer_Preference_Score', 
        aggfunc='mean'
    ).fillna(0)
    
    fig_heat = px.imshow(
        pivot_heat,
        labels=dict(x="Certification Provider", y="Internship Domain", color="Employer Rating"),
        x=pivot_heat.columns,
        y=pivot_heat.index,
        color_continuous_scale="Blues",
        aspect="auto"
    )
    st.plotly_chart(fig_heat, use_container_width=True)
