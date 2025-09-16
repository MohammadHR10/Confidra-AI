import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import io
import os
from typing import List, Dict
import tempfile

# Try to import document processing libraries
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    import docx
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

# Configure page
st.set_page_config(
    page_title="Confidra AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Custom CSS for the new design
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app styling */
    .stApp {
        background: #1E2A38;
        color: white;
    }
    
    .main-container {
        background: #1E2A38;
        min-height: 100vh;
        padding: 2rem;
    }
    
    /* Header styling */
    .app-header {
        display: flex;
        align-items: center;
        margin-bottom: 3rem;
        padding: 1rem 0;
    }
    
    .app-logo {
        width: 32px;
        height: 32px;
        background: #F4F5F7;
        border-radius: 50%;
        margin-right: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #1E2A38;
    }
    
    .app-title {
        color: #F4F5F7;
        font-size: 20px;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        margin: 0;
    }
    
    /* Main content styling */
    .hero-section {
        text-align: center;
        margin: 4rem 0;
    }
    
    .hero-title {
        color: white;
        font-size: 40px;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        color: #E5E5E5;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .hero-description {
        color: white;
        font-size: 24px;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        margin-bottom: 3rem;
    }
    
    /* Upload area styling */
    .upload-container {
        max-width: 720px;
        margin: 0 auto;
        background: white;
        border-radius: 8px;
        border: 1px solid #E5E5E5;
        padding: 2rem;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    /* Button styling */
    .scan-button {
        background: #1E2A38;
        color: white;
        border: 1px solid #E5E5E5;
        border-radius: 8px;
        padding: 12px 20px;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        font-size: 16px;
        margin: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .scan-button:hover {
        background: #2A3A48;
        transform: translateY(-2px);
    }
    
    .scan-button-danger {
        background: #E63946;
        border: 1px solid #E63946;
    }
    
    .scan-button-danger:hover {
        background: #D62828;
    }
    
    /* Results styling */
    .result-container {
        max-width: 800px;
        margin: 2rem auto;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .status-approved {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .status-blocked {
        background: linear-gradient(135deg, #E63946, #D62828);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .status-redacted {
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    /* Override Streamlit default styles */
    .stTextArea textarea {
        background: white !important;
        color: #333 !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 8px !important;
    }
    
    .stFileUploader > div {
        background: white;
        border-radius: 8px;
        border: 2px dashed #8A38F5;
        padding: 2rem;
    }
    
    .stButton button {
        background: #1E2A38 !important;
        color: white !important;
        border: 1px solid #E5E5E5 !important;
        border-radius: 8px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background: #2A3A48 !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    if not PDF_SUPPORT:
        return "PDF processing not available. Please install PyPDF2."
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    if not DOCX_SUPPORT:
        return "DOCX processing not available. Please install python-docx."
    
    try:
        doc = docx.Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def process_document(uploaded_file):
    """Process uploaded document and extract text"""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    else:
        return "Unsupported file type. Please upload PDF, DOCX, or TXT files."

def main():
    # Add Google Fonts
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="app-logo">🛡️</div>
        <h1 class="app-title">Confidra AI</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Scan your contract for NDA risks.</h1>
        <p class="hero-subtitle">Your data is processed securely and never stored.</p>
        <p class="hero-description">Upload a document or paste text below.<br/>We'll scan it against your NDA and compliance rules</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for the upload options
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 Upload Document")
        uploaded_file = st.file_uploader(
            "",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT files",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            if st.button("🔍 SCAN FOR RISKS", key="upload_scan"):
                with st.spinner("🔄 Processing document..."):
                    # Extract text from document
                    text_content = process_document(uploaded_file)
                    
                    if text_content and not text_content.startswith("Error"):
                        # Upload to backend
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/upload-document",
                                data={
                                    "filename": uploaded_file.name,
                                    "content": text_content,
                                    "sensitivity": "protected",
                                    "timestamp": datetime.now().isoformat()
                                }
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                st.markdown(f"""
                                <div class="status-approved">
                                    ✅ Document processed successfully!<br/>
                                    {result['clauses_extracted']} clauses extracted and classified
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Store in session state for querying
                                st.session_state.document_processed = True
                                st.session_state.document_name = uploaded_file.name
                            else:
                                st.markdown("""
                                <div class="status-blocked">
                                    ❌ Failed to process document
                                </div>
                                """, unsafe_allow_html=True)
                                
                        except Exception as e:
                            st.markdown(f"""
                            <div class="status-blocked">
                                ❌ Error: {str(e)}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="status-blocked">
                            ❌ Failed to extract text: {text_content}
                        </div>
                        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ✏️ Paste Text")
        text_input = st.text_area(
            "",
            placeholder="Paste your contract or NDA text here...",
            height=200,
            label_visibility="collapsed"
        )
        
        if text_input:
            if st.button("🔍 SCAN FOR RISKS", key="text_scan"):
                with st.spinner("🔄 Scanning text..."):
                    try:
                        # Upload text to backend
                        response = requests.post(
                            f"{BACKEND_URL}/upload-document",
                            data={
                                "filename": "pasted_text.txt",
                                "content": text_input,
                                "sensitivity": "protected",
                                "timestamp": datetime.now().isoformat()
                            }
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.markdown(f"""
                            <div class="status-approved">
                                ✅ Text processed successfully!<br/>
                                {result['clauses_extracted']} clauses extracted and classified
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Store in session state for querying
                            st.session_state.document_processed = True
                            st.session_state.document_name = "pasted_text.txt"
                        else:
                            st.markdown("""
                            <div class="status-blocked">
                                ❌ Failed to process text
                            </div>
                            """, unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.markdown(f"""
                        <div class="status-blocked">
                            ❌ Error: {str(e)}
                        </div>
                        """, unsafe_allow_html=True)
    
    # Query Section (only show if document is processed)
    if st.session_state.get('document_processed', False):
        st.markdown("---")
        st.markdown("""
        <div class="hero-section">
            <h2 style="color: white; font-size: 32px; margin-bottom: 2rem;">Ask Questions About Your Contract</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Query input
        query = st.text_input(
            "",
            placeholder="e.g., How many vacation days are provided? What are the termination terms?",
            label_visibility="collapsed"
        )
        
        if query and st.button("🚀 ASK QUESTION", key="query_button"):
            with st.spinner("🤔 Analyzing your question..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/ask",
                        json={"query": query, "user_id": "web_user"},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display result based on action
                        if result["action"] == "pass":
                            st.markdown(f"""
                            <div class="status-approved">
                                ✅ <strong>APPROVED</strong><br/>
                                {result["safe_output"]}
                            </div>
                            """, unsafe_allow_html=True)
                        elif result["action"] == "blocked":
                            st.markdown(f"""
                            <div class="status-blocked">
                                🚫 <strong>BLOCKED</strong><br/>
                                Reason: {result['reason']}<br/>
                                {result["safe_output"]}
                            </div>
                            """, unsafe_allow_html=True)
                        elif result["action"] == "redacted":
                            st.markdown(f"""
                            <div class="status-redacted">
                                ✏️ <strong>REDACTED</strong><br/>
                                Reason: {result['reason']}<br/>
                                {result["safe_output"]}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="status-blocked">
                            ❌ API Error: {response.status_code}
                        </div>
                        """, unsafe_allow_html=True)
                        
                except requests.exceptions.RequestException as e:
                    st.markdown(f"""
                    <div class="status-blocked">
                        ❌ Connection error: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="status-blocked">
                        ❌ Unexpected error: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
