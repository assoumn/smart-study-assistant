import streamlit as st
from PIL import Image
import PyPDF2

# NLP functions
from preprocessing.clean_text import clean_text
from keywords.extract_keywords import extract_keywords
from summarization.summarize import summarize_text
from quiz.generate_quiz import generate_quiz
from similarity.similarity import calculate_similarity


# App image
image = Image.open("assets/roboto.png")

# Streamlit page settings
st.set_page_config(
    page_title="Smart Study Assistant",
    layout="centered"
)

# Save app state
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# Custom UI styling
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

# Center image
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(image, width=350)

# App title
st.title("Smart Study Assistant")

st.caption("Analyze lecture text using NLP techniques.")

# Upload lecture PDF
uploaded_file = st.file_uploader(
    "Upload Lecture PDF",
    type=["pdf"]
)

# Manual text input
text = st.text_area(
    "Or enter your lecture text manually",
    height=250
)

# Control summary size
summary_length = st.slider(
    "Select Summary Length",
    min_value=1,
    max_value=10,
    value=3
)

# Extract text from PDF
pdf_text = ""

if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            pdf_text += extracted

# Start NLP analysis
if st.button("Analyze", use_container_width=True):

    final_text = text

    # Use PDF text if uploaded
    if pdf_text:
        final_text = pdf_text

    # Check empty input
    if final_text.strip() == "":
        st.warning("Please enter text or upload a PDF.")

    else:

        # Loading animation
        with st.spinner("Analyzing lecture..."):

            # Clean text
            st.session_state.cleaned_text = clean_text(
                final_text
            )

            # Extract keywords
            st.session_state.keywords = extract_keywords(
                st.session_state.cleaned_text
            )

            # Generate summary
            st.session_state.summary = summarize_text(
                final_text,
                summary_length
            )

            # Generate quiz
            st.session_state.quiz_questions = generate_quiz(
                st.session_state.summary["summary"]
            )

            st.session_state.analysis_done = True


# Show results
if st.session_state.analysis_done:

    # Display cleaned text
    st.divider()
    st.subheader("Cleaned Text")
    st.write(st.session_state.cleaned_text)

    # Display keywords
    st.divider()
    st.subheader("Keywords")

    for keyword, score in st.session_state.keywords:
        st.markdown(f"- {keyword}")

    # Display summary
    st.divider()
    st.subheader("Extractive Summary")

    st.success(
        st.session_state.summary["summary"]
    )

    # Show sentence ranking
    st.divider()
    st.subheader("Sentence Importance Analysis")

    ranked_sentences = st.session_state.summary[
        "ranked_sentences"
    ]

    for index, (score, sentence) in enumerate(
        ranked_sentences,
        start=1
    ):

        st.markdown(
            f"### Sentence Rank #{index}"
        )

        st.write(sentence)

        st.caption(
            f"Importance Score: {score:.2f}"
        )

        st.divider()

    # Show study notes
    st.subheader("Generated Study Notes")

    study_notes = st.session_state.summary[
        "study_notes"
    ]

    for note in study_notes:
        st.markdown(f"• {note}")

    # Quiz section
    st.divider()
    st.subheader("Quiz")

    for index, item in enumerate(
        st.session_state.quiz_questions
    ):

        st.markdown(
            f"### Question {index + 1}"
        )

        st.write(item["question"])

        st.radio(
            "Choose your answer:",
            ["True", "False"],
            key=f"quiz_answer_{index}"
        )

    # Submit quiz answers
    if st.button("Submit Quiz"):

        score = 0

        st.divider()
        st.subheader("Quiz Results")

        for index, item in enumerate(
            st.session_state.quiz_questions
        ):

            user_answer = st.session_state[
                f"quiz_answer_{index}"
            ]

            correct_answer = item["answer"]

            st.markdown(
                f"### Question {index + 1}"
            )

            st.write(item["question"])

            st.write(
                f"Your Answer: {user_answer}"
            )

            st.write(
                f"Correct Answer: {correct_answer}"
            )

            # Check answer correctness
            if user_answer == correct_answer:

                st.success("Correct")
                score += 1

            else:
                st.error("Wrong")

        st.divider()

        st.success(
            f"Final Score: {score} / {len(st.session_state.quiz_questions)}"
        )

    # Student answer similarity
    st.divider()
    st.subheader("Check Your Understanding")

    student_answer = st.text_area(
        "Write a short answer about the lecture:",
        height=120
    )

    # Compare answer with lecture summary
    if st.button("Check Answer Similarity"):

        if student_answer.strip() == "":
            st.warning("Please write an answer first.")

        else:

            similarity_score = calculate_similarity(
                student_answer,
                st.session_state.summary["summary"]
            )

            st.write(
                f"Similarity with lecture summary: {similarity_score}"
            )

            # Give feedback
            if similarity_score >= 0.5:

                st.success(
                    "Your answer is relevant to the lecture."
                )

            else:

                st.warning(
                    "Your answer may need more lecture-related concepts."
                )