from sqlalchemy import text
from sqlalchemy.orm import Session


class PlayerRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_player_details(self, player_name: str):
        query = text("""
            SELECT
                p.*,
                i.matches AS ipl_matches,
                i.runs AS ipl_runs,
                i.wickets AS ipl_wickets,
                i.highest_score,
                i.strike_rate,
                i.economy,

                t.matches AS t20i_matches,
                t.runs AS t20i_runs,
                t.wickets AS t20i_wickets,

                a.team,
                a.price_crore,

                s.orange_caps,
                s.purple_caps,
                s.player_of_the_match_awards

            FROM players p

            LEFT JOIN ipl_career_stats i
                ON p.player_id = i.player_id

            LEFT JOIN t20i_records t
                ON p.player_id = t.player_id

            LEFT JOIN auction_history a
                ON p.player_id = a.player_id

            LEFT JOIN special_stats s
                ON p.player_id = s.player_id

            WHERE LOWER(p.name) = LOWER(:player_name)
        """)

        result = self.db.execute(
            query,
            {"player_name": player_name}
        )

        return result.mappings().first()