import logging
import openai
import os
from dotenv import load_dotenv
import emoji

load_dotenv()

def choose_icon(summary: str) -> str:
    logging.basicConfig(level=logging.INFO)
    logging.info("Fetch: Choose a nice icon")
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_URL")

    client = openai.OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Choose a nice icon for the following text: {summary}. The icon should be relevant to the content and visually appealing. Provide the icon in a simple json text format: {{'icon': 'icon_name'}}. For example, if the text is about technology, you might return {{'icon': '💻'}}. If the text is about nature, you might return {{'icon': '🌳'}}. Please ensure that the icon is appropriate and matches the context of the text."
            }
        ]
    )

    json = response.choices[0].message.content.strip()
    icon = json.split("'icon': '")[1].split("'")[0]

    logging.info(f"AI Interaction: Received icon: {icon}")
    
    if not emoji.is_emoji(icon):
        logging.warning(f"AI Interaction: Icon {icon} is not a valid emoji. Returning default icon.")
        icon = "🌟"

    return icon
