import logging
import asyncio
from send.send_telegram_message import send_telegram_message
from fetchContent.rss_news_fetcher import fetch_top_news
from fetchContent.html_content_fetcher import fetch_html_contents
from buildPost.company_llm_summarizer import create_news_summaries
from buildPost.create_news_post import create_news_post


class NewsPostOrchestrator:

    def create_post_from_top_news(self):
        logging.basicConfig(level=logging.INFO)
        
        top_news = fetch_top_news()
        contents = fetch_html_contents(top_news, 3)
        summaries = create_news_summaries(contents)
        news_post = create_news_post(summaries, top_news)

        asyncio.run(send_telegram_message(news_post))

if __name__ == "__main__":
    orchestrator = NewsPostOrchestrator()
    orchestrator.create_post_from_top_news()
