from app.services.player_metrics_service import PlayerMetricsService


class PlayerDescriptionService:

    BATTING_ROLES = {"Batter", "WK-Batter", "All-rounder"}
    BOWLING_ROLES = {"Bowler", "All-rounder"}

    def __init__(self):
        self.metrics_service = PlayerMetricsService()

    def generate_description(self, player, special_stats):
        name = player["name"]
        role = player["role"]
        metrics = self.metrics_service.calculate(player)

        sections = [
            (
                f"{name} is a {player['age']}-year-old {role.lower()} "
                f"from {player['country']}."
            ),
            f"Batting style: {player['batting_style']}.",
        ]

        if player["bowling_style"] not in (None, "None", "WK"):
            sections.append(f"Bowling style: {player['bowling_style']}.")

        sections.append(
            f"Current IPL team: {player['current_ipl_team']}."
        )

        if role in self.BATTING_ROLES:
            sections.extend(self._batting_sections(player, name))

        if role in self.BOWLING_ROLES:
            sections.extend(self._bowling_sections(player, name))

        if role == "WK-Batter":
            sections.append(
                f"Wicketkeeping record: {player['ipl_catches']} IPL catches and "
                f"{player['t20_catches']} T20I catches."
            )

        sections.append(
            f"Recorded experience: {metrics['recorded_matches']:.0f} combined "
            f"IPL and T20I match appearances."
        )
        sections.extend(self._metric_sections(role, metrics))

        auction_section = self._auction_section(player, name)
        if auction_section:
            sections.append(auction_section)

        achievements_section = self._achievements_section(special_stats)
        if achievements_section:
            sections.append(achievements_section)

        return " ".join(sections)

    @staticmethod
    def _batting_sections(player, name: str) -> list[str]:
        return [
            (
                f"IPL batting record: {name} has played {player['ipl_matches']} matches "
                f"across {player['ipl_innings']} innings, scoring {player['ipl_runs']:,} runs "
                f"at an average of {player['ipl_batting_average']} and a strike rate of "
                f"{player['ipl_strike_rate']}. The record includes a highest score of "
                f"{player['ipl_highest_score']}, {player['ipl_fifties']} fifties, "
                f"{player['ipl_hundreds']} hundreds, {player['ipl_fours']} fours, and "
                f"{player['ipl_sixes']} sixes."
            ),
            (
                f"T20I batting record: {name} has played {player['t20_matches']} matches "
                f"across {player['t20_innings']} innings, scoring {player['t20_runs']:,} runs "
                f"at an average of {player['t20_batting_average']} and a strike rate of "
                f"{player['t20_strike_rate']}. The record includes a highest score of "
                f"{player['t20_highest_score']}, {player['t20_fifties']} fifties, "
                f"{player['t20_hundreds']} hundreds, {player['t20_fours']} fours, and "
                f"{player['t20_sixes']} sixes."
            ),
        ]

    @staticmethod
    def _bowling_sections(player, name: str) -> list[str]:
        return [
            (
                f"IPL bowling record: {name} has taken {player['ipl_wickets']} wickets "
                f"in {player['ipl_matches']} matches at a bowling average of "
                f"{player['ipl_bowling_average']} and an economy rate of "
                f"{player['ipl_economy']}. Best bowling: {player['ipl_best_bowling']}; "
                f"five-wicket hauls: {player['ipl_five_wicket_hauls']}."
            ),
            (
                f"T20I bowling record: {name} has taken {player['t20_wickets']} wickets "
                f"in {player['t20_matches']} matches at a bowling average of "
                f"{player['t20_bowling_average']} and an economy rate of "
                f"{player['t20_economy']}. Best bowling: {player['t20_best_bowling']}; "
                f"five-wicket hauls: {player['t20_five_wicket_hauls']}."
            ),
        ]

    @staticmethod
    def _metric_sections(role: str, metrics: dict) -> list[str]:
        sections = []

        if role in PlayerDescriptionService.BATTING_ROLES:
            sections.append(
                "Calculated batting indicators: fifty-plus scores occurred in "
                f"{metrics['ipl_fifty_plus_rate']}% of IPL innings and "
                f"{metrics['t20_fifty_plus_rate']}% of T20I innings."
            )

            if metrics["ipl_runs_per_crore"] is not None:
                sections.append(
                    "Auction-price indicator: the recorded IPL career output is "
                    f"{metrics['ipl_runs_per_crore']} runs per ₹1 crore of sold price."
                )

        if role in PlayerDescriptionService.BOWLING_ROLES:
            sections.append(
                "Calculated bowling indicators: "
                f"{metrics['ipl_wickets_per_match']} wickets per IPL match and "
                f"{metrics['t20_wickets_per_match']} wickets per T20I match."
            )

            if metrics["ipl_wickets_per_crore"] is not None:
                sections.append(
                    "Auction-price indicator: the recorded IPL career output is "
                    f"{metrics['ipl_wickets_per_crore']} wickets per ₹1 crore of sold price."
                )

        return sections

    @staticmethod
    def _auction_section(player, name: str) -> str | None:
        if player["auction_year"] is None:
            return None

        status = player["status"].lower()

        if status == "unsold":
            return (
                f"In the {player['auction_year']} IPL auction, {name} was unsold "
                f"at a base price of ₹{player['base_price']:,}."
            )

        if status == "retained":
            return (
                f"In the {player['auction_year']} IPL auction data, "
                f"{player['team']} retained {name} for ₹{player['sold_price']:,}."
            )

        return (
            f"In the {player['auction_year']} IPL auction, {name} was sold to "
            f"{player['team']} for ₹{player['sold_price']:,}."
        )

    @staticmethod
    def _achievements_section(special_stats) -> str | None:
        if not special_stats:
            return None

        achievements = []

        for stat in special_stats:
            achievement = stat["stat_name"]

            if stat["stat_value"]:
                achievement += f" ({stat['stat_value']})"

            if stat["format"]:
                achievement += f" in {stat['format']}"

            if stat["season_year"]:
                achievement += f" during {stat['season_year']}"

            achievements.append(achievement)

        return (
            "His database-recorded achievements include "
            + "; ".join(achievements)
            + "."
        )
