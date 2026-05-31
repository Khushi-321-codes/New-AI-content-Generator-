import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Content Generator", layout="centered")

# API Configuration
# Note: Ensure GEMINI_API_KEY is set in Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# --- Helper Function to Clear Inputs ---
def reset_form():
    st.session_state.user_input = ""
    st.session_state.url_input = ""
    st.session_state.mode = "Student"
    st.session_state.language = "English"
    st.session_state.audience = "General"
    st.session_state.platforms = []

# Title & New Content Button
st.title("✨ AI Content Generator")
if st.button("🔄 New Content"):
    st.rerun()

# Input Fields with session_state keys for persistence
mode = st.selectbox("Select Role:", ["Student", "Creator", "Business Brand"], key="mode")
user_input = st.text_area("What's the update today?", key="user_input")
url_input = st.text_input("🔗 Paste a URL to analyze:", key="url_input")

uploaded_file = st.file_uploader("Upload Assets:", type=['jpg', 'png', 'mp4', 'mov'])

col1, col2 = st.columns(2)
with col1:
    language = st.radio("Language:", ["English", "Hinglish"], key="language")
with col2:
    target_audience = st.selectbox("Target Audience:", ["General", "Students", "Professionals", "Kids"], key="audience")

platforms = st.multiselect("Choose Platforms:", ["Instagram", "LinkedIn", "YouTube", "Twitter"], key="platforms")

# Generate Button
if st.button("✨ Generate Content"):
    if not user_input:
        st.warning("Please provide input!")
    else:
        with st.spinner("Generating..."):
            prompt = f"Role: {mode}, Update: {user_input}, URL: {url_input}, Language: {language}, Audience: {target_audience}, Platforms: {platforms}"
            response = model.generate_content(prompt)
            st.success("Draft Generated!")
            st.write(response.text)
            st.download_button("📥 Download Result", response.text, file_name="generated_content.txt")
