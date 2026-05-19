import streamlit as st
from PIL import Image

from preprocessing.clean_text import clean_text
from keywords.extract_keywords import extract_keywords

# future imports
# from summarization.summarize import summarize_text

# Load image
image = Image.open("assets/roboto.png")

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
# INPUT
# -----------------------------

text = st.text_area(
    "Enter your lecture text",
    height=250
)

# -----------------------------
# BUTTON
# -----------------------------

if st.button("Analyze", use_container_width=True):

    if text.strip() == "":
        st.warning("Please enter some text.")

    else:

        # Clean text
        cleaned_text = clean_text(text)

        # Extract keywords
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