import re
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def clean_text(text):

    # lowercase
    text = text.lower()

    # remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # tokenize
    tokens = word_tokenize(text)

    # remove stopwords
    filtered_tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    return " ".join(filtered_tokens)


sample = "Machine Learning is very powerful and useful!"

print(clean_text(sample))