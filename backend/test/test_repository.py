from app.core.database import SessionLocal
from app.repositories.player_repository import PlayerRepository


db = SessionLocal()

try:
    repository = PlayerRepository(db)

    player = repository.get_player_details("Virat Kohli")

    print(player)

finally:
    db.close()