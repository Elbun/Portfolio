import streamlit as st
from lib_function import tech_skill, education, experience, insert_icon, lets_connect

#----------------------------- Set page layout
st.set_page_config(layout="wide")

#----------------------------- Set image location
pic_path = "A. Home/"

#----------------------------- Segment 1 : Introduction
col1, col2, col3, col4 = st.columns([1,2,.5,7])
with col1:
    insert_icon(pic_path, "gif1_hi.gif")
with col2:
    st.html('''<p style="font-size:40px;text-align:right;"><b>Hi, <br>I'm Elvin!</br></b></p>''')
with col4:
    st.html('''<p style="text-align:justify;">A data analyst professional who has a proven track record in various data related roles advanced with
        other business knowledge in <b>Supply Chain Management</b> and <b>Financial Management</b> for IT Consulting and Healthcare industries. 
        Proficient in <b>SQL, Python, Microsoft Excel and BI Tools</b> for comprehensive data engineering and analysis. Comfortable with end-to-end business 
        process analysis, data processing, dashboard creation, and presenting actionable insights with effective story-telling skills. Currently focus on 
        developing advance analytic skills with <b>specialization in corporate planning and budgeting</b> by optimizing corporate data processing and analysis to deliver 
        valuable insights.</p>''')
st.divider()

#----------------------------- Segment 2 : Skill
st.header("Technical Skills")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader("Programming Languages")
    # SQL
    tech_skill("SQL", pic_path, "pic1_sql.png")
    # Python
    tech_skill("Python", pic_path, "pic2_python.png")
with col2:
    st.subheader("Data Analytic Tools")
    # Ms Excel
    tech_skill("Microsoft Excel", pic_path, "pic3_excel.png")
    # TM1
    tech_skill("IBM Planning Analytics / TM1", pic_path, "pic16_ibm (2).png")  
with col3:
    st.subheader("Data Visualization Tools")
    # Qlikview
    tech_skill("Qlikview & Qliksense", pic_path, "pic5_qv.png")
    # Metabase
    tech_skill("Metabase", pic_path, "pic15_metabase.jpeg")
    # Ms Excel
    tech_skill("Power BI", pic_path, "pic4_pbi.png")
with col4:
    st.subheader("Others")
    # Financial Analysis
    tech_skill("Financial Analysis", pic_path, "pic17_fin.png")
    # SCM
    tech_skill("Stock & Warehosue Analysis", pic_path, "pic18_scm.png")
st.divider()

#----------------------------- Segment 3 : Education & Experience
st.header("Education & Experiences")
col1, col2, col3, col4 = st.columns([11,1,11,1])
with col1:
    st.subheader("Experiences")
    # QBAnalytix
    desc = '''QBAnalytix, a preeminent Software Value Plus IBM partner, provides Performance Management solutions including Forecasting & Budgeting, Planning, 
        Reporting, Consolidation, Advance Analytics and Business Intelligence solutions that provides competitive advantages to its clients by enabling them to 
        analyze their data faster and better.'''
    experience("QBAnalytix", pic_path, "pic10_qb.jpg", "Nov 2025", "present", "Associate Consultant", desc)
    # AAM
    desc = '''Anugrah Argon Medica (AAM), a part of Medela Potentia, is a pharmaceuticals and medical devices distributor company with more than 40 years of experience
        serving principals and customers. AAM has more than 30 branches located across Indonesia from Aceh to Jayapura. Many principals have trusted AAM and became 
        partners to serve Indonesia like Dexa Medica, L'OREAL, Abbott, Nestle, Pfizer, Novo Nordisk, Alcon, and so on.'''
    experience("Anugrah Argon Medica", pic_path, "pic13_aam.png", "Jan 2025", "Oct 2025", "Data Analyst", desc)
    # MP
    desc = '''Argon Group is a group of healthcare companies. Its business included distribution (PT Anugrah Argon Medica and Dynamic Argon Co., Ltd), 
        marketing (PT Djembatan Dua), and manufacturing (PT Deca Metric Medica). Argon Group also concern about its technology development to support their 
        business in order to keep and improve their services to their customers and stakeholders.'''
    experience("Medela Potentia (Argon Group)", pic_path, "pic8_mp.png", "Nov 2022", "Dec 2024", "Data Analyst", desc)
    # One Code Solution
    desc = '''One Code Solution is a technology service company specialize in offshore development.'''
    experience("One Code Solution", pic_path, "pic12_ocs.jpeg", "Apr 2022", "Oct 2022", "Data Engineer", desc)
    # Impactto
    desc = '''Impactto is a collective builder platform that aims to democratize early-stage startup founders' access to applicable knowledge and best-practices 
        on how to achieve a product-market fit.'''
    experience("Impactto", pic_path, "pic7_impactto.jpeg", "Jan 2021", "Feb 2022", "Project Management Officer", desc)
with col3:
    st.subheader("Education")
    # ITB
    desc = "Bachelor of Science in Industrial Engineering"
    education("Bandung Institute of Technology", pic_path, "pic11_itb.png", "Aug 2016", "Sep 2020", desc)
    # Download CV
    with open(pic_path+"Resume_Elvin Buntoro.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button(
        label="Get my resume",
        data=PDFbyte,
        file_name="Resume_Elvin Buntoro.pdf",
        mime="application/octet-stream"
    )
st.divider()

#----------------------------- Segment 4 : Contact info
st.header("Let's Connect!")
st.html('''<p style="text-align:justify;">Searching for a solution for your business problem? Or just want to discuss something with me? Don't hesitate to reach out me!</p>''')
col1, col2, col3, col4 = st.columns(4)
with col1:
    # LinkedIn
    lets_connect(pic_path, "pic6_linkedin.png", "Elvin Buntoro", "https://www.linkedin.com/in/elvin-buntoro-39b83b1b2/")
    # Email
    lets_connect(pic_path, "pic9_gmail.webp", "elvinbuntoro@gmail.com", "mailto:elvinbuntoro@gmail.com")
    # Whatsapp
    lets_connect(pic_path, "pic14_wa.png", "+6281280142251", "https://wa.me/6281280142251/")
