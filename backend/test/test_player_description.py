from app.core.database import SessionLocal
from app.repositories.player_repository import PlayerRepository
from app.services.player_description_service import PlayerDescriptionService


def main():

    db = SessionLocal()

    try:
        repository = PlayerRepository(db)

        # Change the player name to test different players
        player = repository.get_player_details("Hardik Pandya")

        if player is None:
            print("Player not found!")
            return

        special_stats = repository.get_special_stats(player["player_id"])

        description_service = PlayerDescriptionService()

        description = description_service.generate_description(
            player,
            special_stats
        )

        print("\n" + "=" * 80)
        print("PLAYER DESCRIPTION")
        print("=" * 80)
        print(description)
        print("=" * 80)

    finally:
        db.close()


if __name__ == "__main__":
    main()