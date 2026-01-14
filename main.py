import streamlit as st
from pdf2docx import Converter
import pypdf
import os
import re
import io
import zipfile
import fitz  # PyMuPDF
try:
    from docx2pdf import convert
except ImportError:
    pass

st.set_page_config(page_title="Universal PDF Tool", page_icon="🔄", layout="wide")

st.title("🔄 Universal PDF Tool")

mode = st.sidebar.selectbox("Select Feature", [
    "PDF to Word", 
    "Word to PDF",
    "Edit PDF (Search & Replace)",
    "Merge PDFs", 
    "Split PDF"
])

# --- FEATURE 1: PDF TO WORD (Vice Versa Part A) ---
if mode == "PDF to Word":
    st.header("📄 PDF to Word Converter")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file:
        if st.button("Convert to Word"):
            with st.spinner("Converting PDF to DOCX..."):
                temp_pdf = "temp_in.pdf"
                temp_docx = "temp_out.docx"
                with open(temp_pdf, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                cv = Converter(temp_pdf)
                cv.convert(temp_docx)
                cv.close()
                
                with open(temp_docx, "rb") as f:
                    st.download_button("Download Word File", f, file_name="converted.docx")
                os.remove(temp_pdf)
                os.remove(temp_docx)

# --- FEATURE 2: WORD TO PDF (Vice Versa Part B) ---
elif mode == "Word to PDF":
    st.header("📄 Word to PDF Converter")
    uploaded_file = st.file_uploader("Upload Word Doc", type=["docx", "doc"])
    if uploaded_file:
        if st.button("Convert to PDF"):
            try:
                with st.spinner("Converting DOCX to PDF..."):
                    with open("temp.docx", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # This command looks for Microsoft Word on the system
                    convert("temp.docx", "temp.pdf")
                    
                    with open("temp.pdf", "rb") as f:
                        st.download_button("Download PDF", f, file_name="converted_from_word.pdf")
            except Exception as e:
                st.error("⚠️ Local Word Instance Not Found.")
                st.info("The 'Word to PDF' feature requires Microsoft Word to be installed on the system (Windows/Mac). It may not work on the hosted Streamlit Cloud (Linux).")
            finally:
                if os.path.exists("temp.docx"): os.remove("temp.docx")
                if os.path.exists("temp.pdf"): os.remove("temp.pdf")

# --- OTHER FEATURES (Edit, Merge, Split) ---
elif mode == "Edit PDF (Search & Replace)":
    st.header("✍️ Edit PDF Content")
    file = st.file_uploader("Upload PDF", type="pdf")
    search_text = st.text_input("Text to redact/edit:")
    if file and search_text:
        if st.button("Apply Edit"):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            for page in doc:
                for rect in page.search_for(search_text):
                    page.add_redact_annotation(rect, fill=(0, 0, 0))
                page.apply_redactions()
            out = io.BytesIO()
            doc.save(out)
            st.download_button("Download Edited PDF", out.getvalue(), "edited.pdf")

elif mode == "Merge PDFs":
    st.header("🔗 Merge PDFs")
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if files and st.button("Merge"):
        merger = pypdf.PdfWriter()
        for pdf in files: merger.append(pdf)
        out = io.BytesIO(); merger.write(out)
        st.download_button("Download Merged", out.getvalue(), "merged.pdf")

elif mode == "Split PDF":
    st.header("✂️ Split PDF")
    file = st.file_uploader("Upload PDF", type="pdf")
    if file and st.button("Split"):
        reader = pypdf.PdfReader(file)
        z_buf = io.BytesIO()
        with zipfile.ZipFile(z_buf, "w") as zf:
            for i in range(len(reader.pages)):
                w = pypdf.PdfWriter(); w.add_page(reader.pages[i])
                p_io = io.BytesIO(); w.write(p_io)
                zf.writestr(f"page_{i+1}.pdf", p_io.getvalue())
        st.download_button("Download ZIP", z_buf.getvalue(), "split.zip")