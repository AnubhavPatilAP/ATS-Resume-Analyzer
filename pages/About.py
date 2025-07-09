import streamlit as st
from manager import NavigationManager, apply_sidebar_style, set_background_css, hide_sidebar_pages

st.set_page_config(page_title="About", page_icon="ℹ️")

# --- Styling ---
set_background_css()
apply_sidebar_style()
hide_sidebar_pages()

# --- Navigation ---
nav_manager = NavigationManager()
nav_manager.top_nav()

# --- About Content ---
st.title("About Resume Analyzer")
st.markdown("---")

st.markdown(
    """
### 📌 Overview
**Resume Analyzer** is a powerful AI-driven platform built to simplify and streamline the recruitment process for both **individual candidates** and **recruiters**.

It offers intelligent resume parsing, structured data extraction, automated filtering, and real-time analytics to help match the right candidate to the right job.

---

### 👤 For Individuals
Job seekers can:
- Upload their resumes (PDF, DOCX, or images).
- Get AI-based feedback on their resume content.
- Analyze **ATS (Applicant Tracking System) compatibility**.
- Discover matching roles based on their skills and experience.

---

### 🧑‍💼 For Recruiters
Recruiters can:
- Upload multiple resumes at once.
- Automatically extract structured data (name, skills, experience, etc.).
- Filter candidates by **skills**, **location**, **experience**, and more.
- View a **dashboard** with graphs, insights, and shortlist actions.
- Manually filter applicants using a dynamic table.
- Export shortlisted results in Excel format.

---

### 🔍 Technologies Used
- **Streamlit** for frontend and user interactions.
- **Groq / Gemini AI** for resume parsing and field extraction.
- **Firebase** for authentication and user-specific data storage.
- **OpenPyXL** for Excel export.
- **Plotly** for data visualization.
- **DuckDB** for efficient local SQL queries.

---

### 🔐 Authentication
User login is secured via Firebase to ensure a personalized and secure experience for both recruiters and individuals.

---

### 📈 Dashboard Insights
Recruiters can visualize:
- Skills distribution
- Candidate experience range
- Applicant location maps
- Shortlisted vs unqualified stats

---

### 🧠 AI & NLP
The platform uses advanced language models to:
- Parse resume PDFs and images
- Interpret unstructured text
- Provide structured output (Name, Skills, Experience, etc.)
- Determine gender from names
- Score resumes against job criteria

---

### 🔄 Page Navigation Flow

#### Recruiter Flow:
`Home → Form → DataCollector → Dashboard → Manual Filter`

#### Individual Flow:
`Home → Individual Analyzer → AI Feedback & Score`

---

### 📬 Contact
For suggestions, improvements, or queries, feel free to reach out to the development team.

---
"""
)
