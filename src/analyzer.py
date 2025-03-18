import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import logging
import re

class ContentAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
    
    def analyze_articles(self, articles):
        """Analyze and score articles"""
        self.logger.info(f"Analyzing {len(articles)} articles")
        for article in articles:
            # Calculate various metrics
            article['keyword_score'] = self.extract_keywords(article)
            article['length_score'] = self.calculate_length_score(article)
            article['relevance_score'] = self.calculate_relevance_score(article)
        
        return articles
    
    def extract_keywords(self, article):
        """Extract important keywords from article"""
        text = article['title'] + " " + article['summary']
        tokens = word_tokenize(text.lower())
        # Remove stopwords and punctuation
        keywords = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        
        # Count developer-related terms
        dev_terms = ['code', 'developer', 'programming', 'software', 'api', 
                    'github', 'python', 'javascript', 'java', 'cloud', 
                    'devops', 'ai', 'machine learning', 'data']
        
        keyword_score = sum(1 for word in keywords if any(term in word for term in dev_terms))
        return keyword_score
    
    def calculate_length_score(self, article):
        """Score based on content length - favor substantial but not excessive content"""
        content_length = len(article['content'])
        if content_length < 100:
            return 0.3  # Too short
        elif content_length < 500:
            return 0.7  # Good length
        elif content_length < 2000:
            return 1.0  # Ideal length
        else:
            return 0.8  # Long but acceptable
    
    def calculate_relevance_score(self, article):
        """Calculate overall relevance score"""
        # Combine different factors with weights
        keyword_weight = 0.6
        length_weight = 0.2
        source_weight = 0.2
        
        # Source type bonus (can be adjusted)
        source_score = 1.0  # Default
        
        # Final weighted score
        score = (article['keyword_score'] * keyword_weight + 
                article['length_score'] * length_weight + 
                source_score * source_weight)
        
        return score
