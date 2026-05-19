from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(text1, text2):
    """
    Calculate how similar two texts are using TF-IDF and cosine similarity.

    Parameters:
        text1 (str): First input text
        text2 (str): Second input text

    Returns:
        float: Similarity score between 0 and 1
    """

    # If one of the texts is empty, there is no similarity
    if not text1 or not text2:
        return 0.0

    # If one of the texts contains only spaces, return 0
    if not text1.strip() or not text2.strip():
        return 0.0

    # Convert the two texts into numerical TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words="english")

    # Fit and transform both texts at the same time
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Compare the first text vector with the second text vector
    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    # Round the score to 2 decimal places for cleaner output
    return round(similarity_score, 2)


# This part is only for testing this file directly
if __name__ == "__main__":

    text1 = "Machine learning is a branch of artificial intelligence."
    text2 = "Artificial intelligence includes machine learning techniques."

    result = calculate_similarity(text1, text2)

    print("Similarity Score:")
    print(result)