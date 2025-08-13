import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="About - ATS Resume Analyzer", page_icon="📄", layout="wide")

# --- Custom Background ---
page_bg = """
<style>
.stApp {
    background: linear-gradient(135deg, #1a1a1a, #0d0d0d);
    background-attachment: fixed;
    color: white;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Title ---
st.title("📄 About ATS Resume Analyzer")
st.write("---")

# --- Hero Section ---
st.markdown("""
### Revolutionizing the Hiring Process with AI  
Recruitment is evolving, and so should your hiring tools.  
The **ATS Resume Analyzer** empowers HR teams, recruiters, and business owners to screen, score, and shortlist candidates faster and more accurately than ever before.  

Instead of spending hours manually reading resumes, our AI handles the heavy lifting — letting you focus on finding the right fit for your organization.
""")

# --- How It Works ---
st.subheader("🔍 How It Works")
st.markdown("""
1. **Define Your Job Criteria**  
   Set your minimum experience, required skills, and location preferences directly in the app.

2. **Upload Resumes in Bulk**  
   Upload hundreds of resumes (PDFs or images) at once — no manual entry needed.

3. **AI-Powered Parsing & Scoring**  
   Using **LLaMA 3** via Groq API, the system extracts skills, work history, education, and calculates an **ATS Score**.

4. **Smart Shortlisting**  
   Candidates are ranked based on:
   - ATS Score  
   - Relevant Experience  
   - Skills Match Percentage  
   - Location Fit (if remote not allowed)

5. **Interactive Dashboard**  
   View applicant data visually — analyze by location, qualification, job title, and even generate skill word clouds.

6. **Download & Share**  
   Export shortlists or the full applicant list to Excel/CSV for easy reporting.
""")

# --- Key Features ---
st.subheader("✨ Key Features")
features = [
    "📥 **Bulk Resume Upload** – Handle 400+ resumes in one go.",
    "🤖 **AI-Powered Parsing** – Extract data with high accuracy from PDFs/images.",
    "⚙️ **Custom Job Criteria** – Tailor filters for each role.",
    "📊 **ATS Scoring** – Objective ranking system.",
    "📈 **Visual Analytics** – Location, qualification, skills breakdown.",
    "☁️ **Secure Cloud Storage** – Data stored per user in Firestore.",
    "📤 **Export Options** – Download results anytime."
]
for f in features:
    st.markdown(f)

# --- Technology Stack ---
st.subheader("🛠 Technology Stack")
st.markdown("""
- **Frontend/UI**: Streamlit (Python-based, interactive UI)
- **Backend**: Python + Firebase (Cloud Firestore)
- **AI Engine**: Groq's LLaMA 3 Model
- **Data Visualization**: Plotly, WordCloud
- **Storage**: Google Cloud Firestore (per-user data isolation)
""")

# --- Why We Built It ---
st.subheader("💡 Why We Built This App")
st.markdown("""
Hiring can be **time-consuming, biased, and inefficient** when done manually.  
Traditional ATS systems often fail to understand context or prioritize candidates fairly.  

We set out to create an **affordable, AI-powered, easy-to-use** alternative that:
- Saves **time** by automating resume screening.
- Improves **accuracy** with advanced parsing and scoring.
- Ensures **fairness** by evaluating based on skills, not formatting quirks.
""")

# --- Our Mission ---
st.subheader("🎯 Our Mission")
st.markdown("""
To **simplify and democratize recruitment technology** so that even small businesses and startups can access powerful ATS tools without the complexity and high costs.  
We believe **great talent should never be overlooked** just because their resume isn't keyword-optimized.
""")

# --- Closing ---
st.markdown("---")
st.markdown("""
💬 *Whether you’re hiring for a small startup or a global enterprise, the ATS Resume Analyzer helps you make data-driven hiring decisions — quickly, fairly, and confidently.*  
""")
