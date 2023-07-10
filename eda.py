import requests
import yfinance as yf
import json
import datetime
import time
import os
from newsapi import NewsApiClient
from concurrent.futures import ThreadPoolExecutor
import hashlib
import sys
import logging
import argparse
from Levenshtein import distance as levenshtein_distance
from datetime import datetime, timedelta
import feedparser
import concurrent.futures
import requests
import pandas as pd


NEWS_API_KEY="27aa1b04bca0464bb3df847f7ce9e876"
# STOCKNEWS_API_KEY = "yztzsrpbo1i16ngef0tp3kjtlemdvl9sh9xemdvz"


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    stream=sys.stderr
)

logging.getLogger().setLevel(logging.INFO)
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def calculate_similarity(string1, string2):
    """Calculate the similarity between two strings using the OSA distance."""
    # Calculate the Levenshtein distance
    distance = levenshtein_distance(string1, string2)
    # Calculate the maximum possible distance
    max_distance = max(len(string1), len(string2))
    # Calculate the similarity
    similarity = 1 - distance / max_distance
    return similarity

def remove_similar_articles(news_list, similarity_threshold=0.6):
    logging.info("Removing similar headlines...")
    """Remove headlines with a similarity greater than the specified threshold."""
    # Initialize an empty list to store the unique news
    unique_news = []
    # Initialize a counter for the number of removed headlines
    removed_headlines = 0
    # Loop over the news in the list
    for news in news_list:
        # Assume that the news is unique until proven otherwise
        is_unique = True
        # Loop over the unique news
        for unique in unique_news:
            # If the news is for the same company on the same day
            # Calculate the similarity between the headlines
            similarity = calculate_similarity(news['title'], unique['title'])
            # If the similarity is greater than the threshold
            if similarity > similarity_threshold:
                # The news is not unique
                is_unique = False
                # logging.info(f"Removing duplicate headline: {news['title']}")
                # logging.info(f"Similarity with headline: {unique['title']}")
                removed_headlines += 1
                break
        # If the news is unique
        if is_unique:
            # Add it to the list of unique news
            unique_news.append(news)
    logging.info(f"Total similar headlines removed: {removed_headlines}")
    return unique_news

def get_news_api(dat):
    # Search for news related to a specific stock
    news = newsapi.get_everything(q=ticker,
                                  from_param=dat - timedelta(days=3),
                                  to=dat,
                                  language='en',
                                  sort_by='relevancy',
                                  )

    # Access and process the news articles
    articles = news['articles']
    articles = remove_similar_articles(articles)
    return articles

        
if __name__ == "__main__":
    ticker = 'AAPL'
    df = pd.read_csv("clean_data.csv")
    # df["Gain"] = df["Close"] - df["Open"]
    df["Series"] = 1
    for index, row in df.iterrows():
        dat = row['Date']
        parsed_date = datetime.strptime(dat, "%Y-%m-%d")
        if parsed_date < datetime.strptime("2023-06-10", "%Y-%m-%d"):
            df.at[index, 'news'] = ""
            continue
        unique_articles = get_news_api(parsed_date)
        day_text = " ".join(articl['description'] for articl in unique_articles)
        df.at[index, 'news'] = new_value = day_text
    df = df.drop(["Unnamed: 0"], axis=1)
    df = df[["Series", "Date", "Gain", "news", "Volume"]]
    df.to_csv('clean_data.csv', index = False)
