# NLP Streamline Tool
Streamline basic text & NLP processing

## How to Use
1. After installing the package, import the functions you need:

```
from nlpstreamline import (
    basic_text_processing,
    nlp_text_processing,
    n_gram_generation
)
```
2. Use following code to do basic text processing(lowercasing, removing urls, tokenizing, remove stopwords and punctuations), nlp processing (stemming and lemmatizing), and n grams generation.

```
print(basic_text_processing('Good Morning! How are you today?'))

print(nlp_text_processing('Good Morning! How are you today?'))

print(n_gram_generation('Good Morning! How are you today?', 2))

```
