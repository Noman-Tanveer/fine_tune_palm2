import requests
from bs4 import BeautifulSoup

def get_wayback_urls():
    base_url = 'https://web.archive.org/web/*/https://www.bloomberg.com/'

    response = requests.get(base_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    articles = soup.find_all('a', class_='Apple, AAPL')

    wayback_urls = []
    for article in articles:
        url = article['href']
        wayback_urls.append(url)

    return wayback_urls

def extract_article_details(wayback_url):
    response = requests.get(wayback_url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.find('h1', class_='article-title').text.strip()
    content = soup.find('div', class_='article-body').text.strip()

    return {
        'title': title,
        'content': content
    }

def mine_articles():
    wayback_urls = get_wayback_urls()
    articles = []

    for wayback_url in wayback_urls:
        article = extract_article_details(wayback_url)
        articles.append(article)

    return articles

import csv

def store_articles(articles, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'content'])
        writer.writeheader()
        writer.writerows(articles)

