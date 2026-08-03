from collections.abc import Generator

from sqlalchemy.orm import Session

from app.services.openai_service import stream_chat
from app.services.query_processing_service import QueryProcessingService
from app.services.semantic_search_service import SemanticSearchService


class RAGService:

    def __init__(self, db: Session):
        self.query_processing_service = QueryProcessingService(db)
        self.semantic_search_service = SemanticSearchService(db)

    def stream_answer(self, question: str) -> Generator[str, None, None]:
        parsed_query = self.query_processing_service.parse(question)
        search_text = self._apply_corrections(
            parsed_query.normalized_text,
            parsed_query.corrections,
        )

        if parsed_query.player_names:
            players = self.semantic_search_service.get_players_by_names(
                parsed_query.player_names
            )
        else:
            players = self.semantic_search_service.search_players(
                question=search_text,
                limit=5,
                country=parsed_query.country,
                role=parsed_query.role,
                team=parsed_query.team,
                max_price=parsed_query.max_price,
            )

        context = self._build_player_context(players)
        rag_input = self._build_rag_input(
            question=question,
            context=context,
        )

        yield from stream_chat(rag_input)

    def _apply_corrections(
        self,
        normalized_text: str,
        corrections: dict[str, str],
    ) -> str:
        corrected_text = normalized_text

        for typed_value, corrected_value in sorted(
            corrections.items(),
            key=lambda correction: len(correction[0]),
            reverse=True,
        ):
            normalized_correction = self.query_processing_service.normalize(
                corrected_value
            )
            corrected_text = corrected_text.replace(
                typed_value,
                normalized_correction,
            )

        return corrected_text

    @staticmethod
    def _build_player_context(players: list[dict]) -> str:
        if not players:
            return "No relevant player records were retrieved from the database."

        player_documents = []

        for position, player in enumerate(players, start=1):
            similarity_line = ""
            if player["similarity"] is not None:
                similarity_line = f"Similarity: {player['similarity']:.4f}\n"

            player_documents.append(
                f"Player {position}: {player['player_name']}\n"
                f"Country: {player['country']}\n"
                f"Role: {player['role']}\n"
                f"Current IPL team: {player['current_ipl_team']}\n"
                f"Recorded sold price: {player['sold_price']}\n"
                f"{similarity_line}"
                f"Description: {player['description']}"
            )

        return "\n\n".join(player_documents)

    @staticmethod
    def _build_rag_input(question: str, context: str) -> str:
        return f"""
User question:
{question}

Retrieved player context:
{context}
""".strip()
