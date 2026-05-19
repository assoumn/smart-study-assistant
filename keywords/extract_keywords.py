import spacy
from collections import Counter


nlp = spacy.load("en_core_web_sm")


def extract_keywords(text, num_keywords=5):
    """
    Extract important study concepts using spaCy noun chunks.

    Returns:
        list: List of tuples (keyword, score)
    """

    if not text or not text.strip():
        return []

    doc = nlp(text)

    concepts = []

    for chunk in doc.noun_chunks:
        phrase = chunk.text.lower().strip()

        if len(phrase) <= 2:
            continue

        if all(token.is_stop for token in chunk):
            continue

        concepts.append(phrase)

    if not concepts:
        return []

    concept_counts = Counter(concepts)

    total = sum(concept_counts.values())

    keywords = []

    for concept, count in concept_counts.most_common(num_keywords):
        score = count / total
        keywords.append((concept, float(round(score, 2))))

    return keywords


if __name__ == "__main__":

    sample_text = """
    Machine learning improves education systems.
    Artificial intelligence helps students learn faster.
    Natural language processing is widely used in AI systems.
    Deep learning improves medical diagnosis.
    """

    result = extract_keywords(sample_text, 5)

    print("Top Study Concepts with Scores:")
    print(result)