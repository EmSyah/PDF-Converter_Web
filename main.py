import streamlit as st
from pdf2docx import Converter
from docx2pdf import convert
import os

st.set_page_config(page_title="Universal Converter", page_icon="🔄")

st.title("🔄 Universal File Converter")

# Sidebar for navigation
mode = st.sidebar.selectbox("Select Conversion Mode", ["PDF to Word", "Word to PDF"])

if mode == "PDF to Word":
    st.header("📄 PDF to Word")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file and st.button("Convert PDF"):
        with st.spinner("Converting..."):
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            cv = Converter("temp.pdf")
            cv.convert("output.docx")
            cv.close()
            with open("output.docx", "rb") as f:
                st.download_button("Download Word File", f, file_name="converted.docx")

else:
    st.header("📝 Word to PDF")
    uploaded_file = st.file_uploader("Upload Word Document", type="docx")
    
    if uploaded_file and st.button("Convert Word"):
        with st.spinner("Converting..."):
            with open("temp.docx", "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Note: Word to PDF requires Microsoft Word installed on the server
            # Free web servers often struggle with this part!
            convert("temp.docx", "output.pdf")
            with open("output.pdf", "rb") as f:
                st.download_button("Download PDF File", f, file_name="converted.pdf")