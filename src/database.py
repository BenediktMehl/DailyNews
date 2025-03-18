import sqlite3
import logging
import json
import argparse
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='data/news.db'):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {str(e)}")
            return False

    def initialize_db(self):
        """Create database tables if they don't exist"""
        if self.connect():
            try:
                # Articles table
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    source TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    published_date TEXT NOT NULL,
                    summary TEXT,
                    content TEXT,
                    relevance_score REAL,
                    collected_date TEXT NOT NULL,
                    sent BOOLEAN DEFAULT 0
                )
                """)

                # Sent updates table
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sent_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    sent_date TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """)

                self.conn.commit()
                self.logger.info("Database initialized successfully")
                return True
            except sqlite3.Error as e:
                self.logger.error(f"Database initialization error: {str(e)}")
                return False
            finally:
                self.close()

    def store_articles(self, articles):
        """Store collected articles in database"""
        if self.connect():
            try:
                now = datetime.now().isoformat()
                for article in articles:
                    self.cursor.execute("""
                    INSERT OR IGNORE INTO articles
                    (title, url, source, source_type, published_date, summary, content, relevance_score, collected_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        article['title'],
                        article['url'],
                        article['source'],
                        article['source_type'],
                        article.get('published_date', now),
                        article.get('summary', ''),
                        article.get('content', ''),
                        article.get('relevance_score', 0),
                        now
                    ))

                self.conn.commit()
                self.logger.info(f"Stored {len(articles)} articles in database")
                return True
            except sqlite3.Error as e:
                self.logger.error(f"Error storing articles: {str(e)}")
                return False
            finally:
                self.close()

    def get_top_articles(self, limit=10, unsent_only=True):
        """Get top articles by relevance score"""
        if self.connect():
            try:
                query = """
                SELECT id, title, url, source, source_type, published_date, summary, content, relevance_score
                FROM articles
                """

                if unsent_only:
                    query += ' WHERE sent = 0'

                query += ' ORDER BY relevance_score DESC LIMIT ?'

                self.cursor.execute(query, (limit,))
                rows = self.cursor.fetchall()

                articles = []
                for row in rows:
                    articles.append({
                        'id': row[0],
                        'title': row[1],
                        'url': row[2],
                        'source': row[3],
                        'source_type': row[4],
                        'published_date': row[5],
                        'summary': row[6],
                        'content': row[7],
                        'relevance_score': row[8]
                    })

                return articles
            except sqlite3.Error as e:
                self.logger.error(f"Error retrieving articles: {str(e)}")
                return []
            finally:
                self.close()

    def mark_articles_as_sent(self, article_ids):
        """Mark articles as sent"""
        if self.connect():
            try:
                placeholders = ','.join(['?'] * len(article_ids))
                query = f"""
                    UPDATE articles SET sent = 1
                    WHERE id IN ({placeholders})
                    """
                self.cursor.execute(query, tuple(article_ids))

                self.conn.commit()
                return True
            except sqlite3.Error as e:
                self.logger.error(f"Error marking articles as sent: {str(e)}")
                return False
            finally:
                self.close()

    def log_sent_update(self, content, status):
        """Log sent update"""
        if self.connect():
            try:
                now = datetime.now().isoformat()
                self.cursor.execute("""
                INSERT INTO sent_updates (content, sent_date, status)
                VALUES (?, ?, ?)
                """, (content, now, status))

                self.conn.commit()
                return True
            except sqlite3.Error as e:
                self.logger.error(f"Error logging sent update: {str(e)}")
                return False
            finally:
                self.close()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Developer News Agent')
    parser.add_argument('--init-db', action='store_true', help='Initialize the database')
    args = parser.parse_args()

    if args.init_db:
        # Initialize the database
        db_manager = DatabaseManager()
        db_manager.initialize_db()
