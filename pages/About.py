import streamlit as st
from manager import apply_sidebar_style, set_background_css, hide_sidebar_pages

# Page config
st.set_page_config(page_title="About", page_icon="ℹ️")

# Styling
set_background_css()
apply_sidebar_style()
hide_sidebar_pages()

# Page content
st.title("About Resume Analyzer")
st.write("---")

st.markdown("""
### 📌 Overview
The **Resume Analyzer** is a powerful AI-driven platform designed to help both **job seekers** and **recruiters** make smarter hiring decisions.  
It uses **advanced natural language processing** to extract, analyze, and compare candidate data with job requirements, providing **ATS-style scoring**, **skill matching**, and **shortlisting recommendations**.

---

### 🎯 Who is this for?
- **Job Seekers** – Understand how your resume performs against job descriptions and identify improvement areas.
- **Recruiters & HR Teams** – Quickly filter through hundreds of resumes, find the most relevant candidates, and make data-backed hiring choices.

---

### ⚙️ How it Works
1. **Upload** your resume (PDF, Word, or Image).
2. **AI-Powered Parsing** extracts skills, experience, qualifications, and other key details.
3. **Matching Algorithm** compares resumes against predefined job criteria.
4. **Scoring & Shortlisting** based on:
   - ATS Score
   - Experience
   - Skills Match %
   - Location compatibility (if required)

---

### 💡 Key Features
- **🔍 Resume Parsing:** Extracts structured data from any resume format.
- **📊 AI Scoring:** Calculates an ATS-style score for each resume.
- **⚖️ Candidate Comparison:** Rank and shortlist based on multiple weighted criteria.
- **🌐 Cloud Storage:** All applicant data securely stored in Firebase/Firestore.
- **📈 Recruiter Dashboard:** Visualize applicant trends (location, skills, qualifications) and export to Excel.

---

### 🔐 Data Privacy
We value your privacy. All resumes and extracted data are stored securely and used **only for analysis purposes**.

---

### 🚀 Why Use Resume Analyzer?
Whether you’re a **fresh graduate**, an **experienced professional**, or a **recruiter handling hundreds of applications**, the Resume Analyzer saves time, improves decision-making, and helps you focus on the **right opportunities**.
""")
st.write("")
st.write("")