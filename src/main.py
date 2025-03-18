import logging
import os
import json
from datetime import datetime
import argparse

from collector import NewsCollector
from analyzer import ContentAnalyzer
from generator import ContentGenerator
from delivery import WhatsAppDelivery
from database import DatabaseManager
from scheduler import LocalScheduler

class DevNewsAgent:
    def __init__(self, config_path='config/settings.json'):
        # Setup logging
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize components
        self.db_manager = DatabaseManager(self.config.get('db_path', 'data/news.db'))
        self.collector = NewsCollector(self.db_manager, self.config.get('sources_path', 'config/sources.json'))
        self.analyzer = ContentAnalyzer()
        self.generator = ContentGenerator()
        self.delivery = WhatsAppDelivery(self.config.get('whatsapp_path', 'config/whatsapp.json'))
    
    def setup_logging(self):
        """Set up logging configuration"""
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{log_dir}/app.log"),
                logging.StreamHandler()
            ]
        )
    
    def run(self):
        """Run the complete news pipeline"""
        self.logger.info("Starting news pipeline")
        
        # Step 1: Collect news
        articles = self.collector.collect_all()
        if not articles:
            self.logger.warning("No articles collected")
            return False
        
        # Step 2: Analyze content
        analyzed_articles = self.analyzer.analyze_articles(articles)
        
        # Step 3: Get top articles from database (includes newly collected ones)
        top_articles = self.db_manager.get_top_articles(limit=10)
        
        # Step 4: Select balanced mix (at least one from each category)
        selected_articles = self.select_balanced_articles(top_articles, count=3)
        if not selected_articles:
            self.logger.warning("No articles selected for update")
            return False
        
        # Step 5: Generate content
        news_update = self.generator.generate_news_update(selected_articles)
        
        # Step 6: Deliver to WhatsApp
        success, response = self.delivery.send_to_channel(news_update)
        
        # Step 7: Update database
        if success:
            article_ids = [article['id'] for article in selected_articles]
            self.db_manager.mark_articles_as_sent(article_ids)
            self.db_manager.log_sent_update(news_update, "success")
            self.logger.info("News update sent successfully")
        else:
            self.db_manager.log_sent_update(news_update, f"failed: {response}")
            self.logger.error(f"Failed to send news update: {response}")
        
        return success
    
    def select_balanced_articles(self, articles, count=3):
        """Select a balanced mix of articles"""
        if not articles:
            return []
        
        # Separate by source type
        dev_articles = [a for a in articles if a['source_type'] == 'developer']
        mainstream_articles = [a for a in articles if a['source_type'] == 'mainstream']
        
        selected = []
        
        # Ensure at least one from each category if available
        if dev_articles:
            selected.append(dev_articles[0])
        if mainstream_articles:
            selected.append(mainstream_articles[0])
        
        # Fill remaining slots with highest scored remaining articles
        remaining = [a for a in articles if a not in selected]
        remaining.sort(key=lambda x: x['relevance_score'], reverse=True)
        selected.extend(remaining[:count-len(selected)])
        
        return selected[:count]

def main():
    parser = argparse.ArgumentParser(description='Developer News Agent')
    parser.add_argument('--run-now', action='store_true', help='Run the news pipeline immediately')
    parser.add_argument('--schedule', action='store_true', help='Start the scheduler')
    parser.add_argument('--time', type=str, default="06:00", help='Scheduled run time (HH:MM)')
    args = parser.parse_args()
    
    agent = DevNewsAgent()
    
    if args.run_now:
        agent.run()
    
    if args.schedule:
        scheduler = LocalScheduler(agent, args.time)
        scheduler.start()

if __name__ == "__main__":
    main()
