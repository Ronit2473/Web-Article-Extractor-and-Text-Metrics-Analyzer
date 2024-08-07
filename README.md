# Ronit2473-Web-Article-Extractor-and-Text-Metrics-Analyzer
The Web-Article-Extractor-and-Text-Metrics-Analyzer is a Python-based solution designed to extract and analyze web articles. It performs the following key tasks:

Web Scraping: Fetches articles from provided URLs, extracting titles and content using BeautifulSoup.
Text Processing: Computes various textual metrics, including sentiment scores, average sentence length, text complexity (FOG index), and word statistics.
Sentiment Analysis: Evaluates the sentiment of the article content using TextBlob, providing positive and negative sentiment scores.
Data Analysis: Analyzes text complexity and readability by calculating metrics like syllable count per word, percentage of complex words, and personal pronoun usage.
Output Generation: Saves the extracted articles and their analysis results in both Excel and CSV formats for easy review and further processing.
The toolkit is designed to help researchers, content analysts, and data scientists gain insights from web articles efficiently.

Features:

Automated extraction of article titles and content
Comprehensive text analysis including sentiment and readability metrics
Output in multiple formats for flexibility in data handling
Usage:

Prepare an Excel file with URLs to be analyzed.
Run the script to extract and analyze the articles.
Review results in the generated Excel and CSV files.

Dependencies:

pandas
requests
beautifulsoup4
textblob
nltk
openpyxl
