from app.core.database import SessionLocal
from app.repositories.player_repository import PlayerRepository


db = SessionLocal()

try:

    repository = PlayerRepository(db)

    player = repository.get_player_details("Virat Kohli")

    print("\n===== PLAYER DETAILS =====\n")
    print(player)

    print("\n===== SPECIAL STATS =====\n")

    special_stats = repository.get_special_stats(player["player_id"])

    for stat in special_stats:
        print(stat)

finally:
    db.close()