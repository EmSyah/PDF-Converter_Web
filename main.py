import streamlit as st
from pdf2docx import Converter
import os
import re

st.set_page_config(page_title="Universal Converter", page_icon="🔄")

st.title("🔄 Universal File Converter")

# Mode selector
mode = st.sidebar.selectbox("Select Conversion Mode", ["PDF to Word", "Word to PDF"])

if mode == "PDF to Word":
    st.header("📄 PDF to Word")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file is not None:
        # 1. Get original name and prepare the Word name
        original_name = uploaded_file.name
        # This replaces .pdf (case insensitive) with .docx at the end of the string
        new_filename = re.sub(r'\.pdf$', '.docx', original_name, flags=re.IGNORECASE)
        
        # 2. Use a safe internal name to avoid server errors with special characters
        # We use 'temp_file.pdf' internally so characters like % or { don't break the OS path
        temp_pdf = "temp_input.pdf"
        temp_docx = "temp_output.docx"

        if st.button("Convert PDF"):
            with st.spinner("Processing..."):
                try:
                    # Write uploaded bytes to a local temp file
                    with open(temp_pdf, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Convert
                    cv = Converter(temp_pdf)
                    cv.convert(temp_docx)
                    cv.close()
                    
                    st.success(f"Successfully converted: {original_name}")

                    # 3. Download button with the DYNAMIC original filename
                    with open(temp_docx, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Word Document",
                            data=f,
                            file_name=new_filename, # This uses the original name!
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    # Cleanup
                    if os.path.exists(temp_pdf): os.remove(temp_pdf)