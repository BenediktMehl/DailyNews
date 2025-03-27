import openai
import os
from dotenv import load_dotenv

load_dotenv()

def summarize_content_with_company_llm(text: str) -> str:
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
                "content": f"Summarize the following text: {text}"
            }
        ]
    )

    return response.choices[0].message.content.strip()
