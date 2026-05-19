from sklearn.feature_extraction.text import TfidfVectorizer


def extract_keywords(text, num_keywords=5):
    """
    Extract important keywords from text using TF-IDF.

    Parameters:
        text (str): Input text
        num_keywords (int): Number of keywords to return

    Returns:
        list: Top keywords
    """

    # Check if text is empty
    if not text or not text.strip():
        return []

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1000,
        ngram_range=(1, 1)
    )

    # Transform text into TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform([text])

    # Get words
    feature_names = vectorizer.get_feature_names_out()

    # Get scores
    scores = tfidf_matrix.toarray()[0]

    # Combine words with scores
    word_scores = list(zip(feature_names, scores))

    # Sort by highest score
    sorted_words = sorted(
        word_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Store keywords
    keywords = []

    for word, score in sorted_words:

        # Skip very short words
        if len(word) <= 2:
            continue

        keywords.append(word)

        # Stop when enough keywords collected
        if len(keywords) == num_keywords:
            break

    return keywords


# Test directly
if __name__ == "__main__":

    sample_text = """
    Artificial intelligence helps computers learn from data.
    Machine learning is a branch of artificial intelligence.
    Artificial intelligence is used in healthcare, education, and robotics.
    Machine learning systems can improve study tools and smart assistants.
    """

    result = extract_keywords(sample_text, 5)

    print("Top Keywords:")
    print(result)