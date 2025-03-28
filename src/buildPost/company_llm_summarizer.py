import logging
import openai
import os
from dotenv import load_dotenv

load_dotenv()

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
                "content": f"Summarize the following text like news agencies would do. Have one headline sentence and then one to three sentences that give some context and detail like this: '*New Study Suggests Preschoolers Exhibit Advanced Reasoning Skills*  The study indicates that preschool-aged children may possess more sophisticated reasoning abilities than previously recognized. Researchers found that these young learners can engage in complex problem-solving, challenging the conventional view of early cognitive development. The findings could have implications for early childhood education strategies.' If the given text does not contain a summarizable text, simply return 'null'. This is the text: {text}"
            }
        ]
    )

    summary = response.choices[0].message.content.strip()

    if summary == 'null':
        logging.warning(f"AI Interaction: Failed to create summary for text: {text}")
        return None

    logging.info(f"AI Interaction: Received summary: {summary}")
    return summary
