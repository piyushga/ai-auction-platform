from app.core.database import SessionLocal
from app.services.semantic_search_service import SemanticSearchService


QUESTION = "Find experienced Indian batters"


def main():
    db = SessionLocal()

    try:
        search_service = SemanticSearchService(db)
        players = search_service.search_players(
            question=QUESTION,
            limit=5,
        )

        print(f"\nQUESTION: {QUESTION}")
        print("\nSEMANTIC SEARCH RESULTS:")

        if not players:
            print("No players found.")
            return

        for position, player in enumerate(players, start=1):
            print(f"\n{position}. {player['player_name']}")
            print(f"Similarity: {player['similarity']:.4f}")
            print(f"Description: {player['description']}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
