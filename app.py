import streamlit as st
from PIL import Image
import PyPDF2

from preprocessing.clean_text import clean_text
from keywords.extract_keywords import extract_keywords

# future imports
# from summarization.summarize import summarize_text

# -----------------------------
# LOAD IMAGE
# -----------------------------

image = Image.open("assets/roboto.png")

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Smart Study Assistant",
    layout="centered"
)

# -----------------------------
# CUSTOM STYLING
# -----------------------------

st.markdown(
    """
    <style>

    .main {
        text-align: center;
    }

    div[data-testid="stTextArea"] textarea {
        text-align: left;
        border-radius: 12px;
    }

    div.stButton > button {
        background-color: #7ED957;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-size: 16px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #6CC84A;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# IMAGE
# -----------------------------

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(image, width=350)

# -----------------------------
# TITLE
# -----------------------------

st.title("Smart Study Assistant")

st.caption("Analyze lecture text using NLP techniques.")

# -----------------------------
# PDF UPLOAD
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload Lecture PDF",
    type=["pdf"]
)

# -----------------------------
# TEXT INPUT
# -----------------------------

text = st.text_area(
    "Or enter your lecture text manually",
    height=250
)

# -----------------------------
# EXTRACT PDF TEXT
# -----------------------------

pdf_text = ""

if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            pdf_text += extracted

# -----------------------------
# BUTTON
# -----------------------------

if st.button("Analyze", use_container_width=True):

    # -----------------------------
    # CHOOSE INPUT SOURCE
    # -----------------------------

    final_text = text

    if pdf_text:
        final_text = pdf_text

    # -----------------------------
    # EMPTY INPUT CHECK
    # -----------------------------

    if final_text.strip() == "":
        st.warning("Please enter text or upload a PDF.")

    else:

        # -----------------------------
        # PREPROCESSING
        # -----------------------------

        cleaned_text = clean_text(final_text)

        # -----------------------------
        # KEYWORD EXTRACTION
        # -----------------------------

        keywords = extract_keywords(cleaned_text)

        # -----------------------------
        # CLEANED TEXT
        # -----------------------------

        st.divider()

        st.subheader("Cleaned Text")

        st.write(cleaned_text)

        # -----------------------------
        # KEYWORDS
        # -----------------------------

        st.divider()

        st.subheader("Keywords")

        st.write(keywords)

        # -----------------------------
        # SUMMARY PLACEHOLDER
        # -----------------------------

        st.divider()

        st.subheader("Summary")

        st.write("Waiting for summarization module...")