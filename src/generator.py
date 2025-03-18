import logging
from datetime import datetime
import re

class ContentGenerator:
    def __init__(self, template_path=None):
        self.logger = logging.getLogger(__name__)
        self.template = """
Good morning from the Dev News team! ☕️
Here are this morning's top stories:

{news_items}

Have a productive day!

Don't miss any updates - hit the notification bell! 🔔
"""
    
    def generate_news_update(self, articles):
        """Generate formatted news update from top articles"""
        self.logger.info(f"Generating news update from {len(articles)} articles")
        
        news_items = []
        for i, article in enumerate(articles):
            summary = self.create_summary(article)
            news_items.append(f"🔵 {article['title']}\n{summary} {article['url']}")
        
        news_content = "\n\n".join(news_items)
        
        # Format the complete message
        today = datetime.now().strftime("%A, %B %d, %Y")
        message = self.template.format(news_items=news_content)
        
        return message
    
    def create_summary(self, article):
        """Create a concise summary of the article"""
        # Start with existing summary if available
        if article['summary'] and len(article['summary']) > 10:
            # Clean HTML tags
            summary = re.sub('<.*?>', '', article['summary'])
            # Truncate if too long
            if len(summary) > 200:
                summary = summary[:197] + "..."
            return summary
        
        # Fallback to first paragraph of content
        if article['content']:
            # Clean HTML tags
            content = re.sub('<.*?>', '', article['content'])
            # Get first paragraph or sentence
            first_para = content.split('\n')[0]
            if len(first_para) > 200:
                first_para = first_para[:197] + "..."
            return first_para
        
        # Last resort
        return f"Latest news from {article['source']}."
