# generate_diagram.py - GPT-4o-mini diagram generation in Mermaid syntax

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

def generate_diagram(text: str, diagram_type: str = "flowchart") -> str:
    """
    Generate a Mermaid diagram from a project management transcript.
    Returns a string containing the Mermaid code.
    """
    try:
        logger.info(f"Generating diagram for text: {text[:50]}...")

        prompt = (
            f"Generate a {diagram_type} diagram in Mermaid syntax for a project management workflow based on the provided transcript.\n"
            "Focus on tasks, assignees, and dependencies.\n"
            "Return ONLY the Mermaid code as plain text (no markdown ``` markers, no explanations, no extra text).\n"
            "The diagram must start with '{diagram_type} TD' and use '-->' for relationships.\n"
            "Use '|Assigned to|' for assignee relationships and '|Depends on|' for dependencies.\n"
            "Ensure the diagram is complete with proper syntax (e.g., nodes in square brackets, no missing connections).\n"
            "Example for a transcript about route planning:\n"
            "Transcript: Team plans route planning and real-time updates, assigned to Anna, with API integration challenges by David.\n"
            "Diagram:\n"
            "flowchart TD\n"
            "    A[Define Features] -->|Assigned to| B(Anna)\n"
            "    A --> C[Routeplanning]\n"
            "    A --> D[Real-time Updates]\n"
            "    C -->|Assigned to| E(Anna)\n"
            "    D -->|Assigned to| F(Anna)\n"
            "    G[Identify Challenges] -->|Assigned to| H(David)\n"
            "    G --> I[API Integration]\n"
            "    I -->|Assigned to| J(David)\n"
            "    C -->|Depends on| I\n"
            "    D -->|Depends on| I\n\n"
            f"Transcript:\n{text}\n\nDiagram:"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that creates Mermaid diagrams for project management workflows."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,  # Ensure enough tokens for complete output
            temperature=0.7
        )

        diagram = response.choices[0].message.content.strip()

        # Validate the diagram syntax
        if not diagram.startswith(f"{diagram_type} ") or "-->" not in diagram:
            logger.error(f"Invalid Mermaid diagram generated: {diagram}")
            raise ValueError("Generated diagram is invalid or incomplete")

        store_embedding(text, diagram, f"diagram_{hash(text)}")
        logger.info("Diagram and embedding stored")

        return diagram

    except Exception as e:
        logger.error(f"Error in generate_diagram: {str(e)}")
        raise Exception(f"Failed to generate diagram: {str(e)}")