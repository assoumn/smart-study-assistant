from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np

# Download tokenizer
nltk.download('punkt')


def summarize_text(text, num_sentences=3):

    # -----------------------------
    # SENTENCE TOKENIZATION
    # -----------------------------
    
    sentences = sent_tokenize(text)

    # Handle very short text
    if len(sentences) <= num_sentences:

        return {

            "summary": text,

            "ranked_sentences": [
                (1.0, sentence)
                for sentence in sentences
            ],

            "study_notes": sentences
        }

    # -----------------------------
    # TF-IDF VECTORIZATION
    # -----------------------------

    vectorizer = TfidfVectorizer(
        stop_words='english'
    )

    tfidf_matrix = vectorizer.fit_transform(sentences)

    # -----------------------------
    # SENTENCE SCORING
    # -----------------------------

    sentence_scores = np.array(
        tfidf_matrix.sum(axis=1)
    ).flatten()

    # -----------------------------
    # SENTENCE RANKING
    # -----------------------------

    ranked_data = sorted(
        zip(sentence_scores, sentences),
        reverse=True
    )

    # -----------------------------
    # EXTRACTIVE SUMMARY
    # -----------------------------

    selected_sentences = [

        sentence

        for score, sentence
        in ranked_data[:num_sentences]
    ]

    # Preserve original order
    final_summary = [

        sentence

        for sentence in sentences
        if sentence in selected_sentences
    ]

    # -----------------------------
    # STUDY NOTES GENERATION
    # -----------------------------

    study_notes = []

    for score, sentence in ranked_data:

        # Keep informative sentences
        if len(sentence.split()) > 8:

            study_notes.append(sentence)

    # -----------------------------
    # RETURN RESULTS
    # -----------------------------

    return {

        # Final summary
        "summary": " ".join(final_summary),

        # Ranked sentences + scores
        "ranked_sentences": ranked_data,

        # Generated study notes
        "study_notes": study_notes
    }