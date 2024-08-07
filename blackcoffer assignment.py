#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import re
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

input_df = pd.read_excel('Input.xlsx')

os.makedirs('articles', exist_ok=True)

def extract_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').get_text(strip=True)
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.get_text(strip=True) for para in paragraphs])
        return title, article_text
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return None, None

for index, row in input_df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']
    try:
        title, article_text = extract_article(url)
        if title and article_text:
            with open(f'articles/{url_id}.txt', 'w', encoding='utf-8') as file:
                file.write(title + '\n' + article_text)
            print(f'Successfully extracted article from {url}')
        else:
            print(f'Failed to extract article from {url}')
    except Exception as e:
        print(f'Failed to extract article from {url}: {e}')

def count_syllables(word):
    word = word.lower()
    vowels = 'aeiouy'
    count = 0

    if word.endswith('es') or word.endswith('ed'):
        if len(word) > 2 and word[-3] not in vowels:
            count -= 1

    if word[0] in vowels:
        count += 1

    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1

    if word.endswith('e'):
        count -= 1

    if count == 0:
        count += 1

    return count

def compute_variables(text):
    blob = TextBlob(text)
    
    positive_score = sum(1 for word in blob.words if word.lower() in positive_words)
    negative_score = sum(1 for word in blob.words if word.lower() in negative_words)
    
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    
    sentences = blob.sentences
    avg_sentence_length = sum(len(sentence.words) for sentence in sentences) / len(sentences)
    complex_words = [word for word in blob.words if len(nltk.word_tokenize(word)) > 2]
    percentage_of_complex_words = len(complex_words) / len(blob.words) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)
    word_count = len(blob.words)
    syllable_per_word = sum(count_syllables(word) for word in blob.words) / word_count
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
    avg_word_length = sum(len(word) for word in blob.words) / word_count
    
    return {
        'positive_score': positive_score,
        'negative_score': negative_score,
        'polarity_score': polarity_score,
        'subjectivity_score': subjectivity_score,
        'avg_sentence_length': avg_sentence_length,
        'percentage_of_complex_words': percentage_of_complex_words,
        'fog_index': fog_index,
        'word_count': word_count,
        'syllable_per_word': syllable_per_word,
        'personal_pronouns': personal_pronouns,
        'avg_word_length': avg_word_length,
    }

positive_words = set(open('positive-words.txt').read().split())
negative_words = set(open('negative-words.txt').read().split())

results = []
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    try:
        with open(f'articles/{url_id}.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        variables = compute_variables(text)
        results.append({
            'URL_ID': url_id,
            'URL': row['URL'],
            **variables
        })
        print(f'Successfully analyzed article {url_id}')
    except Exception as e:
        print(f'Failed to analyze article {url_id}: {e}')

output_df = pd.DataFrame(results)
output_df.to_excel('Output Data Structure.xlsx', index=False)
output_df.to_csv('Output Data Structure.csv', index=False)


# In[ ]:




