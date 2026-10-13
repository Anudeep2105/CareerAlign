import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Resume Optimizer", page_icon="🚀")

st.title("🚀 AI Resume ATS Optimizer")
st.markdown("Upload your resume and JDs to create ATS-proof resumes.")

# Configuration
API_URL_UPLOAD = "http://127.0.0.1:8000/upload"
API_URL_OPTIMIZE = "http://127.0.0.1:8000/optimize"
API_URL_BATCH = "http://127.0.0.1:8000/optimize-batch"

# Model Selection
st.sidebar.header("Settings")
selected_model = st.sidebar.text_input("AI Model Name", value="llama-3.1-8b-instant", help="Check Groq Console for current models (e.g., llama-3.1-70b-versatile, mixtral-8x7b-32768)")

tab1, tab2, tab3 = st.tabs(["✨ Optimize Single", "📦 Batch Optimize", "📁 Standard Parse"])

with tab1:
    st.header("Optimize for Single JD")
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="opt_file")
    jd_text = st.text_area("Paste Job Description (JD) here:", height=200)

    if st.button("Generate ATS-Proof Resume"):
        if uploaded_file and jd_text:
            with st.spinner("AI is optimizing your resume..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {"jd": jd_text, "model": selected_model}
                    response = requests.post(API_URL_OPTIMIZE, files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Resume Optimized Successfully!")
                        st.subheader("Optimized Content Preview:")
                        st.markdown(result["optimized_text"])
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")
        else:
            st.warning("Please upload a resume and provide a JD.")

with tab2:
    st.header("Batch Optimize from URLs")
    st.info("Upload a .txt file containing one JD URL per line.")
    batch_resume = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="batch_res")
    links_file = st.file_uploader("Upload URLs File (.txt)", type=["txt"], key="links_file")

    if st.button("Generate All Resumes"):
        if batch_resume and links_file:
            with st.spinner("Processing multiple JDs... this may take a minute..."):
                try:
                    files = {
                        "file": (batch_resume.name, batch_resume.getvalue(), batch_resume.type),
                        "links_file": (links_file.name, links_file.getvalue(), links_file.type)
                    }
                    data = {"model": selected_model}
                    response = requests.post(API_URL_BATCH, files=files, data=data)
                    
                    if response.status_code == 200:
                        results = response.json().get("results", [])
                        st.success(f"✅ Processed {len(results)} JDs!")
                        
                        for res in results:
                            with st.expander(f"URL: {res.get('url')} - {res.get('status')}"):
                                if res.get('status') == "Success":
                                    st.markdown(res.get('text'))
                                    st.write(f"📄 File saved as: {res.get('file')}")
                                else:
                                    st.error(res.get('error'))
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")
        else:
            st.warning("Please upload both the resume and the links file.")

with tab3:
    st.header("Standard Resume Parsing")
    uploaded_file_parse = st.file_uploader("Choose a resume file", type=["pdf", "docx", "jpg", "jpeg", "png"], key="parse_file")

    if st.button("Parse and Save to DB"):
        if uploaded_file_parse:
            with st.spinner("Parsing..."):
                try:
                    files = {"file": (uploaded_file_parse.name, uploaded_file_parse.getvalue(), uploaded_file_parse.type)}
                    response = requests.post(API_URL_UPLOAD, files=files)
                    if response.status_code == 200:
                        st.success(f"✅ {response.json()['status']}! File: {response.json()['filename']}")
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("Please upload a file.")

st.divider()
st.caption("Powered by GPT-4o | URL-Based Batch Optimizer")
