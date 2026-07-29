from sqlalchemy import text
from sqlalchemy.orm import Session


class PlayerRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_player_details(self, player_name: str):

        query = text("""
            SELECT
                p.player_id,
                p.name,
                p.country,
                p.age,
                p.batting_style,
                p.bowling_style,
                p.role,
                p.current_ipl_team,

                ---------------- IPL ----------------

                i.matches           AS ipl_matches,
                i.innings           AS ipl_innings,
                i.runs              AS ipl_runs,
                i.batting_average   AS ipl_batting_average,
                i.strike_rate       AS ipl_strike_rate,
                i.highest_score     AS ipl_highest_score,
                i.fours             AS ipl_fours,
                i.sixes             AS ipl_sixes,
                i.fifties           AS ipl_fifties,
                i.hundreds          AS ipl_hundreds,
                i.wickets           AS ipl_wickets,
                i.bowling_average   AS ipl_bowling_average,
                i.economy           AS ipl_economy,
                i.best_bowling      AS ipl_best_bowling,
                i.five_wicket_hauls AS ipl_five_wicket_hauls,
                i.catches           AS ipl_catches,

                ---------------- T20I ----------------

                t.matches           AS t20_matches,
                t.innings           AS t20_innings,
                t.runs              AS t20_runs,
                t.batting_average   AS t20_batting_average,
                t.strike_rate       AS t20_strike_rate,
                t.highest_score     AS t20_highest_score,
                t.fours             AS t20_fours,
                t.sixes             AS t20_sixes,
                t.fifties           AS t20_fifties,
                t.hundreds          AS t20_hundreds,
                t.wickets           AS t20_wickets,
                t.bowling_average   AS t20_bowling_average,
                t.economy           AS t20_economy,
                t.best_bowling      AS t20_best_bowling,
                t.five_wicket_hauls AS t20_five_wicket_hauls,
                t.catches           AS t20_catches,

                ---------------- Auction ----------------

                a.auction_year,
                a.team,
                a.base_price,
                a.sold_price,
                a.status

            FROM players p

            LEFT JOIN ipl_career_stats i
                ON p.player_id = i.player_id

            LEFT JOIN t20i_records t
                ON p.player_id = t.player_id

            LEFT JOIN auction_history a
                ON p.player_id = a.player_id

            WHERE LOWER(p.name) = LOWER(:player_name)
        """)

        result = self.db.execute(
            query,
            {
                "player_name": player_name
            }
        )

        return result.mappings().first()

    def get_special_stats(self, player_id: int):

        query = text("""
            SELECT
                stat_name,
                stat_value,
                format,
                season_year
            FROM special_stats
            WHERE player_id = :player_id
        """)

        result = self.db.execute(
            query,
            {
                "player_id": player_id
            }
        )

        return result.mappings().all()