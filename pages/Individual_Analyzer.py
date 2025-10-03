import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
from manager import require_login, hide_sidebar_pages, apply_sidebar_style, set_background_css

# ---------------------------
# Apply styling and login
# ---------------------------
apply_sidebar_style()
set_background_css()
hide_sidebar_pages()


# ---------------------------
# Configure Google Generative AI using Streamlit secrets
# ---------------------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# ---------------------------
# Gemini Pro response
# ---------------------------
def get_gemini_response(input_text, model_name='gemini-1.5-flash', timeout=90):
    try:
        model = genai.GenerativeModel(model_name)
        generation_config = genai.types.GenerationConfig()
        generation_config.timeout_seconds = timeout
        
        response = model.generate_content(
            input_text,
            generation_config=generation_config
        )
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# ---------------------------
# Extract text from PDF
# ---------------------------
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += str(reader.pages[page_num].extract_text())
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# ---------------------------
# Prompts
# ---------------------------
input_prompt = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality.
Your task is to evaluate the resume against the provided job description.
Give me the percentage of match if the resume matches the job description. First, the output should come as a percentage, then list missing keywords, and finally provide your final thoughts.
Assign the percentage matching based on jd and the missing keyword with high accuracy
resume:{text}
description:{jd}
Give the following data in detail:
Name:
Contact:
Profile match:
Missing keywords:
Profile Summary:
Tips: (In this section give tips to improve resume.)
What You did well: (Analyze the resume and point out the strengths of the resume, its structure, etc and give feedback)
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality.
The resume is: {text}
and the job description is: {jd}
Analyze the resume uploaded and answer to the following prompt in detail:

{cust}
"""

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("Individual Resume Analyzer")

jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload your PDF")

submit = st.button("Analyze")

if "responses1" not in st.session_state:
    st.session_state.responses1 = []

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        if text:
            result = get_gemini_response(
                input_prompt.format(text=text, jd=jd),
                model_name='gemini-1.5-flash',
                timeout=90
            )
            if result:
                st.session_state.responses1.append(result)

for resp in st.session_state.responses1:
    st.write(resp)

# ---------------------------
# Custom Query
# ---------------------------
cust = st.text_area("Ask what you want to know about your resume:")
submit2 = st.button("Submit")

if "latest_responses2" not in st.session_state:
    st.session_state.latest_responses2 = ""

if submit2:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        if text:
            result2 = get_gemini_response(
                input_prompt2.format(text=text, jd=jd, cust=cust),
                model_name='gemini-1.5-flash',
                timeout=90
            )
            if result2:
                st.session_state.latest_responses2 = result2

st.write(st.session_state.latest_responses2)
