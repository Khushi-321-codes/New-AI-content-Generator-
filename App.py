import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Content Generator", layout="wide")

# API Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.0-pro')

# Initialize History
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Sidebar ---
st.sidebar.title("📜 History")
for i, entry in enumerate(st.session_state.history):
    st.sidebar.write(f"Draft {i+1}: {entry[:20]}...")

# --- Main App ---
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
            prompt = f"Role: {mode}. Update: {user_input}. URL: {url_input}. Language: {language}. Audience: {target_audience}. Platforms: {', '.join(platforms) if platforms else 'None'}."
            try:
                response = model.generate_content(prompt)
                result = response.text
                st.session_state.history.append(result)
                st.success("Draft Generated!")
                st.write(result)
                st.download_button("📥 Download Result", result, file_name="generated_content.txt")
            except Exception as e:
                st.error(f"Generation Error: {e}")
