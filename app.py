import streamlit as st
from PyPDF2 import PdfMerger, PdfReader
from docx import Document
from PIL import Image
import io

# ---- Tool Functions ----
def pdf_to_word(pdf_file):
    doc = Document()
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            doc.add_paragraph(text)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def word_to_pdf(doc_file):
    st.warning("⚠️ Word to PDF conversion isn't supported in Streamlit without LibreOffice or external tools.")
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
    st.warning("⚠️ PDF compression requires advanced tools like ghostscript or PyMuPDF. Coming soon!")
    return None

# ---- Streamlit UI ----
st.set_page_config(page_title="PDF Tools Hub", layout="centered")
st.title("🛠️ PDF Tools Website (MVP)")
st.markdown("✅ App is running")

tool = st.sidebar.selectbox("📌 Choose a Tool", [
    "PDF to Word", "Word to PDF", "Merge PDFs", "JPG to PDF", "Compress PDF"
])

if tool == "PDF to Word":
    uploaded = st.file_uploader("📄 Upload PDF", type="pdf")
    if uploaded:
        try:
            docx_file = pdf_to_word(uploaded)
            st.success("✅ Conversion successful!")
            st.download_button("⬇️ Download Word File", docx_file, file_name="converted.docx")
        except Exception as e:
            st.error(f"Error converting PDF to Word: {e}")

elif tool == "Word to PDF":
    uploaded = st.file_uploader("📄 Upload Word File (.docx)", type="docx")
    if uploaded:
        word_to_pdf(uploaded)

elif tool == "Merge PDFs":
    uploaded_files = st.file_uploader("📄 Upload PDFs to Merge", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        try:
            merged_pdf = merge_pdfs(uploaded_files)
            st.success("✅ Merge successful!")
            st.download_button("⬇️ Download Merged PDF", merged_pdf, file_name="merged.pdf")
        except Exception as e:
            st.error(f"Error merging PDFs: {e}")

elif tool == "JPG to PDF":
    images = st.file_uploader("🖼️ Upload JPG/PNG Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if images:
        try:
            pdf_output = jpg_to_pdf(images)
            st.success("✅ Conversion successful!")
            st.download_button("⬇️ Download PDF", pdf_output, file_name="images.pdf")
        except Exception as e:
            st.error(f"Error converting images: {e}")

elif tool == "Compress PDF":
    uploaded = st.file_uploader("📄 Upload PDF to Compress", type="pdf")
    if uploaded:
        compress_pdf(uploaded)
