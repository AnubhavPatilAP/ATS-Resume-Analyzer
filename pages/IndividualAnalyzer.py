import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from manager import NavigationManager  

# Navigator
nav_manager = NavigationManager()
nav_manager.top_nav()



from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Gemini Pro response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):  # Fixed typo here (changed 'age' to 'page_num')
        page = reader.pages[page_num]  # Corrected the page extraction
        text += str(page.extract_text())  # Corrected method name to 'extract_text'
    return text

# Prompts for different actions
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
Profile match :
Missing keywords:
Profile Summary:
Tips: (In this section give tips to improve resume.)
What You did well: (Analyze the resume and point out the strengths of the resume, its structure, etc and give feedback)
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of ATS functionality.
The resume is: {text}
and the job description is : {jd}
Analyze the resume uploaded and answer to the following prompt in detail:

{cust}

"""


## streamlit app

st.title("Individual Resume Analyzer")
jd = st.text_area("Paste the job description")
uploaded_file = st.file_uploader("Upload Your resume", type="pdf", help="Please upload your pdf")

submit = st.button("Analyze")


if "responses1" not in st.session_state:
    st.session_state.responses1 = []  # Stores responses from first button



if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        responses1 = get_gemini_response(input_prompt.format(text=text, jd=jd))  # Passed the 'text' and 'jd' values
        st.session_state.responses1.append(responses1)

for resp in st.session_state.responses1:
    st.write(resp)

cust = st.text_area("Ask what you want to know about your resume: ")
submit2 = st.button("Submit")

if "latest_responses2" not in st.session_state:
    st.session_state.latest_responses2 = ""

if submit2:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        responses2 = get_gemini_response(input_prompt2.format(text=text,jd=jd,cust=cust))  # Passed the 'text' and 'jd' values
        st.session_state.latest_responses2 = responses2
  

st.write(st.session_state.latest_responses2)   
