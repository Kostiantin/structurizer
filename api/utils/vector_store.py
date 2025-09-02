# My updated vector store with non-deprecated embeddings
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
import faiss
import numpy as np
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    logger.info("Embeddings initialized")
except Exception as e:
    logger.error(f"Failed to initialize embeddings: {str(e)}")
    raise

def store_embedding(text: str, processed_text: str, doc_id: str):
    try:
        index = faiss.IndexFlatL2(384)  # Dimension for all-MiniLM-L6-v2
        embedding = embeddings.embed_query(text)
        index.add(np.array([embedding]))
        # Save index or processed_text to persistent storage if needed
        logger.info(f"Stored embedding for doc_id: {doc_id}")
    except Exception as e:
        logger.error(f"Error storing embedding: {str(e)}")
        raise Exception(f"Failed to store embedding: {str(e)}")