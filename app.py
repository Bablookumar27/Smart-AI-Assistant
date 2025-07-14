import streamlit as st
import fitz  # PyMuPDF
import requests
import time
import os

# === CONFIG ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDBlRNCS5RCxjI09ggtUqx3OdTeZ76okpw")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={GEMINI_API_KEY}"

# === UTILS ===

def call_gemini_api(payload, retries=5, delay=10):
    last_response_text = ""
    for attempt in range(retries):
        response = requests.post(GEMINI_API_URL, json=payload)
        last_response_text = response.text
        if response.status_code == 429:
            st.warning(f"Quota exhausted. Retrying in {delay} seconds...")
            time.sleep(delay)
        elif not response.ok:
            st.warning(f"Request failed. Status: {response.status_code}. Retrying...")
            time.sleep(delay)
        else:
            return response.json()
    st.error(f"Gemini API error after retries. Last response:\n{last_response_text}")
    st.stop()

def extract_text_from_pdf(uploaded_file_bytes):
    pdf_text = ""
    doc = fitz.open(stream=uploaded_file_bytes, filetype="pdf")
    for page in doc:
        pdf_text += page.get_text()
    return pdf_text

def split_text_by_tokens(text, max_tokens=300):
    avg_token_length = 4
    chunk_size = max_tokens * avg_token_length
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_large_text(text, lang, chunk_size=300):
    chunks = split_text_by_tokens(text, max_tokens=chunk_size)
    summaries = []
    for i, chunk in enumerate(chunks):
        if lang == "Hindi":
            prompt = f"निम्नलिखित शोध पत्र के इस भाग को सरल हिंदी में संक्षेपित करें:\n\n{chunk}"
        else:
            prompt = f"Please summarize this part of the research paper in simple English:\n\n{chunk}"

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        response_json = call_gemini_api(payload)
        part_summary = response_json["candidates"][0]["content"]["parts"][0]["text"]
        summaries.append(part_summary)
    return "\n\n".join(summaries)

def answer_question_with_context(summary_text, question, lang):
    if lang == "Hindi":
        prompt = f"""
नीचे शोध पत्र का सारांश दिया गया है:\n\n{summary_text[:2000]}

अब निम्नलिखित प्रश्न का उत्तर दो:\n\n{question}
"""
    else:
        prompt = f"""
Below is the summary of a research paper:\n\n{summary_text[:2000]}

Now answer this question:\n\n{question}
"""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 300
        }
    }
    response_json = call_gemini_api(payload)
    return response_json["candidates"][0]["content"]["parts"][0]["text"]

def general_chat_response(message, lang):
    if lang == "Hindi":
        prompt = f"तुम एक बुद्धिमान सहायक हो। इस प्रश्न का उत्तर हिंदी में दो:\n\n{message}"
    else:
        prompt = f"You are a smart assistant. Please respond:\n\n{message}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 300
        }
    }
    response_json = call_gemini_api(payload)
    return response_json["candidates"][0]["content"]["parts"][0]["text"]

# === UI SETUP ===

st.set_page_config(page_title="Research Paper Chatbot", layout="wide")
st.markdown("""
    <style>
        .big-title {font-size: 36px; color: #4CAF50; font-weight: bold;}
        .sub-title {font-size: 20px; color: #2196F3;}
    </style>
""", unsafe_allow_html=True)
st.markdown('<p class="big-title">📄 Research Paper Chatbot Assistant</p>', unsafe_allow_html=True)

# Sidebar settings
st.sidebar.title("Settings")
lang = st.sidebar.radio("Choose Language:", ["English", "Hindi"])
chunk_size = st.sidebar.slider("Chunk Size (Tokens)", 100, 600, 300)
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []

# Session state
if "paper_text" not in st.session_state:
    st.session_state.paper_text = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload PDF
uploaded_file = st.file_uploader("📤 Upload a research paper (PDF)", type="pdf")

if uploaded_file:
    uploaded_file_bytes = uploaded_file.read()
    extracted_text = extract_text_from_pdf(uploaded_file_bytes)
    st.session_state.paper_text = extracted_text

    st.success("✅ PDF uploaded and extracted successfully.")
    st.markdown('<p class="sub-title">Preview (first 500 characters):</p>', unsafe_allow_html=True)
    st.code(extracted_text[:500])

    # Extract abstract or limit
    text_lower = extracted_text.lower()
    abs_start = text_lower.find("abstract")
    concl_start = text_lower.find("conclusion")

    if abs_start != -1 and concl_start != -1:
        text_to_summarize = extracted_text[abs_start:concl_start]
    else:
        text_to_summarize = extracted_text[:3000]

    with st.spinner("Summarizing..."):
        summary = summarize_large_text(text_to_summarize, lang, chunk_size=chunk_size)
        st.session_state.summary = summary

    st.markdown("### 📝 Paper Summary")
    st.write(summary)
    st.download_button("📥 Download Summary", summary, file_name="summary.txt")

# Chat Interface (Always Visible)
st.subheader("💬Smart Assistant")

for role, message in st.session_state.chat_history:
    if role == "User":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.chat_history.append(("User", prompt))
    if st.session_state.summary is None:
        with st.spinner("Summarizing quickly..."):
            if lang == "Hindi":
                prompt = f"निम्नलिखित टेक्स्ट को सरल हिंदी में संक्षेपित करें:\n\n{text_to_summarize}"
            else:
                prompt = f"Please summarize the following text in simple English:\n\n{text_to_summarize}"

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 500
            }
        }
        response_json = call_gemini_api(payload)
        summary = response_json["candidates"][0]["content"]["parts"][0]["text"]
        st.session_state.summary = summary
else:
    summary = st.session_state.summary

