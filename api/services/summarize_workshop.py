# summarize_workshop.py - GPT-5 mini summarization

from dotenv import load_dotenv
import os
import openai
import logging
from ..utils.vector_store import store_embedding

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("GPT5_API_KEY")
if not api_key:
    raise Exception("GPT5_API_KEY not found!")

client = openai.OpenAI(api_key=api_key)

def summarize_workshop(text: str) -> str:
    """
    Summarize a project management or sprint planning transcript using GPT-5 mini.
    """
    try:
        logger.info(f"Summarizing text: {text[:50]}...")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes project management and sprint planning transcripts."},
                {"role": "user", "content": text}
            ],
            max_tokens=300,
            temperature=0.7
        )

        summary = response.choices[0].message.content
        store_embedding(text, summary, f"summary_{hash(text)}")
        logger.info("Summary and embedding stored")

        return summary.strip()

    except Exception as e:
        logger.error(f"Error in summarize_workshop: {str(e)}")
        raise Exception(f"Failed to summarize: {str(e)}")
