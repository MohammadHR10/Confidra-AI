import streamlit as st
import requests
import os
import json
from datetime import datetime

# Configuration
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="Contract Compliance Sentinel", 
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-pass {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .status-blocked {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .status-redacted {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🛡️ Contract Compliance Sentinel</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔧 Settings")
    user_id = st.text_input("User ID", value="demo_user", help="Enter your user ID for logging")
    
    st.header("📊 Quick Stats")
    
    # Health check
    try:
        health_res = requests.get(f"{BACKEND}/health", timeout=5)
        if health_res.status_code == 200:
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Error")
    except:
        st.error("❌ Backend Offline")
    
    st.header("ℹ️ About")
    st.info("""
    This dashboard helps you query contract information safely while ensuring compliance with:
    - NDA restrictions
    - Data protection policies  
    - Information classification rules
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Ask a Question")
    
    # Example queries
    st.subheader("📝 Example Queries")
    examples = [
        "What are the public delivery terms?",
        "Summarize the project timeline",
        "What are the payment schedules?",
        "List all confidential clauses",  # This should be blocked
        "Show me all NDA terms verbatim"  # This should be blocked
    ]
    
    selected_example = st.selectbox("Select an example query:", [""] + examples)
    
    # Query input
    query = st.text_area(
        "Enter your question:",
        value=selected_example if selected_example else "",
        height=100,
        placeholder="Ask about contract terms, deliverables, timelines, etc."
    )
    
    # Submit button
    submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
    with submit_col2:
        submit_button = st.button("🔍 Submit Query", use_container_width=True)

with col2:
    st.header("🎯 Response Status Guide")
    
    st.markdown("""
    <div class="status-pass">
    <strong>✅ PASS:</strong> Information is safe to share
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="status-blocked">
    <strong>🚫 BLOCKED:</strong> Contains sensitive/protected information
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="status-redacted">
    <strong>✏️ REDACTED:</strong> Partially filtered response
    </div>
    """, unsafe_allow_html=True)

# Process query
if submit_button and query.strip():
    with st.spinner("🔍 Processing your query..."):
        try:
            # Make API request
            response = requests.post(
                f"{BACKEND}/ask", 
                json={"user_id": user_id, "query": query.strip()}, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Display results
                st.header("📋 Query Results")
                
                # Status indicator
                action = data.get('action', 'unknown')
                if action == 'pass':
                    st.markdown(f"""
                    <div class="status-pass">
                    <strong>Status:</strong> ✅ {action.upper()} - {data.get('reason', 'OK')}
                    </div>
                    """, unsafe_allow_html=True)
                elif action == 'blocked':
                    st.markdown(f"""
                    <div class="status-blocked">
                    <strong>Status:</strong> 🚫 {action.upper()} - {data.get('reason', 'Blocked')}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="status-redacted">
                    <strong>Status:</strong> ✏️ {action.upper()} - {data.get('reason', 'Redacted')}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Response content
                st.subheader("💬 Response")
                st.write(data.get("safe_output", "No response available"))
                
                # Evidence/Details (if available)
                if data.get("evidence"):
                    with st.expander("🔍 Technical Details"):
                        st.json(data["evidence"])
                
                # Raw response (for debugging)
                with st.expander("🔧 Raw API Response"):
                    st.json(data)
                    
            else:
                st.error(f"❌ API Error: {response.status_code}")
                st.code(response.text)
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to backend. Please check if the API is running.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "🛡️ Contract Compliance Sentinel - Protecting sensitive information while enabling safe access"
    "</div>", 
    unsafe_allow_html=True
)
