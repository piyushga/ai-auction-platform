from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.embedding_service import generate_embedding


class SemanticSearchService:

    def __init__(self, db: Session):
        self.db = db

    def search_players(self, question: str, limit: int = 5) -> list[dict]:
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        if limit < 1 or limit > 20:
            raise ValueError("Limit must be between 1 and 20.")

        question_embedding = generate_embedding(question)
        pgvector_embedding = self._embedding_to_pgvector(question_embedding)

        query = text("""
            SELECT
                player_id,
                player_name,
                description,
                embedding <=> CAST(:embedding AS vector) AS distance,
                1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM player_embeddings
            ORDER BY distance
            LIMIT :limit
        """)

        result = self.db.execute(
            query,
            {
                "embedding": pgvector_embedding,
                "limit": limit,
            },
        )

        return [dict(player) for player in result.mappings().all()]

    @staticmethod
    def _embedding_to_pgvector(embedding: list[float]) -> str:
        return "[" + ",".join(str(value) for value in embedding) + "]"
