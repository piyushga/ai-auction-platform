from app.core.database import SessionLocal
from app.repositories.player_repository import PlayerRepository
from app.services.embedding_service import generate_embedding
from app.services.player_description_service import PlayerDescriptionService


def main():
    db = SessionLocal()

    try:
        repository = PlayerRepository(db)
        player = repository.get_player_details("Virat Kohli")

        if player is None:
            print("Player not found!")
            return

        special_stats = repository.get_special_stats(player["player_id"])

        description_service = PlayerDescriptionService()
        description = description_service.generate_description(
            player,
            special_stats,
        )

        embedding = generate_embedding(description)

        print("\nPLAYER DESCRIPTION:\n")
        print(description)
        print("\nEMBEDDING DETAILS:\n")
        print(f"Vector length: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
