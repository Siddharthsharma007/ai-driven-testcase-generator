import streamlit as st
import requests
import json

# Custom CSS for professional styling
st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-box {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    .error-box {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://localhost:8000"

# Main header
st.markdown("""
<div class="main-header">
    <h1>🧪 AI Test Case Generator</h1>
    <p>Generate comprehensive test cases from requirements using AI</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with navigation
st.sidebar.markdown("## 🧭 Navigation")
page = st.sidebar.selectbox(
    "Choose a section:",
    ["🏠 Dashboard", "📚 Knowledge Base", "❓ Q&A", "🧪 Test Generation", "🧩 UI Suite from Screenshot", "📊 Export"]
)

# Dashboard
if page == "🏠 Dashboard":
    st.markdown("## 📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📚 KB Documents</h3>
            <p>Manage your knowledge base</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🧪 Test Cases</h3>
            <p>Generate comprehensive tests</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>❓ Q&A</h3>
            <p>Ask questions about your KB</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>🚀 Getting Started</h4>
        <p>1. Upload documents to Knowledge Base</p>
        <p>2. Generate test cases with AI</p>
        <p>3. Export results in multiple formats</p>
        <p>4. Ask questions about your requirements</p>
    </div>
    """, unsafe_allow_html=True)

# Knowledge Base
elif page == "📚 Knowledge Base":
    st.markdown("## 📚 Knowledge Base Management")
    
    # Upload section
    st.markdown("### 📤 Upload Documents")
    with st.expander("Add new document to Knowledge Base", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            kb_file = st.file_uploader(
                "Choose a document",
                type=["pdf", "docx", "png", "jpg", "jpeg", "bmp"],
                key="kb_upload"
            )
        with col2:
            kb_tag = st.text_input("Tag/Feature", placeholder="e.g., Login, Payment", key="kb_tag")
        
        if st.button("📤 Upload to KB", key="upload_kb"):
            if kb_file and kb_tag:
                with st.spinner("Uploading and processing..."):
                    files = {"file": (kb_file.name, kb_file, kb_file.type)}
                    data = {"tag": kb_tag}
                    resp = requests.post(f"{BACKEND_URL}/kb/upload", files=files, data=data)
                    if resp.status_code == 200:
                        st.markdown("""
                        <div class="success-box">
                            ✅ Document uploaded and indexed successfully!
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="error-box">
                            ❌ Upload failed: """ + resp.text + """
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Please select a file and enter a tag.")
    
    # List KB entries
    st.markdown("### 📋 Knowledge Base Entries")
    kb_list_resp = requests.get(f"{BACKEND_URL}/kb/list")
    if kb_list_resp.status_code == 200:
        kb_entries = kb_list_resp.json()
        if kb_entries:
            for i, entry in enumerate(kb_entries):
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    with col1:
                        st.markdown(f"**🏷️ Tag:** {entry['tag']}")
                    with col2:
                        st.markdown(f"**📄 File:** {entry['filename']}")
                    with col3:
                        st.markdown(f"**📅 Uploaded:** {entry['uploaded_at'][:10]}")
                    with col4:
                        if st.button("🗑️ Delete", key=f"del_{i}"):
                            resp = requests.delete(
                                f"{BACKEND_URL}/kb/delete",
                                params={"tag": entry['tag'], "filename": entry['filename']}
                            )
                            if resp.status_code == 200:
                                st.success("Entry deleted!")
                                st.rerun()
                            else:
                                st.error("Delete failed!")
        else:
            st.info("No documents in Knowledge Base yet. Upload some documents to get started!")
    else:
        st.error("Could not fetch KB entries.")

# Q&A Section
elif page == "❓ Q&A":
    st.markdown("## ❓ Knowledge Base Q&A")
    
    # Get KB tags for context selection
    kb_list_resp = requests.get(f"{BACKEND_URL}/kb/list")
    if kb_list_resp.status_code == 200:
        kb_entries = kb_list_resp.json()
        tags = list(sorted(set(entry['tag'] for entry in kb_entries)))
        selected_tags = st.multiselect(
            "🔍 Select tags to include in context (optional):",
            tags,
            help="Leave empty to search all documents"
        )
    else:
        selected_tags = []
    
    # Q&A interface
    st.markdown("### 💬 Ask a Question")
    user_question = st.text_area(
        "What would you like to know about your requirements?",
        placeholder="e.g., What is the password reset policy? How does the login flow work?",
        height=100
    )
    
    if st.button("🔍 Get Answer", key="ask_kb"):
        if user_question.strip():
            with st.spinner("🤔 Thinking..."):
                resp = requests.post(
                    f"{BACKEND_URL}/kb/ask",
                    json={"question": user_question, "tags": selected_tags}
                )
                if resp.status_code == 200:
                    answer = resp.json().get("answer", "No answer found.")
                    st.markdown("""
                    <div class="success-box">
                        <h4>💡 Answer:</h4>
                        """ + answer + """
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="error-box">
                        ❌ Failed to get answer from KB.
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Please enter a question.")

# Test Generation
elif page == "🧪 Test Generation":
    st.markdown("## 🧪 Test Case Generation")
    
    # Get KB tags for context
    kb_list_resp = requests.get(f"{BACKEND_URL}/kb/list")
    if kb_list_resp.status_code == 200:
        kb_entries = kb_list_resp.json()
        tags = list(sorted(set(entry['tag'] for entry in kb_entries)))
        selected_tags = st.multiselect(
            "📚 Include KB context (optional):",
            tags,
            help="Select tags to include their content as context for better test generation"
        )
    else:
        selected_tags = []
    
    # Test Coverage Options
    st.markdown("### 🎯 Test Coverage Options")
    coverage_level = st.selectbox(
        "📊 Coverage Level:",
        ["Comprehensive (30-50 test cases)", "Standard (15-25 test cases)", "Basic (8-12 test cases)"],
        help="Choose the level of test coverage you need"
    )
    
    # Input section
    st.markdown("### 📝 Requirements Input")
    tab1, tab2 = st.tabs(["📄 Upload Document", "✍️ Manual Input"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Upload BRD or Image",
            type=["pdf", "docx", "png", "jpg", "jpeg", "bmp"],
            key="main_upload"
        )
    
    with tab2:
        manual_text = st.text_area(
            "Paste your requirements here:",
            placeholder="Describe the feature or requirements for which you want to generate test cases...",
            height=200
        )
    
    # Output format selection
    st.markdown("### 📊 Output Format")
    formats = st.multiselect(
        "Select output formats:",
        ["csv", "excel", "json"],
        default=["csv"],
        help="Choose the formats you want to export"
    )
    
    # Generate button
    if st.button("🚀 Generate Test Cases", key="generate"):
        # Gather KB context
        kb_context = ""
        for tag in selected_tags:
            resp = requests.get(f"{BACKEND_URL}/kb/get_text", params={"tag": tag})
            if resp.status_code == 200:
                kb_context += resp.json().get("text", "") + "\n\n"
        
        # Get requirements text
        if uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            resp = requests.post(f"{BACKEND_URL}/upload", files=files)
            if resp.status_code == 200:
                text = resp.json()["text"]
            else:
                st.error("File extraction failed.")
                st.stop()
        elif manual_text.strip():
            text = manual_text
        else:
            st.warning("Please upload a file or enter requirements text.")
            st.stop()
        
        # Combine KB context and requirements
        full_text = (kb_context + text).strip()
        
        with st.spinner("🤖 Generating comprehensive test cases with AI..."):
            resp = requests.post(f"{BACKEND_URL}/generate", data={"text": full_text})
            if resp.status_code == 200:
                cases = resp.json()["cases"]
                if not cases:
                    st.error("AI did not return any test cases.")
                    st.stop()
            else:
                st.error("AI generation failed.")
                st.stop()
        
        st.markdown("""
        <div class="success-box">
            ✅ Generated """ + str(len(cases)) + """ test cases successfully!
        </div>
        """, unsafe_allow_html=True)
        
        # Display results
        st.markdown("### 📋 Generated Test Cases")
        st.dataframe(cases, use_container_width=True)
        
        # Export section
        st.markdown("### 📤 Export Results")
        if st.button("📦 Download as ZIP"):
            with st.spinner("📦 Creating ZIP file..."):
                resp = requests.post(f"{BACKEND_URL}/export", json={"cases": cases, "formats": formats})
                if resp.status_code == 200:
                    st.download_button(
                        "📥 Download ZIP",
                        resp.content,
                        file_name="test_cases.zip",
                        mime="application/zip"
                    )
                else:
                    st.error("Export failed.")

# UI Suite from Screenshot
elif page == "🧩 UI Suite from Screenshot":
    st.markdown("## 🧩 UI-based Test Suite from Screenshot")
    st.markdown(
        "Upload a UI screenshot and let the AI generate a production-grade test suite, locators, and automation examples."
    )

    ui_file = st.file_uploader(
        "Upload UI screenshot",
        type=["png", "jpg", "jpeg", "bmp"],
        key="ui_suite_upload",
    )

    col_left, col_right = st.columns([1, 1])
    with col_left:
        if ui_file:
            st.image(ui_file, caption="Uploaded UI Screenshot", use_column_width=True)

    with col_right:
        st.markdown(
            """
            <div class="info-box">
                <h4>What will be generated?</h4>
                <p>• 50+ detailed test cases (functional, UI, validation, negative, boundary, security, accessibility, cross-browser, mobile)</p>
                <p>• Suggested CSS/XPath/Playwright locators</p>
                <p>• Example automation snippets in Playwright + TypeScript and Selenium + Java (POM)</p>
                <p>• Coverage summary, risk areas, smoke & regression suites</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("🚀 Generate UI Test Suite", key="generate_ui_suite"):
        if not ui_file:
            st.warning("Please upload a UI screenshot first.")
        else:
            with st.spinner("🤖 Analyzing UI and generating suite..."):
                files = {"file": (ui_file.name, ui_file, ui_file.type)}
                resp = requests.post(f"{BACKEND_URL}/generate_ui_suite", files=files)

                if resp.status_code != 200:
                    st.markdown(
                        f"""
                        <div class="error-box">
                            ❌ Failed to generate UI test suite: {resp.text}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    suite = resp.json().get("suite", {})
                    ui_elements = suite.get("ui_elements", [])
                    test_cases = suite.get("test_cases", [])
                    locators = suite.get("locators", [])
                    automation_examples = suite.get("automation_examples", {})
                    coverage_summary = suite.get("coverage_summary", "")
                    risk_areas = suite.get("risk_areas", [])
                    smoke_suite = suite.get("smoke_suite", [])
                    regression_suite = suite.get("regression_suite", [])

                    st.markdown(
                        f"""
                        <div class="success-box">
                            ✅ Generated {len(test_cases)} test cases and {len(locators)} locators successfully!
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # UI elements
                    st.markdown("### 🧱 Identified UI Elements")
                    if ui_elements:
                        st.dataframe(ui_elements, use_container_width=True)
                    else:
                        st.info("No UI elements returned.")

                    # Test cases
                    st.markdown("### 📋 Generated Test Cases")
                    if test_cases:
                        st.dataframe(test_cases, use_container_width=True)
                    else:
                        st.info("No test cases returned.")

                    # Locators
                    st.markdown("### 🎯 Suggested Locators")
                    if locators:
                        st.dataframe(locators, use_container_width=True)
                    else:
                        st.info("No locators returned.")

                    # Automation examples
                    st.markdown("### 🤖 Automation Examples")
                    pw_example = automation_examples.get("playwright_typescript")
                    sel_example = automation_examples.get("selenium_java")

                    if pw_example:
                        with st.expander("Playwright + TypeScript (POM Example)", expanded=False):
                            st.markdown(pw_example, unsafe_allow_html=True)
                    else:
                        st.info("No Playwright example returned.")

                    if sel_example:
                        with st.expander("Selenium + Java (POM Example)", expanded=False):
                            st.markdown(sel_example, unsafe_allow_html=True)
                    else:
                        st.info("No Selenium example returned.")

                    # Strategy outputs
                    st.markdown("### 📊 Test Strategy Summary")
                    if coverage_summary:
                        st.markdown(f"**Coverage Summary:**\n\n{coverage_summary}")

                    if risk_areas:
                        st.markdown("**Risk Areas:**")
                        for r in risk_areas:
                            st.markdown(f"- {r}")

                    if smoke_suite:
                        st.markdown("**Recommended Smoke Suite:**")
                        for tc in smoke_suite:
                            st.markdown(f"- {tc.get('Test Case ID', '')}: {tc.get('Title', '')}")

                    if regression_suite:
                        st.markdown("**Recommended Regression Suite:**")
                        for tc in regression_suite:
                            st.markdown(f"- {tc.get('Test Case ID', '')}: {tc.get('Title', '')}")

# Export section
elif page == "📊 Export":
    st.markdown("## 📊 Export & Download")
    st.info("Use the Test Generation section to create and export test cases.")
    st.markdown("""
    <div class="info-box">
        <h4>📤 Export Options</h4>
        <p>• CSV - For spreadsheet applications</p>
        <p>• Excel - For Microsoft Excel</p>
        <p>• JSON - For Jira Xray integration</p>
        <p>• ZIP - All formats bundled together</p>
    </div>
    """, unsafe_allow_html=True) 