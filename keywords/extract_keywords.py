from sklearn.feature_extraction.text import TfidfVectorizer


def extract_keywords(text, num_keywords=5):
    """
    Extract important keywords and phrases using TF-IDF.
    """

    # Return empty list if text is empty
    if not text or not text.strip():
        return []

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1000,
        ngram_range=(1, 2)
    )

    # Transform text into TF-IDF matrix contain scores
    tfidf_matrix = vectorizer.fit_transform([text])

    # Get words and phrases
    feature_names = vectorizer.get_feature_names_out()

    # Get scores
    scores = tfidf_matrix.toarray()[0]

    # Combine words/phrases with scores
    word_scores = list(zip(feature_names, scores))

    # Sort descending by score
    sorted_words = sorted(
        word_scores,
        key=lambda x: (
            len(x[0].split()),  # prefer phrases
            x[1]                # then higher score
        ),
        reverse=True
    )

    keywords = []

    for word, score in sorted_words:

        parts = word.split()

        # Skip repeated words
        if len(parts) == 2 and parts[0] == parts[1]:
            continue

        # Skip phrases with tiny words
        if any(len(part) <= 2 for part in parts):
            continue

        # Skip meaningless combinations
        weak_words = {
            "used", "using", "help", "helps",
            "make", "makes", "good", "new"
        }

        if any(part in weak_words for part in parts):
            continue

        # Avoid duplicates
        already_exists = False

        for existing in keywords:

            if word in existing or existing in word:
                already_exists = True
                break

        if already_exists:
            continue

        keywords.append(word)

        # Stop when enough keywords found
        if len(keywords) == num_keywords:
            break

    return keywords


if __name__ == "__main__":

    sample_text = """
    Machine learning improves education systems.
    Artificial intelligence helps students learn faster.
    Natural language processing is widely used in AI systems.
    Deep learning improves medical diagnosis.
    """

    result = extract_keywords(sample_text, 5)

    print("Top Keywords:")
    print(result)