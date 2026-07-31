from sqlalchemy import text

from app.core.database import SessionLocal
from app.repositories.player_repository import PlayerRepository
from app.services.embedding_service import generate_embedding
from app.services.player_description_service import PlayerDescriptionService


def embedding_to_pgvector(embedding: list[float]) -> str:
    return "[" + ",".join(str(value) for value in embedding) + "]"


def main():
    db = SessionLocal()

    try:
        repository = PlayerRepository(db)
        player = repository.get_player_details("Virat Kohli")

        if player is None:
            print("Player not found!")
            return

        already_stored = db.execute(
            text(
                "SELECT id FROM player_embeddings "
                "WHERE player_id = :player_id LIMIT 1"
            ),
            {"player_id": player["player_id"]},
        ).scalar_one_or_none()

        if already_stored is not None:
            print("Virat Kohli already has a stored embedding.")
            return

        special_stats = repository.get_special_stats(player["player_id"])
        description = PlayerDescriptionService().generate_description(
            player,
            special_stats,
        )
        embedding = generate_embedding(description)

        embedding_id = db.execute(
            text("""
                INSERT INTO player_embeddings (
                    player_id,
                    player_name,
                    description,
                    embedding
                )
                VALUES (
                    :player_id,
                    :player_name,
                    :description,
                    CAST(:embedding AS vector)
                )
                RETURNING id
            """),
            {
                "player_id": player["player_id"],
                "player_name": player["name"],
                "description": description,
                "embedding": embedding_to_pgvector(embedding),
            },
        ).scalar_one()

        db.commit()

        print(f"Stored {player['name']} embedding with id: {embedding_id}")
        print(f"Vector length: {len(embedding)}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
