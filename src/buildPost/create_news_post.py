import os
from src.fetchContent.html_content_fetcher import HTMLContentFetcher
from src.buildPost.company_llm_summarizer import create_news_summary

def create_news_post(news_topics, urls) -> str:
    with open('src/buildPost/post_template.txt', 'r') as template_file:
        template = template_file.read()

    formatted_post = template
    news_topics_str = "\n\n".join(f"🌟 {topic} {urls[i]}" for i, topic in enumerate(news_topics))
    news_topics_str = f"\n\n{news_topics_str}\n\n"
    formatted_post = formatted_post.replace("[News Topics]", news_topics_str)

    return formatted_post
