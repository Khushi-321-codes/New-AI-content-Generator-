import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Content Generator", layout="centered")

# API Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.title("✨ AI Content Generator")

mode = st.selectbox("Select Role:", ["Student", "Creator", "Business Brand"])
user_input = st.text_area("What's the update today?")
url_input = st.text_input("🔗 Paste a URL to analyze:")

if st.button("✨ Generate Content"):
    if not user_input:
        st.warning("Please provide input!")
    else:
        with st.spinner("Generating..."):
            prompt = f"Write content for a {mode} about: {user_input}. URL: {url_input}"
            response = model.generate_content(prompt)
            st.success("Draft Generated!")
            st.write(response.text)
