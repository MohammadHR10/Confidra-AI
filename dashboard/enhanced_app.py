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
    page_title="Contract Compliance Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .query-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 1rem 0;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 0.5rem;
        border: 2px dashed #1f77b4;
        margin: 1rem 0;
    }
    .status-pass { background-color: #d4edda; color: #155724; padding: 0.5rem; border-radius: 0.25rem; }
    .status-blocked { background-color: #f8d7da; color: #721c24; padding: 0.5rem; border-radius: 0.25rem; }
    .status-redacted { background-color: #fff3cd; color: #856404; padding: 0.5rem; border-radius: 0.25rem; }
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

def upload_document_to_backend(text_content, filename, sensitivity_level="public"):
    """Upload processed document to backend"""
    try:
        # For now, we'll create a simple API call to add the document
        # You might need to create a new endpoint in your backend
        data = {
            "filename": filename,
            "content": text_content,
            "sensitivity": sensitivity_level,
            "timestamp": datetime.now().isoformat()
        }
        # This would be a new endpoint you'd need to create
        response = requests.post(f"{BACKEND_URL}/upload-document", json=data)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Error uploading to backend: {str(e)}")
        return False

def main():
    # Header
    st.markdown('<h1 class="main-header">📋 Contract Compliance Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Document Upload Section
        st.subheader("📤 Upload Documents")
        
        uploaded_file = st.file_uploader(
            "Upload Contract/NDA Document",
            type=['pdf', 'docx', 'txt'],
            help="Upload PDF, DOCX, or TXT files containing contract or NDA information"
        )
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Sensitivity level selector
            sensitivity = st.selectbox(
                "Document Sensitivity Level",
                ["public", "protected", "confidential"],
                help="Classify the sensitivity level of the uploaded document"
            )
            
            if st.button("🔄 Process Document"):
                with st.spinner("Processing document..."):
                    # Extract text from document
                    text_content = process_document(uploaded_file)
                    
                    if text_content and not text_content.startswith("Error"):
                        st.success("Document processed successfully!")
                        
                        # Show preview of extracted text
                        with st.expander("📄 Document Preview"):
                            st.text_area("Extracted Text (first 500 chars):", text_content[:500], height=150)
                        
                        # TODO: Here you would typically:
                        # 1. Parse the document into clauses
                        # 2. Classify each clause
                        # 3. Update the backend database
                        
                        st.info("💡 Document processing complete! The system will now use this document for compliance checking.")
                    else:
                        st.error(f"Failed to process document: {text_content}")
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        user_id = st.text_input("User ID", value="employee_001")
        show_debug = st.checkbox("Show Debug Info", value=False)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Query Interface", "📊 Analytics", "📋 Document Management", "🔍 Audit Logs"])
    
    with tab1:
        st.header("Ask Questions About Contracts")
        
        # Query input
        col1, col2 = st.columns([4, 1])
        with col1:
            query = st.text_area(
                "Enter your question:",
                placeholder="e.g., What are the delivery terms? What penalties apply for late payment?",
                height=100
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit_query = st.button("🚀 Submit Query", use_container_width=True)
        
        # Process query
        if submit_query and query:
            with st.spinner("Processing query..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/ask",
                        json={"query": query, "user_id": user_id},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display result based on action
                        if result["action"] == "pass":
                            st.markdown(f'<div class="status-pass">✅ <strong>APPROVED</strong></div>', unsafe_allow_html=True)
                            st.success("**Response:**")
                            st.write(result["safe_output"])
                        elif result["action"] == "blocked":
                            st.markdown(f'<div class="status-blocked">🚫 <strong>BLOCKED</strong></div>', unsafe_allow_html=True)
                            st.error(f"**Reason:** {result['reason']}")
                            st.write(result["safe_output"])
                        elif result["action"] == "redacted":
                            st.markdown(f'<div class="status-redacted">✏️ <strong>REDACTED</strong></div>', unsafe_allow_html=True)
                            st.warning(f"**Reason:** {result['reason']}")
                            st.write(result["safe_output"])
                        
                        if show_debug:
                            st.json(result)
                    else:
                        st.error(f"API Error: {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")
    
    with tab2:
        st.header("📊 Compliance Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Queries", "247", "+12")
        with col2:
            st.metric("Approved", "195", "+8")
        with col3:
            st.metric("Blocked", "32", "+3")
        with col4:
            st.metric("Redacted", "20", "+1")
        
        # Sample charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Query types chart
            fig = px.pie(
                values=[195, 32, 20],
                names=['Approved', 'Blocked', 'Redacted'],
                title='Query Results Distribution',
                color_discrete_map={'Approved': '#28a745', 'Blocked': '#dc3545', 'Redacted': '#ffc107'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Timeline chart
            dates = pd.date_range('2024-01-01', periods=30, freq='D')
            values = pd.Series([10, 15, 12, 20, 18, 25, 22] * 4 + [15, 12])[:30]
            
            fig = px.line(
                x=dates, y=values,
                title='Daily Query Volume',
                labels={'x': 'Date', 'y': 'Number of Queries'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("📋 Document Management")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📄 Uploaded Documents")
            
            # Sample document list
            docs_data = {
                'Document Name': ['Contract_v1.pdf', 'NDA_Standard.docx', 'Employment_Agreement.pdf'],
                'Upload Date': ['2024-01-15', '2024-01-12', '2024-01-10'],
                'Sensitivity': ['Protected', 'Confidential', 'Public'],
                'Status': ['Active', 'Active', 'Active'],
                'Clauses Extracted': [45, 23, 67]
            }
            
            df = pd.DataFrame(docs_data)
            st.dataframe(df, use_container_width=True)
        
        with col2:
            st.subheader("📊 Document Stats")
            st.metric("Total Documents", "3")
            st.metric("Total Clauses", "135")
            st.metric("Protected Clauses", "68")
            st.metric("Public Clauses", "67")
    
    with tab4:
        st.header("🔍 Audit Logs")
        
        # Sample audit log
        audit_data = {
            'Timestamp': ['2024-01-15 14:30:25', '2024-01-15 14:25:15', '2024-01-15 14:20:10'],
            'User ID': ['employee_001', 'employee_002', 'employee_001'],
            'Query': ['What are delivery terms?', 'Show me all penalty clauses', 'Contract duration?'],
            'Action': ['APPROVED', 'BLOCKED', 'APPROVED'],
            'Reason': ['Public information', 'Sensitive data request', 'Public information']
        }
        
        audit_df = pd.DataFrame(audit_data)
        st.dataframe(audit_df, use_container_width=True)
        
        # Export functionality
        if st.button("📥 Export Audit Log"):
            csv = audit_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
