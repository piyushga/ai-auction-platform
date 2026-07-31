from sqlalchemy import text
from app.core.database import engine


try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT NOW();"))

        print("✅ Database connected successfully!")
        print(result.fetchone())

        tables_result = connection.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))

        print("\n📌 Tables in database:")

        for row in tables_result:
            print(row[0])

except Exception as e:
    print("❌ Database connection failed!")
    print(e)