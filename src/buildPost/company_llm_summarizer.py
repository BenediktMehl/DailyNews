import logging
import re
import openai
import os
from dotenv import load_dotenv

load_dotenv()

def create_news_summaries(texts: list) -> list:
    summaries = []
    for text in texts:
        summary = create_news_summary(text)
        if summary is None:
            logging.warning(f"AI Interaction: Failed to create summary for text: {text}")
        else:
            logging.info(f"AI Interaction: Created summary: {summary}")
            summaries.append(summary)
    return summaries

def create_news_summary(text: str) -> str:
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
                                Summarize the following text in maximum 2-3 sentences like news agencies would do. 
                                Have a title, one headline sentence and then one to three sentences that give some context and detail like this: 
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



