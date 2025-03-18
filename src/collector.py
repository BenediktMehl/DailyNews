import feedparser
import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime, timedelta

class NewsCollector:
    def __init__(self, db_manager, config_path='config/sources.json'):
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)
        with open(config_path, 'r') as f:
            self.sources = json.load(f)
    
    def collect_all(self):
        """Collect news from all configured sources"""
        articles = []
        for category in ['developer', 'mainstream']:
            for source in self.sources[category]:
                try:
                    if source['type'] == 'rss':
                        new_articles = self.collect_from_rss(source['url'], source['name'], category)
                        articles.extend(new_articles)
                    elif source['type'] == 'api':
                        new_articles = self.collect_from_api(source)
                        articles.extend(new_articles)
                except Exception as e:
                    self.logger.error(f"Error collecting from {source['name']}: {str(e)}")
        
        # Store in database
        self.db_manager.store_articles(articles)
        return articles
    
    def collect_from_rss(self, url, source_name, category):
        """Collect news from RSS feed"""
        self.logger.info(f"Collecting from RSS: {source_name}")
        feed = feedparser.parse(url)
        articles = []
        
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_start = yesterday.replace(hour=0, minute=0, second=0)
        
        for entry in feed.entries:
            # Parse date
            if hasattr(entry, 'published_parsed'):
                pub_date = datetime(*entry.published_parsed[:6])
            else:
                # If no date, assume recent
                pub_date = datetime.now()
            
            # Only include articles from yesterday
            if pub_date >= yesterday_start and pub_date < datetime.now():
                article = {
                    'title': entry.title,
                    'url': entry.link,
                    'source': source_name,
                    'source_type': category,
                    'published_date': pub_date.isoformat(),
                    'summary': entry.summary if hasattr(entry, 'summary') else '',
                    'content': entry.content[0].value if hasattr(entry, 'content') else entry.summary if hasattr(entry, 'summary') else '',
                }
                articles.append(article)
        
        return articles
    
    def collect_from_api(self, source):
        """Collect news from API source"""
        # Implementation depends on specific API
        pass
