import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render(df):
    st.markdown("<h3 style='color: #F8FAFC; font-weight: 800;'>🎯 AI Student Career Pathway Advisor</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>Personalized AI Career Outcome Predictor & Individual Student Action Roadmap</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h4 style='color: #00E676;'>🤖 Student Profile Input & Live Career Predictor</h4>", unsafe_allow_html=True)
    st.markdown("<p style='color: #CBD5E1;'>Adjust your student profile parameters below to calculate your predicted placement probability, estimated salary package, and personalized AI action plan:</p>", unsafe_allow_html=True)
    
    c_in1, c_in2, c_in3, c_in4 = st.columns(4)
    
    with c_in1:
        user_degree = st.selectbox("Education Level", df['Education_Level'].unique())
        user_branch = st.selectbox("Branch / Domain", df['Course_Branch'].unique())
        
    with c_in2:
        user_college = st.selectbox("College Category", df['College_Name'].unique())
        user_target_domain = st.selectbox("Target Career Field", [
            "Software Engineering", "Data Science & Analytics", "Cloud & DevOps", 
            "Artificial Intelligence / ML", "Cyber Security", "Product Management"
        ])
        
    with c_in3:
        user_certs = st.number_input("Certifications Earned", min_value=0, max_value=6, value=1)
        user_interns = st.number_input("Internships Completed", min_value=0, max_value=4, value=1)
        
    with c_in4:
        user_duration = st.selectbox("Total Internship Duration (Months)", [0, 2, 3, 6, 9, 12], index=2)
        user_gpa_score = st.slider("Academic Score (1-100)", 50, 100, 78)

    # Predictive Logic Engine
    tier_bonus = 12 if "Tier 1" in user_college else (6 if "Tier 2" in user_college else 0)
    practical_est = min(100, int(30 + user_interns * 18 + user_duration * 2.5 + tier_bonus))
    theoretical_est = min(100, int(40 + user_certs * 12 + tier_bonus))
    employer_rating_est = min(10.0, max(2.0, round(3.5 + (user_interns * 1.5) + (user_duration * 0.25) + (user_certs * 0.4) + (tier_bonus * 0.08), 1)))
    
    # Calculate probability
    logit = -2.2 + (user_interns * 1.3) + (user_duration * 0.15) + (user_certs * 0.35) + (tier_bonus * 0.05) + (employer_rating_est * 0.4)
    placement_prob = 1 / (1 + np.exp(-logit)) * 100
    
    est_salary_min = max(3.5, round(4.5 + tier_bonus*0.35 + user_interns*2.2 + user_duration*0.45 + user_certs*0.6 - 1.2, 2))
    est_salary_max = round(est_salary_min + 3.2, 2)
    
    ppo_prob = round(min(85, max(5, user_duration * 6.5 + user_interns * 15)), 1)
    
    st.markdown("<h4 style='color: #FFFFFF !important; margin-top: 16px;'>🎯 Your Predicted Career Outcomes:</h4>", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    
    p1.metric("Placement Probability", f"{placement_prob:.1f}%")
    p2.metric("Estimated Salary Range", f"₹{est_salary_min:.1f} - {est_salary_max:.1f} LPA")
    p3.metric("PPO Conversion Chance", f"{ppo_prob:.1f}%")
    p4.metric("Employer Preference Score", f"{employer_rating_est:.1f} / 10")
    
    # AI Personalized Strategic Advice Box for Students
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    if user_interns == 0 and user_certs > 0:
        st.markdown("""
            <div style="background: rgba(245, 158, 11, 0.15); border: 2px solid #F59E0B; border-radius: 12px; padding: 18px; color: #FFFFFF !important;">
                <h4 style="color: #F59E0B !important; margin: 0 0 8px 0;">⚠️ AI Personal Guidance: Priority Action Required!</h4>
                You have earned certifications but have <strong>zero internship experience</strong>.<br/>
                • <strong>Impact</strong>: Completing just <strong>1 internship (3-6 months)</strong> will boost your placement odds from ~69% to <strong>97%+</strong> and raise your starting salary by <strong>+₹4.37 LPA</strong>.<br/>
                • <strong>Action Item</strong>: Pause further certifications for now and focus 100% of your effort on securing a 3-month industry internship.
            </div>
        """, unsafe_allow_html=True)
    elif user_interns > 0 and user_certs == 0:
        st.markdown("""
            <div style="background: rgba(56, 189, 248, 0.15); border: 2px solid #38BDF8; border-radius: 12px; padding: 18px; color: #FFFFFF !important;">
                <h4 style="color: #38BDF8 !important; margin: 0 0 8px 0;">ℹ️ AI Personal Guidance: Upgrade to Tier-1 Package!</h4>
                Great job on securing practical internship experience!<br/>
                • <strong>Impact</strong>: You already qualify for high placement odds (~97%). To unlock premium Tier-1 salary brackets (₹14+ LPA), pair your experience with 1 top vendor certification (AWS / Google Cloud / Azure).<br/>
                • <strong>Action Item</strong>: Earn 1 specialized industry certification aligned with your target role to maximize your salary package.
            </div>
        """, unsafe_allow_html=True)
    elif user_interns > 0 and user_certs > 0:
        st.markdown("""
            <div style="background: rgba(0, 230, 118, 0.15); border: 2px solid #00E676; border-radius: 12px; padding: 18px; color: #FFFFFF !important;">
                <h4 style="color: #00E676 !important; margin: 0 0 8px 0;">🌟 AI Personal Guidance: Top 5% Hybrid Candidate Profile!</h4>
                Congratulations! You possess a <strong>Hybrid Profile</strong> (Both Internships & Certifications).<br/>
                • <strong>Impact</strong>: You belong to the highest employability bracket with <strong>98.3% placement odds</strong> and top starting packages (₹14.37 LPA average).<br/>
                • <strong>Action Item</strong>: Focus on advanced System Design, LeetCode/Problem Solving, and convert your internship into a Direct Pre-Placement Offer (PPO).
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.15); border: 2px solid #EF4444; border-radius: 12px; padding: 18px; color: #FFFFFF !important;">
                <h4 style="color: #EF4444 !important; margin: 0 0 8px 0;">🚨 AI Personal Guidance: High Employability Risk Profile!</h4>
                You currently have no internships and no industry certifications.<br/>
                • <strong>Impact</strong>: Placement probability is below 46% with low average starting packages.<br/>
                • <strong>Action Item</strong>: Build 2 hands-on technical portfolio projects immediately, enroll in foundational skill bootcamps, and apply for entry-level internships.
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # INDIVIDUAL STUDENT PERSONAL ROADMAP & ACTION PLAN
    st.markdown("<h3 style='color: #FFFFFF !important;'>🎓 Personal Student Career Roadmap & Success Blueprint</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>Follow this 4-step data-backed career execution plan to maximize your placement speed and salary package:</p>", unsafe_allow_html=True)
    
    rec_c1, rec_c2 = st.columns(2)
    
    with rec_c1:
        st.markdown("""
        <div style="background: #09101F; border: 1px solid #1E293B; border-radius: 14px; padding: 20px; margin-bottom: 16px;">
            <h4 style="color: #00E676 !important; margin-top: 0;">Phase 1: Practical Internship Focus (Highest Value)</h4>
            <p style="color: #FFFFFF !important; line-height: 1.6;">
                • <strong>Data Insight</strong>: Internships provide a <strong>+27.8% higher placement rate</strong> than certifications alone.<br/>
                • <strong>Your Action Plan</strong>: Complete at least <strong>1 to 2 internships</strong> lasting 3 to 6 months before your final semester. Focus on solving real customer/business problems rather than basic observation.
            </p>
        </div>
        
        <div style="background: #09101F; border: 1px solid #1E293B; border-radius: 14px; padding: 20px; margin-bottom: 16px;">
            <h4 style="color: #38BDF8 !important; margin-top: 0;">Phase 2: Aim for 6+ Month Internships for Direct PPO</h4>
            <p style="color: #FFFFFF !important; line-height: 1.6;">
                • <strong>Data Insight</strong>: Internships lasting <strong>6 months or longer</strong> yield a <strong>65%+ Direct PPO conversion rate</strong>.<br/>
                • <strong>Your Action Plan</strong>: Negotiate long-term internship extensions. Converting an internship into a PPO eliminates post-graduation job search stress and reduces days-to-offer to zero.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with rec_c2:
        st.markdown("""
        <div style="background: #09101F; border: 1px solid #1E293B; border-radius: 14px; padding: 20px; margin-bottom: 16px;">
            <h4 style="color: #FBBF24 !important; margin-top: 0;">Phase 3: Build a Dual-Credential "Hybrid" Profile</h4>
            <p style="color: #FFFFFF !important; line-height: 1.6;">
                • <strong>Data Insight</strong>: Candidates with <strong>BOTH</strong> internships and certifications achieve <strong>98.32% placement</strong> and peak packages (₹14.37 LPA).<br/>
                • <strong>Your Action Plan</strong>: Combine your practical internship experience with 1-2 recognized certifications (AWS, Azure, Meta, Google Cloud) to stand out in top candidate pools.
            </p>
        </div>
        
        <div style="background: #09101F; border: 1px solid #1E293B; border-radius: 14px; padding: 20px; margin-bottom: 16px;">
            <h4 style="color: #C084FC !important; margin-top: 0;">Phase 4: Master High-Demand Core Skills</h4>
            <p style="color: #FFFFFF !important; line-height: 1.6;">
                • <strong>Data Insight</strong>: Skills in <strong>Python, SQL, Cloud Architecture (AWS), and Machine Learning</strong> command the highest salary premiums.<br/>
                • <strong>Your Action Plan</strong>: Include quantifiable metrics on your resume showcasing these skills (e.g. <em>"Built automated SQL data pipeline processing 50k records daily"</em>).
            </p>
        </div>
        """, unsafe_allow_html=True)
