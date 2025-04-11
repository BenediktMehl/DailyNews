import logging
import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()


def create_news_topics(topics: list, max_number_of_news = 3) -> list:
    topics_with_ai = []
    number_of_summaries = 0
    for topic in topics:
        content = topic['content']
        if len(content) < 1000 or len(content) > 15000:
            logging.warning(f"AI Interaction: Text length is not valid: {len(content)} characters")
            continue
        if number_of_summaries >= max_number_of_news:
            break
        topic_ai = create_news_topic(topic)
        if topic_ai is None:
            logging.warning(f"AI Interaction: Failed to create topic")
        else:
            logging.info(f"AI Interaction: Created topic: {topic_ai}")
            number_of_summaries += 1
            topics_with_ai.append(topic_ai)
    return topics_with_ai


def create_news_topic(topic: dict) -> dict:
    logging.basicConfig(level=logging.INFO)
    logging.info("Fetch: Fetching API key and base URL from environment variables")
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_URL")

    logging.info("AI Interaction: Initializing OpenAI client")
    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    logging.info("AI Interaction: Creating chat completion request")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"""
                                Have a title, one headline sentence and then one or two sentences that give some context and details.
                                The text should be very short (like the example below), easy to read and in high quality, but simple english, like news agencies would write it.
                                You respond in the following json format: 
                                {{
                                    "headline": "Criticism of additional US tariffs on imported cars",
                                    "entry_sentence": "The USA has announced additional tariffs of 25% on car imports."
                                    "detail": "They are to come into force on April 2 and apply to all cars not produced in the USA."
                                }}
                                Dont put any links or references into the summary. If the given text does not contain a summarizable text, simply return 'null'. 
                                This is the text: {topic['content']}
                            """
            }
        ]
    )

    try:
        string_response = response.choices[0].message.content.strip()
        logging.info(f"AI Interaction: Received response from OpenAI API: {string_response}")

        if string_response == "null":
            return None

        json_response = json.loads(string_response.strip('```json').strip('```').strip())

        if "headline" not in json_response or "entry_sentence" not in json_response or "detail" not in json_response:
            logging.warning(f"AI Interaction: JSON object does not contain required fields: {json_response}")
            return None
        return topic | json_response
    except Exception as e:
        logging.error(f"AI Interaction: Failed to parse JSON: {e}")
        return None
