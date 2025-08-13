import streamlit as st

# --- Import your style functions ---
def apply_sidebar_style():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background: #1c1c3c;
            padding-top: 20px;
            border-right: 1px solid #5a189a;
        }
        [data-testid="stSidebarNav"] > div {
            font-size: 18px;
            font-weight: bold;
            color: #f8f8f2;
        }
        section[data-testid="stSidebar"] a {
            color: #dcdcdc !important;
            font-size: 16px;
            padding: 8px 12px;
            display: block;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        section[data-testid="stSidebar"] a:hover {
            background-color: #5a189a22;
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLinkActive"] {
            background-color: #5a189a88;
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)

def set_background_css():
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main {
        background: linear-gradient(135deg, #240046 0%, #3c096c 50%, #5a189a 70%, #006494 90%) !important;
        color: white !important;
    }
    .block-container {
        padding: 2rem 3rem;
    }
    h1, h2, h3, h4, h5, h6, p, li {
        color: white !important;
    }
    hr {
        border: 1px solid #5a189a;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Apply Styles ---
apply_sidebar_style()
set_background_css()

# --- Page Content ---
st.title("📄 About ATS Resume Analyzer")
st.write("---")

st.markdown("""
### Revolutionizing the Hiring Process with AI  
Recruitment is evolving, and so should your hiring tools.  
The **ATS Resume Analyzer** empowers HR teams, recruiters, and business owners to screen, score, and shortlist candidates faster and more accurately than ever before.  

Instead of spending hours manually reading resumes, our AI handles the heavy lifting — letting you focus on finding the right fit for your organization.
""")

st.subheader("🔍 How It Works")
st.markdown("""
1. **Define Your Job Criteria** – Set your minimum experience, required skills, and location preferences directly in the app.  
2. **Upload Resumes in Bulk** – Upload hundreds of resumes (PDFs or images) at once.  
3. **AI-Powered Parsing & Scoring** – Using **LLaMA 3** via Groq API, the system extracts skills, work history, education, and calculates an **ATS Score**.  
4. **Smart Shortlisting** – Candidates ranked by ATS score, relevant experience, skills match %, and location fit.  
5. **Interactive Dashboard** – Analyze by location, qualification, skills word clouds.  
6. **Download & Share** – Export shortlists or the full applicant list to Excel/CSV.
""")

st.subheader("✨ Key Features")
st.markdown("""
- 📥 **Bulk Resume Upload** – Handle 400+ resumes in one go.  
- 🤖 **AI-Powered Parsing** – Extract data with high accuracy.  
- ⚙️ **Custom Job Criteria** – Tailor filters for each role.  
- 📊 **ATS Scoring** – Objective candidate ranking.  
- 📈 **Visual Analytics** – Skills, location, qualification charts.  
- ☁️ **Secure Cloud Storage** – Per-user Firestore database.  
- 📤 **Export Options** – Download results anytime.
""")

st.subheader("🛠 Technology Stack")
st.markdown("""
- **Frontend/UI**: Streamlit  
- **Backend**: Python + Firebase  
- **AI Engine**: Groq's LLaMA 3 Model  
- **Visualization**: Plotly, WordCloud  
- **Database**: Google Cloud Firestore
""")

st.subheader("💡 Why We Built This App")
st.markdown("""
Hiring can be **time-consuming, biased, and inefficient** when done manually.  
We built ATS Resume Analyzer to make recruitment **faster, fairer, and more data-driven** — so great talent never slips through the cracks.
""")

st.subheader("🎯 Our Mission")
st.markdown("""
To **simplify and democratize recruitment technology** so small businesses and startups can access the same powerful ATS tools used by big corporations — without the complexity or cost.
""")

st.write("---")
st.markdown("""
💬 *Whether you’re hiring for a small startup or a global enterprise, the ATS Resume Analyzer helps you make data-driven hiring decisions — quickly, fairly, and confidently.*  
""")
