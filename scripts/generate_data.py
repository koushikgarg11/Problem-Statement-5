import os
import numpy as np
import pandas as pd

def generate_employability_dataset(num_records=2500, seed=42):
    np.random.seed(seed)
    
    student_ids = [f"STU{10000 + i}" for i in range(num_records)]
    ages = np.random.choice([21, 22, 23, 24, 25], size=num_records, p=[0.25, 0.40, 0.20, 0.10, 0.05])
    genders = np.random.choice(["Male", "Female", "Non-Binary"], size=num_records, p=[0.52, 0.45, 0.03])
    
    education_levels = np.random.choice(
        ["B.Tech", "BCA", "B.Sc (CS/IT)", "M.Tech", "MBA (Tech & Analytics)"],
        size=num_records,
        p=[0.50, 0.20, 0.15, 0.08, 0.07]
    )
    
    grad_years = np.random.choice([2023, 2024, 2025, 2026], size=num_records, p=[0.20, 0.30, 0.35, 0.15])
    
    colleges = np.random.choice(
        [
            "IIT / NIT Group (Tier 1)", 
            "BITS & Top National Inst (Tier 1)", 
            "State Tech University (Tier 2)", 
            "Apex Institute of Technology (Tier 2)", 
            "City Engineering College (Tier 3)", 
            "Regional Tech Institute (Tier 3)"
        ],
        size=num_records,
        p=[0.12, 0.13, 0.30, 0.25, 0.12, 0.08]
    )
    
    branches = np.random.choice(
        [
            "Computer Science & Engineering", 
            "Data Science & Artificial Intelligence", 
            "Information Technology", 
            "Electronics & Communication", 
            "Business Analytics", 
            "Cyber Security"
        ],
        size=num_records,
        p=[0.35, 0.25, 0.15, 0.12, 0.08, 0.05]
    )
    
    # Certifications setup
    cert_names_pool = [
        "AWS Certified Solutions Architect",
        "Google Professional Data Engineer",
        "Microsoft Certified: Azure Developer",
        "Meta Front-End Developer Specialization",
        "IBM Data Science Professional",
        "TensorFlow Developer Certificate",
        "Certified Information Systems Security Professional (CISSP)",
        "NPTEL Cloud Computing & Distributed Systems",
        "Coursera Machine Learning Specialization",
        "Docker & Kubernetes Developer Cert"
    ]
    cert_providers_pool = ["AWS", "Google Cloud", "Microsoft Azure", "Coursera", "IBM", "Meta", "NPTEL", "Udemy"]
    
    num_certs = np.random.choice([0, 1, 2, 3, 4, 5], size=num_records, p=[0.20, 0.30, 0.25, 0.15, 0.07, 0.03])
    cert_names = []
    cert_providers = []
    
    for count in num_certs:
        if count == 0:
            cert_names.append("None")
            cert_providers.append("None")
        else:
            chosen_certs = np.random.choice(cert_names_pool, size=min(count, 3), replace=False)
            chosen_provs = np.random.choice(cert_providers_pool, size=min(count, 3), replace=False)
            cert_names.append("; ".join(chosen_certs))
            cert_providers.append("; ".join(chosen_provs))
            
    # Internships setup
    intern_companies_pool = [
        "Microsoft Tech", "Amazon AWS", "Google India", "Deloitte Consulting", 
        "TCS Innovation Labs", "Infosys Center", "FinTech Solutions", 
        "CyberGuard Analytics", "DataMetrics Labs", "InnovateTech Startup"
    ]
    intern_domains_pool = [
        "Software Engineering", "Data Science & Analytics", "Cloud & DevOps", 
        "Artificial Intelligence / ML", "Cyber Security", "Product & Business Analytics"
    ]
    
    num_internships = np.random.choice([0, 1, 2, 3], size=num_records, p=[0.25, 0.40, 0.25, 0.10])
    intern_durations = []
    intern_companies = []
    intern_domains = []
    
    for n_int in num_internships:
        if n_int == 0:
            intern_durations.append(0)
            intern_companies.append("None")
            intern_domains.append("None")
        else:
            duration = int(np.random.choice([2, 3, 6, 9, 12], p=[0.30, 0.35, 0.20, 0.10, 0.05]) * (1 + 0.3*(n_int-1)))
            comp = np.random.choice(intern_companies_pool)
            dom = np.random.choice(intern_domains_pool)
            intern_durations.append(duration)
            intern_companies.append(comp)
            intern_domains.append(dom)
            
    # Calculate Experience Profile Group
    profile_groups = []
    for nc, ni in zip(num_certs, num_internships):
        if ni > 0 and nc > 0:
            profile_groups.append("Both (Hybrid)")
        elif ni > 0 and nc == 0:
            profile_groups.append("Internship Only")
        elif ni == 0 and nc > 0:
            profile_groups.append("Certification Only")
        else:
            profile_groups.append("Neither")
            
    # Skills pool generator
    skills_pool = [
        "Python", "SQL", "AWS", "Docker", "React", "Machine Learning", 
        "Data Analysis", "Communication", "Problem Solving", "Java", 
        "Git", "Kubernetes", "Power BI", "Tableau", "System Design"
    ]
    
    student_skills = []
    for nc, ni in zip(num_certs, num_internships):
        skill_count = min(10, max(2, nc * 2 + ni * 3 + np.random.randint(1, 4)))
        chosen_skills = list(np.random.choice(skills_pool, size=skill_count, replace=False))
        student_skills.append(", ".join(chosen_skills))
        
    # Scores & Employability Probabilities logic
    practical_scores = []
    theoretical_scores = []
    employer_pref_scores = []
    placed_statuses = []
    salaries = []
    ppo_conversions = []
    time_to_offers = []
    
    for i in range(num_records):
        nc = num_certs[i]
        ni = num_internships[i]
        dur = intern_durations[i]
        college = colleges[i]
        
        tier_boost = 15 if "Tier 1" in college else (8 if "Tier 2" in college else 0)
        
        pract_score = min(100, max(20, int(30 + ni * 18 + dur * 2.5 + tier_boost + np.random.normal(0, 6))))
        theo_score = min(100, max(20, int(40 + nc * 12 + tier_boost + np.random.normal(0, 7))))
        
        emp_pref = min(10.0, max(2.0, round(3.5 + (ni * 1.5) + (dur * 0.25) + (nc * 0.4) + (tier_boost * 0.08) + np.random.normal(0, 0.5), 1)))
        
        logit = -2.2 + (ni * 1.3) + (dur * 0.15) + (nc * 0.35) + (tier_boost * 0.05) + (emp_pref * 0.4)
        prob_placement = 1 / (1 + np.exp(-logit))
        is_placed = np.random.binomial(1, prob_placement) == 1
        
        if is_placed:
            status = "Placed"
            base_sal = 4.5 + tier_boost * 0.35
            intern_boost = ni * 2.2 + (dur * 0.45)
            cert_boost = nc * 0.6
            salary = round(base_sal + intern_boost + cert_boost + np.random.normal(0, 1.2), 2)
            salary = max(3.5, salary)
            
            if ni > 0 and dur >= 6 and np.random.rand() < 0.65:
                ppo = "Direct PPO (Pre-Placement Offer)"
            elif ni > 0 and np.random.rand() < 0.35:
                ppo = "Internship Conversion"
            else:
                ppo = "On-Campus / Off-Campus Placement"
                
            t_offer = max(5, int(120 - (ni * 30) - (dur * 4) - (nc * 8) + np.random.normal(0, 15)))
        else:
            status = "Unplaced"
            salary = 0.0
            ppo = "Not Converted"
            t_offer = -1
            
        practical_scores.append(pract_score)
        theoretical_scores.append(theo_score)
        employer_pref_scores.append(emp_pref)
        placed_statuses.append(status)
        salaries.append(salary)
        ppo_conversions.append(ppo)
        time_to_offers.append(t_offer)
        
    df = pd.DataFrame({
        "Student_ID": student_ids,
        "Age": ages,
        "Gender": genders,
        "Education_Level": education_levels,
        "Graduation_Year": grad_years,
        "College_Name": colleges,
        "Course_Branch": branches,
        "Certification_Name": cert_names,
        "Certification_Provider": cert_providers,
        "Number_of_Certifications": num_certs,
        "Internship_Company": intern_companies,
        "Internship_Domain": intern_domains,
        "Internship_Duration_Months": intern_durations,
        "Number_of_Internships": num_internships,
        "Experience_Profile": profile_groups,
        "Practical_Skill_Score": practical_scores,
        "Theoretical_Score": theoretical_scores,
        "Employer_Preference_Score": employer_pref_scores,
        "Placement_Status": placed_statuses,
        "Salary_Package_LPA": salaries,
        "PPO_Conversion_Status": ppo_conversions,
        "Time_to_Offer_Days": time_to_offers,
        "Primary_Skills": student_skills
    })
    
    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("data", "employability_dataset.csv")
    df.to_csv(csv_path, index=False)
    print(f"Dataset successfully created with {len(df)} records at: {csv_path}")
    return df

if __name__ == "__main__":
    generate_employability_dataset()
