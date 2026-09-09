import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_powerbi_docx():
    doc = Document()
    
    # Page setup - Margins 1 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Color Palette
    PRIMARY_NAVY = RGBColor(15, 23, 42)     # #0F172A
    SECONDARY_BLUE = RGBColor(2, 132, 199)  # #0284C7
    ACCENT_GREEN = RGBColor(0, 166, 81)     # #00A651
    DARK_TEXT = RGBColor(30, 41, 59)        # #1E293B
    
    # Helper to add styled headings
    def add_custom_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_NAVY
        p.paragraph_format.space_after = Pt(4)
        
    def add_custom_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(13)
        run.font.italic = True
        run.font.color.rgb = SECONDARY_BLUE
        p.paragraph_format.space_after = Pt(24)

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = PRIMARY_NAVY
        
    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = SECONDARY_BLUE

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = DARK_TEXT

    def add_paragraph_text(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Segoe UI'
        run.font.size = Pt(10.5)
        run.font.color.rgb = DARK_TEXT
        return p

    def add_bullet_text(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Segoe UI'
        r_bold.font.size = Pt(10.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = PRIMARY_NAVY
        
        r_text = p.add_run(text)
        r_text.font.name = 'Segoe UI'
        r_text.font.size = Pt(10.5)
        r_text.font.color.rgb = DARK_TEXT

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(15, 23, 42)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_callout(text, title="💡 Power BI Best Practice"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "E0F2FE")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"{title}\n")
        r_title.font.name = 'Segoe UI'
        r_title.font.size = Pt(11)
        r_title.font.bold = True
        r_title.font.color.rgb = SECONDARY_BLUE
        
        r_body = p.add_run(text)
        r_body.font.name = 'Segoe UI'
        r_body.font.size = Pt(10)
        r_body.font.color.rgb = DARK_TEXT
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- DOCUMENT GENERATION ---
    
    add_custom_title("Power BI End-to-End Implementation Guide")
    add_custom_subtitle("Employability Intelligence & Career Success Platform | Power BI Native Visual Architecture")
    
    add_paragraph_text(
        "This guide provides step-by-step technical instructions for building a complete, high-performance Power BI report suite for ACC. "
        "Unlike standard dashboards that replicate simple web charts, this guide leverages advanced Power BI native visuals—including Decomposition Trees, Key Influencers AI Visuals, Treemaps, Ribbon Charts, Gauge Visuals, Smart Narratives, and What-If Parameter Sliders."
    )
    
    add_callout(
        "Power BI Desktop and Power BI Service offer powerful AI and structural visuals not available in standard web apps. "
        "By utilizing Decomposition Trees, Key Influencers, and What-If Parameters, ACC leadership can perform deep-root cause analysis on candidate employability.",
        title="⚡ Visual Strategy Notice"
    )

    # SECTION 1: DATA PIPELINE
    add_heading_1("1. Data Source Connection & Power Query M-Code Pipeline")
    add_paragraph_text("Connect Power BI Desktop to the master dataset (`employability_dataset.csv`) and apply the following M-Code data transformation step in Power Query Editor:")
    
    m_code = """let
    Source = Csv.Document(File.Contents("C:\\ACC_Platform\\data\\employability_dataset.csv"),[Delimiter=",", Columns=23, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Student_ID", type text}, {"Age", Int64.Type}, {"Gender", type text},
        {"Education_Level", type text}, {"Graduation_Year", Int64.Type}, {"College_Name", type text},
        {"Course_Branch", type text}, {"Certification_Name", type text}, {"Certification_Provider", type text},
        {"Number_of_Certifications", Int64.Type}, {"Internship_Company", type text}, {"Internship_Domain", type text},
        {"Internship_Duration_Months", Int64.Type}, {"Number_of_Internships", Int64.Type}, {"Experience_Profile", type text},
        {"Practical_Skill_Score", Int64.Type}, {"Theoretical_Score", Int64.Type}, {"Employer_Preference_Score", type number},
        {"Placement_Status", type text}, {"Salary_Package_LPA", type number}, {"PPO_Conversion_Status", type text},
        {"Time_to_Offer_Days", Int64.Type}, {"Primary_Skills", type text}
    }),
    #"Added IsPlaced" = Table.AddColumn(#"Changed Type", "Is_Placed_Binary", each if [Placement_Status] = "Placed" then 1 else 0, Int64.Type),
    #"Added SalaryTier" = Table.AddColumn(#"Added IsPlaced", "Salary_Tier", 
        each if [Salary_Package_LPA] >= 15 then "High Package (15+ LPA)"
        else if [Salary_Package_LPA] >= 8 then "Mid Package (8-15 LPA)"
        else if [Salary_Package_LPA] > 0 then "Standard Package (<8 LPA)"
        else "Unplaced", type text)
in
    #"Added SalaryTier\""""
    add_code_block(m_code)

    # SECTION 2: STAR SCHEMA DATA MODELING
    add_heading_1("2. Data Modeling & Star Schema Architecture")
    add_paragraph_text("To ensure maximum DAX evaluation speed and filter propagation, configure the model into a Star Schema with a dedicated Skills Bridge Table:")
    
    add_bullet_text("Fact_Student_Employability: ", "Central fact table storing 2,500 student records and transactional placement metrics.")
    add_bullet_text("Dim_College: ", "Dimension table of unique College Names and Tier classifications (Tier 1, Tier 2, Tier 3).")
    add_bullet_text("Dim_Experience_Profile: ", "Dimension table categorizing profiles (Both Hybrid, Internship Only, Certification Only, Neither).")
    add_bullet_text("Dim_Skills_Bridge: ", "Reference table created by splitting `Primary_Skills` by delimiter `, ` maintaining a 1-to-Many relationship with `Student_ID`.")

    # SECTION 3: DAX CALCULATED MEASURES
    add_heading_1("3. Comprehensive DAX Calculated Measures Dictionary")
    add_paragraph_text("Create a dedicated calculated table `_Analytics_Measures` in Power BI and add the following 15 production DAX measures:")

    dax_measures = """// 1. Total Student Cohort Count
Total Students = COUNTROWS('Fact_Student_Employability')

// 2. Placed Students Count
Placed Count = CALCULATE(COUNTROWS('Fact_Student_Employability'), 'Fact_Student_Employability'[Placement_Status] = "Placed")

// 3. Overall Placement Rate %
Placement Rate % = DIVIDE([Placed Count], [Total Students], 0) * 100

// 4. Average Starting Salary Package (Placed Only)
Avg Salary LPA = CALCULATE(AVERAGE('Fact_Student_Employability'[Salary_Package_LPA]), 'Fact_Student_Employability'[Placement_Status] = "Placed")

// 5. Internship Only Placement Rate %
Internship Placement Rate = CALCULATE([Placement Rate %], 'Fact_Student_Employability'[Experience_Profile] = "Internship Only")

// 6. Certification Only Placement Rate %
Cert Placement Rate = CALCULATE([Placement Rate %], 'Fact_Student_Employability'[Experience_Profile] = "Certification Only")

// 7. Hybrid Profile Placement Rate %
Hybrid Placement Rate = CALCULATE([Placement Rate %], 'Fact_Student_Employability'[Experience_Profile] = "Both (Hybrid)")

// 8. Placement Advantage Gap (% difference)
Placement Advantage Gap = [Internship Placement Rate] - [Cert Placement Rate]

// 9. Avg Salary - Internship Only
Avg Salary Internship Only = CALCULATE([Avg Salary LPA], 'Fact_Student_Employability'[Experience_Profile] = "Internship Only")

// 10. Avg Salary - Certification Only
Avg Salary Cert Only = CALCULATE([Avg Salary LPA], 'Fact_Student_Employability'[Experience_Profile] = "Certification Only")

// 11. Salary Premium Percentage (Internship vs Cert)
Salary Premium % = DIVIDE([Avg Salary Internship Only] - [Avg Salary Cert Only], [Avg Salary Cert Only], 0) * 100

// 12. Direct PPO Conversion Rate %
PPO Conversion Rate % = DIVIDE(
    CALCULATE(COUNTROWS('Fact_Student_Employability'), 'Fact_Student_Employability'[PPO_Conversion_Status] = "Direct PPO (Pre-Placement Offer)"),
    CALCULATE(COUNTROWS('Fact_Student_Employability'), 'Fact_Student_Employability'[Number_of_Internships] > 0),
    0
) * 100

// 13. Average Employer Preference Rating (1-10)
Avg Employer Rating = AVERAGE('Fact_Student_Employability'[Employer_Preference_Score])

// 14. Average Days to Job Offer
Avg Days to Offer = CALCULATE(AVERAGE('Fact_Student_Employability'[Time_to_Offer_Days]), 'Fact_Student_Employability'[Placement_Status] = "Placed")

// 15. Dynamic Predicted Placement Rate (What-If Parameter Measure)
Predicted Placement Rate % = 
VAR IntVal = SELECTEDVALUE('Internships_Parameter'[Internships_Parameter], 1)
VAR DurVal = SELECTEDVALUE('Duration_Parameter'[Duration_Parameter], 3)
VAR CertVal = SELECTEDVALUE('Certs_Parameter'[Certs_Parameter], 1)
VAR Logit = -2.2 + (IntVal * 1.3) + (DurVal * 0.15) + (CertVal * 0.35)
RETURN DIVIDE(1, 1 + EXP(-Logit)) * 100\""""
    add_code_block(dax_measures)

    # SECTION 4: PAGE-BY-PAGE POWER BI NATIVE VISUAL LAYOUT
    add_heading_1("4. Page-by-Page Power BI Native Visual Layout Guides")
    add_paragraph_text("Below are detailed build specifications for 6 specialized Power BI report pages featuring unique Power BI native visual types:")

    # PAGE 1
    add_heading_2("Page 1: 📊 Employability Macro Impact")
    add_bullet_text("Visual 1 - Ribbon Chart (Rank Changes Across College Tiers): ", "Axis: `College_Name`, Legend: `Experience_Profile`, Values: `Placement Rate %`. Shows how candidate ranking shifts across college tiers.")
    add_bullet_text("Visual 2 - Tornado / Clustered Bar Chart (Placement Gap): ", "Y-Axis: `Education_Level`, X-Axis: `Placement Advantage Gap`. Highlights which degree levels benefit most from internship experience.")
    add_bullet_text("Visual 3 - Card Visual Grid: ", "Displays `Total Students`, `Placement Rate %`, `Avg Salary LPA`, and `Placement Advantage Gap` (+27.8%).")
    add_bullet_text("Slicers: ", "Dropdown slicers for `Graduation_Year` and `Course_Branch`.")

    # PAGE 2
    add_heading_2("Page 2: ⚖️ Head-to-Head Comparison & Target Benchmark")
    add_bullet_text("Visual 1 - Radial Gauge Visual (Internship vs Hybrid Target): ", "Value: `Internship Placement Rate` (97.7%), Target: `Hybrid Placement Rate` (98.3%), Max: 100%. Demonstrates how close internship candidates get to peak hybrid performance.")
    add_bullet_text("Visual 2 - Scatter Visual with Quadrant Reference Constant Lines: ", "X-Axis: `Theoretical_Score`, Y-Axis: `Practical_Skill_Score`, Size: `Salary_Package_LPA`, Legend: `Experience_Profile`. Add X=70 and Y=70 Constant Reference Lines to split candidates into 4 placement quadrants.")
    add_bullet_text("Visual 3 - Multi-Row Card: ", "Side-by-side metric comparison between `Internship Only` vs `Certification Only` profiles.")

    # PAGE 3
    add_heading_2("Page 3: 💰 Placement Pipeline & Time-to-Offer Funnel")
    add_bullet_text("Visual 1 - Funnel Visual (Internship to Job Conversion Pipeline): ", "Category: `PPO_Conversion_Status`, Values: `Total Students`. Displays conversion bottlenecks from internship start to Direct PPO offer.")
    add_bullet_text("Visual 2 - Line and Clustered Column Combo Chart: ", "Shared Axis: `Number_of_Internships`, Column Values: `Placement Rate %`, Line Values: `Avg Salary LPA`.")
    add_bullet_text("Visual 3 - Clustered Column Chart (Speed to Offer): ", "X-Axis: `Experience_Profile`, Y-Axis: `Avg Days to Offer`. Demonstrates how internships reduce hiring speed from 98 days down to 28 days.")

    # PAGE 4
    add_heading_2("Page 4: 🏢 Employer Preference & AI Key Drivers")
    add_bullet_text("Visual 1 - Decomposition Tree Visual (Root Cause Analysis): ", "Analyze: `Avg Employer Rating`, Explain By: `Experience_Profile`, `College_Name`, `Course_Branch`. Enables executives to click and dynamically break down employer preference ratings at any level.")
    add_bullet_text("Visual 2 - AI Key Influencers Visual: ", "Analyze: `Placement_Status`, Explain By: `Number_of_Internships`, `Internship_Duration_Months`, `Employer_Preference_Score`, `Number_of_Certifications`. Automatically identifies top drivers boosting placement odds by X times.")
    add_bullet_text("Visual 3 - Matrix Visual with Conditional Color Heatmap: ", "Rows: `Internship_Domain`, Columns: `Certification_Provider`, Values: `Avg Employer Rating`. Apply Conditional Formatting -> Background Color Scale (Dark Slate to Neon Green).")

    # PAGE 5
    add_heading_2("Page 5: 🎯 Skills Demand & Market Treemap")
    add_bullet_text("Visual 1 - Treemap Visual (Skill Market Volume & Value): ", "Group: `Skill` (from `Dim_Skills_Bridge`), Values: `Placed Count`, Details: `Avg Salary LPA`. Tile size represents volume of hires; color gradient represents average salary boost.")
    add_bullet_text("Visual 2 - Smart Narrative AI Visual: ", "Automatically generates dynamic text summarizing top high-paying skills (Python, AWS, SQL) and auto-updates when filters change.")
    add_bullet_text("Visual 3 - Scatter Visual (Skill Opportunity Matrix): ", "X-Axis: `Placement Rate %`, Y-Axis: `Avg Salary LPA`, Size: `Total Students`, Details: `Skill`.")

    # PAGE 6
    add_heading_2("Page 6: 🚀 Dynamic What-If Career Pathway Advisor")
    add_bullet_text("Visual 1 - What-If Parameter Sliders: ", "Create 3 Numeric Range Parameters: `Internships_Parameter` (0-4), `Duration_Parameter` (0-12 months), `Certs_Parameter` (0-5). Render as interactive slider controls.")
    add_bullet_text("Visual 2 - KPI Card (Predicted Placement Probability %): ", "Displays `[Predicted Placement Rate %]` measure reacting live in real-time as users adjust the slider parameters.")
    add_bullet_text("Visual 3 - Strategy Decision Matrix Table: ", "Displays recommended ACC policy actions based on candidate risk profile.")

    # SECTION 5: PUBLISHING & SERVICE SETUP
    add_heading_1("5. Power BI Service Deployment, RLS & Governance")
    add_bullet_text("1. Save & Publish: ", "Save report as `ACC_Employability_Intelligence.pbix` and publish to Power BI Service (`app.powerbi.com`).")
    add_bullet_text("2. Scheduled Refresh: ", "Configure Gateway Connection under Dataset Settings for daily automated refresh.")
    add_bullet_text("3. Row-Level Security (RLS): ", "In Power BI Desktop, navigate to Modeling -> Manage Roles. Create role `College_Admin` with DAX filter `[College_Name] = USERPRINCIPALNAME()`.")
    add_bullet_text("4. Mobile Layout Optimization: ", "Switch to View -> Mobile Layout and organize KPI cards and Decomposition Trees for mobile smartphone viewing.")

    # Save document
    os.makedirs("data", exist_ok=True)
    out_path = "PowerBI_End_To_End_Guide.docx"
    doc.save(out_path)
    print(f"Document successfully created at: {out_path}")
    return out_path

if __name__ == "__main__":
    create_powerbi_docx()
