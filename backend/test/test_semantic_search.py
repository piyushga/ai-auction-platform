from app.core.database import SessionLocal
from app.services.query_processing_service import QueryProcessingService
from app.services.semantic_search_service import SemanticSearchService


QUESTION = "Find experinced Indain bastmen under 25 cror"


def main():
    db = SessionLocal()

    try:
        parsed_query = QueryProcessingService(db).parse(QUESTION)

        print(f"\nORIGINAL QUESTION: {parsed_query.original_text}")
        print(f"NORMALIZED TEXT: {parsed_query.normalized_text}")
        print(f"COUNTRY FILTER: {parsed_query.country}")
        print(f"ROLE FILTER: {parsed_query.role}")
        print(f"TEAM FILTER: {parsed_query.team}")
        print(f"MAXIMUM PRICE: {parsed_query.max_price}")
        print(f"CORRECTIONS: {parsed_query.corrections}")

        players = SemanticSearchService(db).search_players(
            question=parsed_query.normalized_text,
            limit=5,
            country=parsed_query.country,
            role=parsed_query.role,
            team=parsed_query.team,
            max_price=parsed_query.max_price,
        )

        print("\nFILTERED SEMANTIC SEARCH RESULTS:")

        if not players:
            print("No players matched the filters.")
            return

        for position, player in enumerate(players, start=1):
            print(f"\n{position}. {player['player_name']}")
            print(f"Country: {player['country']}")
            print(f"Role: {player['role']}")
            print(f"Sold price: {player['sold_price']}")
            print(f"Similarity: {player['similarity']:.4f}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
