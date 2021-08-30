# Clean reviews text

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import unicodedata


def clean(text):

    for punctuation in string.punctuation:
        text = text.replace(punctuation, ' ')  # Remove Punctuation

    lowercased = text.lower()  # Lower Case

    unaccented_string = unicodedata.unidecode(lowercased)  # remove accents

    tokenized = word_tokenize(unaccented_string)  # Tokenize

    words_only = [word for word in tokenized
                  if word.isalpha()]  # Remove numbers

    stop_words = set(stopwords.words('portuguese'))  # Make stopword list

    without_stopwords = [
        word for word in words_only if not word in stop_words
    ]  # Remove Stop Words

    return " ".join(without_stopwords)
