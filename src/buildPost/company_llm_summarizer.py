import logging
import re
import openai
import os
from dotenv import load_dotenv

load_dotenv()


def create_news_summaries(texts: list) -> list:
    news_topics = []
    number_of_summaries = 0
    for text in texts:
        if len(text) < 1000 or len(text) > 15000:
            logging.warning(f"AI Interaction: Text length is not valid: {len(text)} characters")
            continue
        if number_of_summaries >= 3:
            break
        topic = create_news_topic(text)
        if topic is None:
            logging.warning(f"AI Interaction: Failed to create topic")
        else:
            logging.info(f"AI Interaction: Created topic: {topic}")
            number_of_summaries += 1
            news_topics.append(topic)
    return news_topics


def create_news_topic(text: str) -> str:
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
                                The text should be easy to read and in high quality, but simple english, like news agencies would write it.
                                You respond in the following json format: 
                                {{
                                    "headline": "Criticism of additional US tariffs on imported cars",
                                    "entry_sentence": "The USA has announced additional tariffs of 25% on car imports."
                                    "detail": "They are to come into force on April 2 and apply to all cars not produced in the USA."
                                }}
                                Dont put any links or references into the summary. If the given text does not contain a summarizable text, simply return 'null'. 
                                This is the text: {text}
                            """
            }
        ]
    )


    try:
        json = response.choices[0].message.content.strip()
        logging.info(f"AI Interaction: Received response from OpenAI API: {json}")

        if json == "null":
            return None
        json = json.replace("'", '"')
        json = json.replace("“", '"').replace("”", '"')
        json = json.replace("‘", '"').replace("’", '"')
        json_response = eval(json)
        if not isinstance(json_response, dict):
            logging.warning(f"AI Interaction: Response is not a valid JSON object: {json_response}")
            return None
        if "headline" not in json_response or "entry_sentence" not in json_response or "detail" not in json_response:
            logging.warning(f"AI Interaction: JSON object does not contain required fields: {json_response}")
            return None
        return json_response
    except Exception as e:
        logging.error(f"AI Interaction: Failed to parse JSON: {e}")
        return None
