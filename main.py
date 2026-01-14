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
# I have ensured "Edit" is completely removed from this list
mode = st.sidebar.selectbox("Select Feature", [
    "PDF to Word", 
    "Word to PDF",
    "Merge PDFs", 
    "Split PDF"
])

# --- 1. PDF TO WORD (Works on Web & Local) ---
if mode == "PDF to Word":
    st.header("📄 PDF to Word Converter")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file:
        original_name = uploaded_file.name
        new_filename = re.sub(r'\.pdf$', '.docx', original_name, flags=re.IGNORECASE)
        
        if st.button("Convert to Word"):
            with st.spinner("Processing..."):
                try:
                    pdf_bytes = uploaded_file.read()
                    
                    # Temporarily save for the converter
                    with open("temp.pdf", "wb") as f:
                        f.write(pdf_bytes)
                    
                    cv = Converter("temp.pdf")
                    cv.convert("temp.docx")
                    cv.close()
                    
                    with open("temp.docx", "rb") as f:
                        st.download_button("⬇️ Download Word", f, file_name=new_filename)
                    
                    os.remove("temp.pdf")
                    os.remove("temp.docx")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- 2. WORD TO PDF (Conditional Logic) ---
elif mode == "Word to PDF":
    st.header("📄 Word to PDF Converter")
    st.warning("⚠️ This feature requires Microsoft Word (Windows/Mac) and may not work on the live web link.")
    uploaded_file = st.file_uploader("Upload Word Doc", type=["docx", "doc"])
    
    if uploaded_file:
        original_name = uploaded_file.name
        new_filename = re.sub(r'\.docx$|\.doc$', '.pdf', original_name, flags=re.IGNORECASE)
        
        if st.button("Convert to PDF"):
            try:
                from docx2pdf import convert
                with open("t_in.docx", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                convert("t_in.docx", "t_out.pdf")
                
                with open("t_out.pdf", "rb") as f:
                    st.download_button("⬇️ Download PDF", f, file_name=new_filename)
                
                os.remove("t_in.docx")
                os.remove("t_out.pdf")
            except Exception:
                st.error("This server environment (Linux) does not support Word-to-PDF conversion. Please run this tool locally on Windows/Mac.")

# --- 3. MERGE PDFs ---
elif mode == "Merge PDFs":
    st.header("🔗 Merge PDFs")
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if files and st.button("Merge"):
        merger = pypdf.PdfWriter()
        for pdf in files:
            merger.append(pdf)
        out = io.BytesIO()
        merger.write(out)
        st.download_button("Download Merged PDF", out.getvalue(), "merged.pdf")

# --- 4. SPLIT PDF ---
elif mode == "Split PDF":
    st.header("✂️ Split PDF")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file and st.button("Split"):
        reader = pypdf.PdfReader(file)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            for i in range(len(reader.pages)):
                writer = pypdf.PdfWriter()
                writer.add_page(reader.pages[i])
                p_io = io.BytesIO()
                writer.write(p_io)
                zf.writestr(f"page_{i+1}.pdf", p_io.getvalue())
        st.download_button("Download ZIP", zip_buffer.getvalue(), "split.zip")