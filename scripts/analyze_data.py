import os
import json
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import RandomForestClassifier

def run_analytical_pipeline(csv_path="data/employability_dataset.csv"):
    print("Starting analysis pipeline...")
    df = pd.read_csv(csv_path)
    
    # 1. Overall placement rate by Experience Profile
    df['Is_Placed'] = (df['Placement_Status'] == 'Placed').astype(int)
    profile_placement = df.groupby('Experience_Profile').agg(
        Total_Students=('Student_ID', 'count'),
        Placed_Count=('Is_Placed', 'sum'),
        Placement_Rate=('Is_Placed', 'mean'),
        Avg_Salary_All=('Salary_Package_LPA', 'mean')
    ).reset_index()
    
    placed_df = df[df['Is_Placed'] == 1]
    salary_placed = placed_df.groupby('Experience_Profile')['Salary_Package_LPA'].agg(['mean', 'median', 'std', 'count']).reset_index()
    salary_placed.columns = ['Experience_Profile', 'Avg_Salary_Placed', 'Median_Salary_Placed', 'Std_Salary_Placed', 'Count_Placed']
    
    profile_summary = pd.merge(profile_placement, salary_placed, on='Experience_Profile', how='left')
    profile_summary['Placement_Rate_Pct'] = (profile_summary['Placement_Rate'] * 100).round(2)
    profile_summary['Avg_Salary_Placed'] = profile_summary['Avg_Salary_Placed'].round(2)
    
    # Head-to-Head: Internship Only vs Certification Only
    int_only = df[df['Experience_Profile'] == 'Internship Only']
    cert_only = df[df['Experience_Profile'] == 'Certification Only']
    hybrid = df[df['Experience_Profile'] == 'Both (Hybrid)']
    
    h2h_metrics = {
        "internship_only": {
            "placement_rate": round(int_only['Is_Placed'].mean() * 100, 2),
            "avg_salary_placed": round(int_only[int_only['Is_Placed'] == 1]['Salary_Package_LPA'].mean(), 2),
            "avg_employer_pref": round(int_only['Employer_Preference_Score'].mean(), 2)
        },
        "certification_only": {
            "placement_rate": round(cert_only['Is_Placed'].mean() * 100, 2),
            "avg_salary_placed": round(cert_only[cert_only['Is_Placed'] == 1]['Salary_Package_LPA'].mean(), 2),
            "avg_employer_pref": round(cert_only['Employer_Preference_Score'].mean(), 2)
        },
        "hybrid_both": {
            "placement_rate": round(hybrid['Is_Placed'].mean() * 100, 2),
            "avg_salary_placed": round(hybrid[hybrid['Is_Placed'] == 1]['Salary_Package_LPA'].mean(), 2),
            "avg_employer_pref": round(hybrid['Employer_Preference_Score'].mean(), 2)
        }
    }
    
    # Statistical Significance Test (T-Test & Chi-Square)
    t_stat_sal, p_val_sal = stats.ttest_ind(
        int_only[int_only['Is_Placed'] == 1]['Salary_Package_LPA'],
        cert_only[cert_only['Is_Placed'] == 1]['Salary_Package_LPA'],
        equal_var=False
    )
    
    contingency_table = pd.crosstab(df['Experience_Profile'], df['Is_Placed'])
    chi2, p_val_chi2, dof, ex = stats.chi2_contingency(contingency_table)
    
    stat_tests = {
        "t_test_salary": {"t_statistic": round(float(t_stat_sal), 4), "p_value": float(p_val_sal), "significant": bool(p_val_sal < 0.05)},
        "chi2_placement": {"chi2_statistic": round(float(chi2), 4), "p_value": float(p_val_chi2), "significant": bool(p_val_chi2 < 0.05)}
    }
    
    # 3. Internship to Job Conversion Rates
    intern_students = df[df['Number_of_Internships'] > 0]
    ppo_summary = intern_students.groupby('PPO_Conversion_Status').agg(
        Count=('Student_ID', 'count')
    ).reset_index()
    ppo_summary['Percentage'] = (ppo_summary['Count'] / len(intern_students) * 100).round(2)
    
    dur_ppo = intern_students.groupby('Internship_Duration_Months').agg(
        Total=('Student_ID', 'count'),
        Direct_PPO=('PPO_Conversion_Status', lambda x: (x == 'Direct PPO (Pre-Placement Offer)').sum()),
        Placement_Rate=('Is_Placed', 'mean'),
        Avg_Salary=('Salary_Package_LPA', lambda x: x[x > 0].mean())
    ).reset_index()
    dur_ppo['PPO_Conversion_Rate_Pct'] = (dur_ppo['Direct_PPO'] / dur_ppo['Total'] * 100).round(2)
    dur_ppo['Placement_Rate_Pct'] = (dur_ppo['Placement_Rate'] * 100).round(2)
    dur_ppo['Avg_Salary'] = dur_ppo['Avg_Salary'].round(2)
    
    # 4. Employer Preference for Certifications vs Internships
    emp_pref_by_group = df.groupby('Experience_Profile')['Employer_Preference_Score'].agg(['mean', 'median', 'std']).reset_index()
    emp_pref_by_group.columns = ['Experience_Profile', 'Mean_Employer_Preference', 'Median_Pref', 'Std_Pref']
    emp_pref_by_group['Mean_Employer_Preference'] = emp_pref_by_group['Mean_Employer_Preference'].round(2)
    
    # 5. Multiple Internships vs Multiple Certifications Impact
    multi_int = df.groupby('Number_of_Internships').agg(
        Student_Count=('Student_ID', 'count'),
        Placement_Rate=('Is_Placed', 'mean'),
        Avg_Salary=('Salary_Package_LPA', lambda x: x[x > 0].mean()),
        Avg_Employer_Pref=('Employer_Preference_Score', 'mean')
    ).reset_index()
    multi_int['Placement_Rate_Pct'] = (multi_int['Placement_Rate'] * 100).round(2)
    multi_int['Avg_Salary'] = multi_int['Avg_Salary'].round(2)
    multi_int['Avg_Employer_Pref'] = multi_int['Avg_Employer_Pref'].round(2)
    
    multi_cert = df.groupby('Number_of_Certifications').agg(
        Student_Count=('Student_ID', 'count'),
        Placement_Rate=('Is_Placed', 'mean'),
        Avg_Salary=('Salary_Package_LPA', lambda x: x[x > 0].mean()),
        Avg_Employer_Pref=('Employer_Preference_Score', 'mean')
    ).reset_index()
    multi_cert['Placement_Rate_Pct'] = (multi_cert['Placement_Rate'] * 100).round(2)
    multi_cert['Avg_Salary'] = multi_cert['Avg_Salary'].round(2)
    multi_cert['Avg_Employer_Pref'] = multi_cert['Avg_Employer_Pref'].round(2)
    
    # 6. Optimized Skills analysis using vectorized explode
    df_skills = df.assign(Skill=df['Primary_Skills'].str.split(', ')).explode('Skill')
    skills_agg = df_skills.groupby('Skill').agg(
        Total_Students=('Student_ID', 'count'),
        Placed_Students=('Is_Placed', 'sum'),
        Placement_Rate=('Is_Placed', 'mean'),
        Avg_Salary_With_Skill=('Salary_Package_LPA', lambda x: x[x > 0].mean())
    ).reset_index()
    
    skills_agg['Skill_Placement_Rate_Pct'] = (skills_agg['Placement_Rate'] * 100).round(2)
    skills_agg['Avg_Salary_With_Skill'] = skills_agg['Avg_Salary_With_Skill'].round(2)
    skills_impact = skills_agg.sort_values(by='Placed_Students', ascending=False)
    
    # 7. Machine Learning Feature Importance
    X_features = pd.get_dummies(df[[
        'Age', 'Number_of_Certifications', 'Number_of_Internships', 
        'Internship_Duration_Months', 'Practical_Skill_Score', 'Theoretical_Score',
        'Employer_Preference_Score'
    ]], drop_first=True)
    
    y_placement = df['Is_Placed']
    
    rf_clf = RandomForestClassifier(n_estimators=50, random_state=42)
    rf_clf.fit(X_features, y_placement)
    
    feature_importances = pd.DataFrame({
        'Feature': X_features.columns,
        'Importance': rf_clf.feature_importances_
    }).sort_values(by='Importance', ascending=False)
    
    top_placement_drivers = feature_importances.head(10).to_dict(orient='records')
    
    analytics_results = {
        "total_students": int(len(df)),
        "overall_placement_rate": float(round(df['Is_Placed'].mean() * 100, 2)),
        "overall_avg_salary": float(round(placed_df['Salary_Package_LPA'].mean(), 2)),
        "h2h_comparison": h2h_metrics,
        "statistical_tests": stat_tests,
        "top_placement_drivers": top_placement_drivers
    }
    
    with open("data/summary_metrics.json", "w") as f:
        json.dump(analytics_results, f, indent=4)
        
    profile_summary.to_csv("data/summary_profile_impact.csv", index=False)
    dur_ppo.to_csv("data/summary_duration_ppo.csv", index=False)
    multi_int.to_csv("data/summary_multi_internships.csv", index=False)
    multi_cert.to_csv("data/summary_multi_certs.csv", index=False)
    skills_impact.to_csv("data/summary_skills_impact.csv", index=False)
    
    print("Analytical pipeline completed successfully!")
    return analytics_results

if __name__ == "__main__":
    run_analytical_pipeline()
