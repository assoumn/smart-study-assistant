import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

nltk.download('punkt')

def summarize_text(text, num_sentences=3):

    # 1. Split into sentences
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    # 2. TF-IDF vectorization on sentences
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # 3. Score each sentence (sum of TF-IDF weights)
    sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()

    # 4. Rank sentences
    ranked_sentences = [
        sentence for _, sentence in sorted(
            zip(sentence_scores, sentences),
            reverse=True
        )
    ]

    # 5. Pick top sentences
    selected = ranked_sentences[:num_sentences]

    # 6. Restore original order (IMPORTANT for readability)
    final_summary = [
        s for s in sentences if s in selected
    ]

    return " ".join(final_summary)