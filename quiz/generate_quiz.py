from nltk.tokenize import sent_tokenize
import random


def generate_quiz(text, num_questions=3):

    sentences = sent_tokenize(text)

    quiz = []

    selected_sentences = sentences[:num_questions]

    for sentence in selected_sentences:

        sentence = sentence.strip()

        if len(sentence) < 20:
            continue

        # Randomly choose True or False
        is_true = random.choice([True, False])

        # TRUE question
        if is_true:

            question = sentence

            answer = "True"

        # FALSE question
        else:

            # Simple rule-based modification
            if " is " in sentence:

                question = sentence.replace(" is ", " is not ", 1)

            elif " are " in sentence:

                question = sentence.replace(" are ", " are not ", 1)

            else:

                question = "Not true: " + sentence

            answer = "False"

        quiz.append({
            "question": f"True or False: {question}",
            "answer": answer
        })

    return quiz


# -----------------------------
# TEST FILE DIRECTLY
# -----------------------------

if __name__ == "__main__":

    sample = """
    Artificial intelligence helps computers perform tasks.
    Machine learning is a branch of AI.
    NLP enables computers to understand human language.
    Deep learning uses neural networks.
    """

    quiz = generate_quiz(sample)

    for q in quiz:

        print(q["question"])
        print("Correct Answer:", q["answer"])
        print()