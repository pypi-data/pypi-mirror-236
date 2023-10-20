import re
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import string
from typing import List
from collections import Counter
from nltk.util import ngrams

def basic_text_processing(raw_str: str) -> str:
    """

    A function that could preprocess your str. It could:
        1. Lowercase all words
        2. Remove URLs
        3. Tokenize the string into individual words
        4. Remove punctuations
        5. Remove stopwords    
    
    This function will return a string after done all of these works.

    """

    # Lowercase all words
    content = raw_str.lower()

    # Remove URLs from the content using regular expressions
    content_without_urls = re.sub(r"http\S+", "", content)
    contents = re.sub(r"www\S+", "", content_without_urls)

    # Tokenize the string into individual words
    words = nltk.word_tokenize(contents)

    # Remove stopwords and punctuation from the list of words
    stop_words = set(stopwords.words('english'))

    punctuations = set(string.punctuation)
    filtered_words = []
    for word in words:
        if word not in stop_words:
            filtered_word = ''.join(ch for ch in word if ch not in punctuations)
            if filtered_word:
                filtered_words.append(filtered_word)

    final_str = " ".join(filtered_words)

    return final_str


def nlp_text_processing(raw_str: str) -> List[str]:
    """

    This function will process your raw str to stemmed and lemmatized words list.
    It will return a list which contains all words after stemmed and lemmatized.
    The stemming method is Snowball Stemmer, and the Lemmatizer is called WordNet.

    """

    # Use basic text processing function to process the raw string
    processed_str = basic_text_processing(raw_str).split()

    # Stem the filtered words using the Snowball stemmer
    stemmer = SnowballStemmer('english')
    stemmed_words = []
    for word in processed_str:
        stemmed_word = stemmer.stem(word)
        stemmed_words.append(stemmed_word)

    # Lemmatize the stemmed words using the WordNet lemmatizer
    lemma = nltk.wordnet.WordNetLemmatizer()
    lemma_words = []
    for word in stemmed_words:
        lemma_word = lemma.lemmatize(word)
        lemma_words.append(lemma_word)
    
    return lemma_words


def n_gram_generation(raw_str: str, n: int) -> dict:
    """

    This function could generate n grams.    
    It will return a dictionary containing all n grams ranked from the highest frequency to the lowest one.
    n must be a positive number.
    
    """

    # Process raw string using basice text processing function and NLP processing function
    nlp_processed_words = nlp_text_processing(raw_str)

    if n>0:
        # generate a list of ngram
        n_gram = ngrams(nlp_processed_words, n)
         # Count the frequency of each ngram in the list
        n_gram_count = Counter(n_gram)
        # Sort the word counts in descending order
        sorted_word_counts = sorted(n_gram_count.items(), key=lambda x: x[1], reverse=True)

        return sorted_word_counts
    else:
        return print('n must be a positive number!')

    