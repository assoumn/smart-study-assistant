import streamlit as st

from preprocessing.clean_text import clean_text

st.title("Smart Study Assistant")

text = st.text_area("Enter your lecture text")

if st.button("Analyze"):

    cleaned = clean_text(text)

    st.subheader("Cleaned Text")

    st.write(cleaned)