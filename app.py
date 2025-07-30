import streamlit as st
from PyPDF2 import PdfMerger
from docx import Document
from PIL import Image
import pdfplumber
import io

# ---- Tool Functions ----
def pdf_to_word(pdf_file):
    doc = Document()
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def word_to_pdf(doc_file):
    st.warning("⚠️ Word to PDF conversion isn't directly supported in this demo.")
    return None

def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    buffer = io.BytesIO()
    merger.write(buffer)
    merger.close()
    buffer.seek(0)
    return buffer

def jpg_to_pdf(image_files):
    images = [Image.open(img).convert('RGB') for img in image_files]
    buffer = io.BytesIO()
    images[0].save(buffer, save_all=True, append_images=images[1:], format="PDF")
    buffer.seek(0)
    return buffer

def compress_pdf(pdf_file):
    st.warning("⚠️ PDF compression requires external tools like PyMuPDF or ghostscript.")
    return None

# ---- Streamlit UI ----
st.set_page_config(page_title="PDF Tools Hub", layout="centered")
st.title("🛠️ PDF Tools Website (MVP)")

tool = st.sidebar.selectbox("📌 Choose a Tool", [
    "PDF to Word", "Word to PDF", "Merge PDFs", "JPG to PDF", "Compress PDF"
])

if tool == "PDF to Word":
    uploaded = st.file_uploader("📄 Upload PDF", type="pdf")
    if uploaded:
        docx_file = pdf_to_word(uploaded)
        st.success("✅ Conversion successful!")
        st.download_button("⬇️ Download Word File", docx_file, file_name="converted.docx")

elif tool == "Word to PDF":
    uploaded = st.file_uploader("📄 Upload Word File (.docx)", type="docx")
    if uploaded:
        word_to_pdf(uploaded)

elif tool == "Merge PDFs":
    uploaded_files = st.file_uploader("📄 Upload PDFs to Merge", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        merged_pdf = merge_pdfs(uploaded_files)
        st.success("✅ Merge successful!")
        st.download_button("⬇️ Download Merged PDF", merged_pdf, file_name="merged.pdf")

elif tool == "JPG to PDF":
    images = st.file_uploader("🖼️ Upload JPG/PNG Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if images:
        pdf_output = jpg_to_pdf(images)
        st.success("✅ Conversion successful!")
        st.download_button("⬇️ Download PDF", pdf_output, file_name="images.pdf")

elif tool == "Compress PDF":
    uploaded = st.file_uploader("📄 Upload PDF to Compress", type="pdf")
    if uploaded:
        compress_pdf(uploaded)
