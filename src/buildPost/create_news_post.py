import logging
from buildPost.create_image import create_image
from buildPost.llm_icon_chooser import choose_icon

def create_news_post(news_topics, top_news) -> str:
    logging.basicConfig(level=logging.INFO)
    logging.info("Fetch: Reading post template")
    with open('src/buildPost/post_template.txt', 'r') as template_file:
        template = template_file.read()

    logging.info("AI Interaction: Formatting post with news topics and URLs")
    formatted_post = template

    news_topics_str = "\n\n".join(f"{choose_icon(topic)} *{topic['entry_sentence']}* {topic['detail']} {top_news[i]['url']}" for i, topic in enumerate(news_topics))
    news_topics_str = f"\n{news_topics_str}\n"
    formatted_post = formatted_post.replace("[News Topics]", news_topics_str)
    
    logging.info(f"AI Interaction: Post formatted successfully: {formatted_post}")

    image = create_image(news_topics)

    return (image, formatted_post)
