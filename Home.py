import streamlit as st

st.set_page_config(page_title="Homepage", page_icon="🏡")

st.title("🏡 Welcome to the Homepage")
st.write("Click the button below to go to the App page.")

# Button to navigate
st.page_link("pages/IndividualAnalyzer.py", label="Go to App", icon="🚀")
