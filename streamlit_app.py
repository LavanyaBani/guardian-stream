import streamlit as st
import subprocess
import json
from pathlib import Path

st.set_page_config(page_title="GuardianStream", layout="wide")

st.title("🛡️ GuardianStream")
st.markdown("### Multi-Modal Sports Media Forensics Engine")

# Sidebar
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose Module", ["Piracy Detector", "Authenticity Detector"])

if option == "Piracy Detector":
    st.header("🔒 Piracy Detection Engine")
    st.write("Detect unauthorized broadcasts and trace leak sources")
    
    if st.button("🎬 Run Leak Detection Demo", type="primary"):
        with st.spinner("Running forensic analysis..."):
            try:
                result = subprocess.run(
                    ["python", "src/simulate_leak_trace.py"],
                    capture_output=True,
                    text=True,
                    cwd="D:\\guardian-stream"
                )
                
                st.success("✅ Analysis Complete!")
                st.code(result.stdout)
                
                # Show report if exists
                report_path = Path("D:\\guardian-stream\\leak_trace_report.json")
                if report_path.exists():
                    with open(report_path) as f:
                        report = json.load(f)
                    st.json(report)
                    
            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.header("🛡️ Clip Authenticity Detector")
    st.write("Verify video authenticity using biological signals")
    
    video_path = st.text_input("Video Path", "D:\\guardian-stream\\videos\\novak_interview_real.mp4")
    context = st.text_area("Context", "Novak Djokovic post match interview")
    video_type = st.radio("Video Type", ["interview", "sports"])
    
    if st.button("🚀 Run Analysis", type="primary"):
        with st.spinner("Analyzing video..."):
            try:
                cmd = [
                    "python", "src/gemini_intelligence.py",
                    "--video-path", video_path,
                    "--context", context,
                    "--real-mode"
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd="D:\\guardian-stream"
                )
                
                st.success("✅ Analysis Complete!")
                st.code(result.stdout)
                
                # Show report
                report_path = Path("D:\\guardian-stream\\gemini_intelligence_report.json")
                if report_path.exists():
                    with open(report_path) as f:
                        report = json.load(f)
                    st.json(report)
                    
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.markdown("**Built for Hackathon 2026**")