from apikey import keys
from newsapi import NewsApiClient
from collections import defaultdict
import pandas as pd

newsapi = NewsApiClient(api_key=keys['NewsAPI']['key'])

def to_csv(news, filename):
    all_news = []
    for article in news:
        all_news.append([article['source']['name'], article['publishedAt'], article['title'], article['description']])
    pd.DataFrame(all_news, columns=['source', 'date', 'title', 'description']).to_csv(filename, index_label=False, index=False)

categories = ['science', 'technology', 'general', 'entertainment', 'health', 'business', 'sports'] # politics is not an option
max_results = 1000  # max limit of article querying

for category in categories:
    category_news = []

    num_articles = 0
    requested_articles = 1
    page = 1

    while num_articles < min(requested_articles, max_results):
        requested_news = newsapi.get_top_headlines(category=category, page=page, page_size=100, country='us')

        requested_articles = requested_news['totalResults']
        num_articles += len(requested_news['articles'])
        category_news.extend(requested_news['articles'])
        page += 1

    to_csv(category_news, "sentiments/_todo/{}.csv".format(category))
