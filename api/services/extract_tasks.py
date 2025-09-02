# extract_tasks.py - GPT-5 mini task extraction

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

def extract_tasks(text: str) -> str:
    """
    Extract actionable tasks from a project management or sprint planning transcript.
    """
    try:
        logger.info(f"Extracting tasks from text: {text[:50]}...")

        prompt = (
            "Extract actionable tasks from this project management or sprint planning transcript.\n"
            "Each bullet should:\n"
            "- Start with a verb (actionable)\n"
            "- Include assignee if mentioned\n"
            "- Include deadlines if mentioned\n"
            "- Be short and clear\n\n"
            f"Transcript:\n{text}\n\nTasks:"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts tasks from project transcripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        tasks = response.choices[0].message.content
        store_embedding(text, tasks, f"tasks_{hash(text)}")
        logger.info("Tasks and embedding stored")

        return tasks.strip()

    except Exception as e:
        logger.error(f"Error in extract_tasks: {str(e)}")
        raise Exception(f"Failed to extract tasks: {str(e)}")
