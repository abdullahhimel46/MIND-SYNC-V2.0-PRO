import streamlit as st
import requests
import time
import PyPDF2
from docx import Document
import io

# Page Config
st.set_page_config(page_title="Minimal RAG", page_icon="🧠", layout="centered")

# --- UTILS FOR FILE PARSING ---
def extract_text(file):
    try:
        if file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file)
            return " ".join([page.extract_text() for page in pdf_reader.pages])
        elif file.name.endswith('.docx'):
            doc = Document(file)
            return " ".join([para.text for para in doc.paragraphs])
        else:
            return file.read().decode('utf-8')
    except Exception as e:
        return f"Error parsing file: {e}"

# --- LOAD CUSTOM CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- UI CONTENT ---
st.markdown('<h1 class="main-title">MIND SYNC</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">AUGMENTED INTELLIGENCE</p>', unsafe_allow_html=True)

# --- KNOWLEDGE HUB (EXPANDER) ---
with st.expander("📂 KNOWLEDGE HUB"):
    st.info("Upload documents to expand the AI's knowledge base in real-time.")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file:
        if st.button("🚀 SYNC TO MIND"):
            with st.spinner("Neural Processing..."):
                text_content = extract_text(uploaded_file)
                if text_content and not text_content.startswith("Error"):
                    try:
                        res = requests.post("http://127.0.0.1:8000/upload", json={"text": text_content})
                        if res.status_code == 200:
                            st.success(f"Successfully Synced: {uploaded_file.name}")
                            st.balloons()
                        else:
                            st.error(f"Sync Error: {res.status_code}")
                    except Exception as e:
                        st.error(f"Connection Failed: {e}")
                else:
                    st.error("Parsing failed. Please check the file format.")

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble"><b>AI:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# Input area
with st.form("query_form", clear_on_submit=True):
    query = st.text_input("", placeholder="Ask anything to your documents...")
    submit = st.form_submit_button("SEND QUERY")

if submit and query.strip():
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": query.strip()})
    st.rerun()

# Logic to handle response (after rerun)
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    last_query = st.session_state.messages[-1]["content"]
    
    with st.status("🧠 Mind Syncing...", expanded=True) as status:
        st.write("Retrieving context from documents...")
        try:
            res = requests.post("http://127.0.0.1:8000/chat", json={"query": last_query})
            if res.status_code == 200:
                data = res.json()
                answer = data["answer"]
                context = data.get("context", "No specific sources found.")
                
                # Format response with sources
                full_content = f"{answer}\n\n---\n**Sources Found:**\n{context}"
                
                st.session_state.messages.append({"role": "assistant", "content": full_content})
                status.update(label="Sync Complete!", state="complete", expanded=False)
            else:
                st.session_state.messages.append({"role": "assistant", "content": "Error: Backend unreachable."})
                status.update(label="Sync Failed", state="error", expanded=False)
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Connection Error: {e}"})
            status.update(label="Connection Error", state="error", expanded=False)
    st.rerun()

# --- SEXY FOOTER ---
st.markdown("""
    <div class="footer">
        MIND SYNC V2.0 PRO • © 2026 ALL RIGHTS RESERVED <br>
        DEV <span>ABDULLAH</span>
    </div>
""", unsafe_allow_html=True)
