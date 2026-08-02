from app.core.database import SessionLocal
from app.services.query_processing_service import QueryProcessingService


QUESTION = "comare vrat kehli and ruhit sherma"


def main():
    db = SessionLocal()

    try:
        parsed_query = QueryProcessingService(db).parse(QUESTION)

        print(f"\nORIGINAL QUESTION: {parsed_query.original_text}")
        print(f"NORMALIZED TEXT: {parsed_query.normalized_text}")
        print(f"MATCHED PLAYERS: {parsed_query.player_names}")
        print(f"CORRECTIONS: {parsed_query.corrections}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
