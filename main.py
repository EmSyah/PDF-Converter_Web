import streamlit as st
from pdf2docx import Converter
import os

st.set_page_config(page_title="PDF Converter", page_icon="📄")

st.title("📄 PDF to Word Converter")
st.info("Upload a PDF file below to convert it into an editable Word document.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file temporarily so the library can read it
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Target file: {uploaded_file.name}")

    if st.button("Start Conversion"):
        with st.spinner("Processing... Please wait."):
            try:
                # Perform the conversion
                cv = Converter("temp.pdf")
                cv.convert("converted_result.docx")
                cv.close()
                
                st.balloons() # Fun celebration!
                st.success("Conversion Complete!")

                # Provide the download button
                with open("converted_result.docx", "rb") as file:
                    st.download_button(
                        label="Click here to Download Word File",
                        data=file,
                        file_name=f"{uploaded_file.name.split('.')[0]}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")