import re
import nltk
import logging
import numpy as np
from typing import Tuple, List
from llama_cpp import Llama
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class QuestionRelevanceAgent:
    def __init__(self, db_tables: str, threshold: float = 0.5, model_path: str = "path/to/your/model.bin"):
        self.threshold = threshold
        self.db_tables = db_tables
        self.llm = Llama(
            model_path=model_path,
            n_ctx=512,
            n_threads=4,
            embedding=True,
            verbose=False
        )  # TODO: Refactor it in an interface class


        self.stop_words = set(stopwords.words('english'))

        logger.info(f"{type(self).__name__} starts initialization..")
        logger.info("Starts embed the database_schema")
        self.db_tables_embedding = self._get_embedding(db_tables)
        logger.info("Embed the database_schema finished successfully!")

    def check_relevance(self, question: str) -> Tuple[bool, float]:
        processed_question = self._preprocess_text(question)
        question_embedding = self._get_embedding(processed_question)
        relevance_score = self._cosine_similarity(self.db_tables_embedding, question_embedding)
        is_relevant = relevance_score >= self.threshold
        return is_relevant, relevance_score

    def _get_embedding(self, text: str) -> np.ndarray:
        embedding = self.llm.embed(text)
        if isinstance(embedding, list):
            embedding = np.array(embedding)
        elif isinstance(embedding, dict) and 'embedding' in embedding:
            embedding = np.array(embedding['embedding'])
        else:
            raise ValueError("Unexpected embedding format")

        # If the embedding is 2D, average across the first dimension
        if embedding.ndim > 1:
            embedding = np.mean(embedding, axis=0)

        return embedding

    def _preprocess_text(self, text: str) -> str:
        # Convert to lowercase
        text = text.lower()

        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stopwords
        tokens = [token for token in tokens if token not in self.stop_words]

        # Join the tokens back into a string
        cleaned_text = ' '.join(tokens)

        return cleaned_text

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))