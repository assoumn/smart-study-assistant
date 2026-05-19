import streamlit as st

from preprocessing.clean_text import clean_text

# future imports
# from keywords.extract_keywords import extract_keywords
# from summarization.summarize import summarize_text

st.set_page_config(
    page_title="Smart Study Assistant",
    layout="centered"
)

st.title("Smart Study Assistant")

st.write("Analyze lecture text using NLP techniques.")

text = st.text_area(
    "Enter your lecture text",
    height=250
)

if st.button("Analyze"):
    

    if text.strip() == "":
        st.warning("Please enter some text.")
    
    else:

        cleaned_text = clean_text(text)

        st.subheader("Cleaned Text")

        st.write(cleaned_text)
        
        # Placeholder for keywords
        st.subheader("Keywords")

        st.write("Waiting for keyword module...")

        # Placeholder for summary
        st.subheader("Summary")

        st.write("Waiting for summarization module...")