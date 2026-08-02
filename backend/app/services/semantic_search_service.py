from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.embedding_service import generate_embedding


class SemanticSearchService:

    def __init__(self, db: Session):
        self.db = db

    def search_players(
        self,
        question: str,
        limit: int = 5,
        country: str | None = None,
        role: str | None = None,
        team: str | None = None,
        max_price: int | None = None,
    ) -> list[dict]:
        question = question.strip()

        if not question:
            raise ValueError("Question cannot be empty.")

        if limit < 1 or limit > 20:
            raise ValueError("Limit must be between 1 and 20.")

        question_embedding = generate_embedding(question)
        pgvector_embedding = self._embedding_to_pgvector(question_embedding)

        filters = []
        parameters = {
            "embedding": pgvector_embedding,
            "limit": limit,
        }

        if country:
            filters.append("LOWER(p.country) = LOWER(:country)")
            parameters["country"] = country

        if role:
            filters.append("p.role = :role")
            parameters["role"] = role

        if team:
            filters.append("LOWER(p.current_ipl_team) = LOWER(:team)")
            parameters["team"] = team

        if max_price is not None:
            filters.append("auction.sold_price <= :max_price")
            parameters["max_price"] = max_price

        where_clause = ""
        if filters:
            where_clause = "WHERE " + " AND ".join(filters)

        query = text(f"""
            SELECT
                pe.player_id,
                pe.player_name,
                p.country,
                p.role,
                p.current_ipl_team,
                auction.sold_price,
                pe.description,
                pe.embedding <=> CAST(:embedding AS vector) AS distance,
                1 - (pe.embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM player_embeddings pe
            JOIN players p
                ON p.player_id = pe.player_id
            LEFT JOIN LATERAL (
                SELECT a.sold_price
                FROM auction_history a
                WHERE a.player_id = p.player_id
                ORDER BY a.auction_year DESC, a.id DESC
                LIMIT 1
            ) auction ON TRUE
            {where_clause}
            ORDER BY distance
            LIMIT :limit
        """)

        result = self.db.execute(
            query,
            parameters,
        )

        return [dict(player) for player in result.mappings().all()]

    @staticmethod
    def _embedding_to_pgvector(embedding: list[float]) -> str:
        return "[" + ",".join(str(value) for value in embedding) + "]"
