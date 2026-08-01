from sqlalchemy import text

from app.core.database import SessionLocal
from app.repositories.player_repository import PlayerRepository
from app.services.embedding_service import generate_embedding
from app.services.player_description_service import PlayerDescriptionService


def embedding_to_pgvector(embedding: list[float]) -> str:
    return "[" + ",".join(str(value) for value in embedding) + "]"


def main():
    db = SessionLocal()
    repository = PlayerRepository(db)
    description_service = PlayerDescriptionService()

    created_count = 0
    updated_count = 0
    skipped_count = 0
    failed_count = 0

    try:
        player_names = db.execute(
            text("SELECT name FROM players ORDER BY player_id")
        ).scalars().all()

        for player_name in player_names:
            try:
                player = repository.get_player_details(player_name)

                if player is None:
                    print(f"Skipped {player_name}: player details not found.")
                    skipped_count += 1
                    continue

                special_stats = repository.get_special_stats(player["player_id"])
                description = description_service.generate_description(
                    player,
                    special_stats,
                )

                existing_embedding = db.execute(
                    text("""
                        SELECT id, description
                        FROM player_embeddings
                        WHERE player_id = :player_id
                        ORDER BY id
                        LIMIT 1
                    """),
                    {"player_id": player["player_id"]},
                ).mappings().first()

                if existing_embedding and existing_embedding["description"] == description:
                    print(f"Skipped {player['name']}: embedding is up to date.")
                    skipped_count += 1
                    continue

                embedding = generate_embedding(description)
                pgvector_embedding = embedding_to_pgvector(embedding)

                if existing_embedding:
                    db.execute(
                        text("""
                            UPDATE player_embeddings
                            SET player_name = :player_name,
                                description = :description,
                                embedding = CAST(:embedding AS vector),
                                created_at = CURRENT_TIMESTAMP
                            WHERE id = :id
                        """),
                        {
                            "id": existing_embedding["id"],
                            "player_name": player["name"],
                            "description": description,
                            "embedding": pgvector_embedding,
                        },
                    )
                    updated_count += 1
                    print(f"Updated {player['name']}.")
                else:
                    db.execute(
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
                        """),
                        {
                            "player_id": player["player_id"],
                            "player_name": player["name"],
                            "description": description,
                            "embedding": pgvector_embedding,
                        },
                    )
                    created_count += 1
                    print(f"Stored {player['name']}.")

                db.commit()

            except Exception as error:
                db.rollback()
                failed_count += 1
                print(f"Failed {player_name}: {error}")

        print("\nEmbedding ingestion complete.")
        print(f"Created: {created_count}")
        print(f"Updated: {updated_count}")
        print(f"Skipped: {skipped_count}")
        print(f"Failed: {failed_count}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
