import streamlit as st
from pdf2docx import Converter
import pypdf
import os
import re
import io
import zipfile

# --- PAGE CONFIG ---
st.set_page_config(page_title="Universal PDF Tool", page_icon="🔄", layout="wide")

st.title("🔄 Universal PDF Tool")

# --- SIDEBAR NAVIGATION ---
mode = st.sidebar.selectbox("Select Feature", [
    "PDF to Word", 
    "Merge PDFs", 
    "Split PDF", 
    "Edit (Rotate)"
])

# --- 1. PDF TO WORD (Your Original Logic) ---
if mode == "PDF to Word":
    st.header("📄 PDF to Word Converter")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file is not None:
        original_name = uploaded_file.name
        new_filename = re.sub(r'\.pdf$', '.docx', original_name, flags=re.IGNORECASE)
        
        temp_pdf = "temp_input.pdf"
        temp_docx = "temp_output.docx"

        if st.button("Convert to Word"):
            with st.spinner("Processing conversion..."):
                try:
                    with open(temp_pdf, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    cv = Converter(temp_pdf)
                    cv.convert(temp_docx)
                    cv.close()
                    
                    st.success(f"Converted: {original_name}")
                    with open(temp_docx, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Word Document",
                            data=f,
                            file_name=new_filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    if os.path.exists(temp_pdf): os.remove(temp_pdf)
                    if os.path.exists(temp_docx): os.remove(temp_docx)

# --- 2. MERGE PDFS ---
elif mode == "Merge PDFs":
    st.header("🔗 Merge Multiple PDFs")
    files = st.file_uploader("Upload 2 or more PDFs", type="pdf", accept_multiple_files=True)
    
    if files:
        if st.button("Merge Files"):
            merger = pypdf.PdfWriter()
            for pdf in files:
                merger.append(pdf)
            
            output = io.BytesIO()
            merger.write(output)
            st.success("PDFs Merged Successfully!")
            st.download_button("⬇️ Download Merged PDF", output.getvalue(), "merged.pdf", "application/pdf")

# --- 3. SPLIT PDF ---
elif mode == "Split PDF":
    st.header("✂️ Split PDF into Individual Pages")
    file = st.file_uploader("Upload a PDF", type="pdf")
    
    if file:
        if st.button("Split Pages"):
            reader = pypdf.PdfReader(file)
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for i in range(len(reader.pages)):
                    writer = pypdf.PdfWriter()
                    writer.add_page(reader.pages[i])
                    page_io = io.BytesIO()
                    writer.write(page_io)
                    zf.writestr(f"page_{i+1}.pdf", page_io.getvalue())
            
            st.success("Split complete!")
            st.download_button("⬇️ Download All Pages (ZIP)", zip_buffer.getvalue(), "split_pages.zip", "application/zip")

# --- 4. EDIT (ROTATE) ---
elif mode == "Edit (Rotate)":
    st.header("🔄 Rotate PDF Pages")
    file = st.file_uploader("Upload PDF", type="pdf")
    
    if file:
        angle = st.slider("Select Rotation Angle", 0, 270, 90, 90)
        if st.button("Apply Rotation"):
            reader = pypdf.PdfReader(file)
            writer = pypdf.PdfWriter()
            
            for page in reader.pages:
                page.rotate(angle)
                writer.add_page(page)
            
            output = io.BytesIO()
            writer.write(output)
            st.download_button("⬇️ Download Rotated PDF", output.getvalue(), "rotated.pdf", "application/pdf")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit & pypdf")