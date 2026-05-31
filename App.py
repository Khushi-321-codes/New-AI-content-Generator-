import streamlit as st
import google.generativeai as genai
import os

# Page Configuration
st.set_page_config(page_title="AI Content Generator", layout="wide")

# API Configuration - Force set environment variable
api_key = st.secrets["GEMINI_API_KEY"]
os.environ["GOOGLE_API_KEY"] = api_key
genai.configure(api_key=api_key)

# Model selection - Using 'gemini-pro' specifically to avoid flash/v1beta issues
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Model Load Error: {e}")

# --- UI Components ---
st.title("✨ AI Content Generator")

# Inputs
mode = st.selectbox("Select Role:", ["Student", "Creator", "Business Brand"])
user_input = st.text_area("What's the update today?")
url_input = st.text_input("🔗 Paste a URL to analyze:")

uploaded_file = st.file_uploader("Upload Assets:", type=['jpg', 'png', 'mp4', 'mov'])

col1, col2 = st.columns(2)
with col1:
    language = st.radio("Language:", ["English", "Hinglish"])
with col2:
    target_audience = st.selectbox("Target Audience:", ["General", "Students", "Professionals", "Kids"])

platforms = st.multiselect("Choose Platforms:", ["Facebook", "Instagram", "LinkedIn", "YouTube", "Twitter"])

# Generate Button
if st.button("✨ Generate Content"):
    if not user_input:
        st.warning("Please provide input!")
    else:
        with st.spinner("Generating..."):
            prompt = f"Role: {mode}. Update: {user_input}. URL: {url_input}. Language: {language}. Audience: {target_audience}. Platforms: {', '.join(platforms)}."
            
            try:
                response = model.generate_content(prompt)
                st.success("Draft Generated!")
                st.write(response.text)
                st.download_button("📥 Download Result", response.text, file_name="generated_content.txt")
            except Exception as e:
                st.error(f"Generation Error: {e}")
