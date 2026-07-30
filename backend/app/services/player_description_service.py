class PlayerDescriptionService:

    def generate_description(self, player, special_stats):

        role = player["role"]

        description = (
            f"{player['name']} is a {player['age']}-year-old {role.lower()} "
            f"from {player['country']}. "
            f"He is a {player['batting_style'].lower()} batter and bowls "
            f"{player['bowling_style'].lower()}. "
            f"He currently represents {player['current_ipl_team']} in the Indian Premier League. "
        )

        # -------------------------
        # Role-specific description
        # -------------------------

        if role == "Batsman":

            description += (
                f"He is known for his batting consistency and ability to anchor an innings while "
                f"also accelerating when required. Across his IPL career, he has scored "
                f"{player['ipl_runs']:,} runs in {player['ipl_matches']} matches, including "
                f"{player['ipl_hundreds']} centuries and {player['ipl_fifties']} half-centuries. "
                f"His highest IPL score is {player['ipl_highest_score']}. "
                f"In T20 Internationals, he has accumulated {player['t20_runs']:,} runs, "
                f"making him one of the most dependable batters for his country. "
            )

        elif role == "Bowler":

            description += (
                f"He is recognized for his wicket-taking ability and disciplined bowling. "
                f"Across his IPL career, he has taken {player['ipl_wickets']} wickets in "
                f"{player['ipl_matches']} matches with best bowling figures of "
                f"{player['ipl_best_bowling']}. "
                f"In T20 Internationals, he has claimed {player['t20_wickets']} wickets and "
                f"has consistently been a key bowler in crucial matches. "
            )

        elif role == "All-rounder":

            description += (
                f"He is a genuine all-rounder who contributes with both bat and ball. "
                f"In the IPL, he has scored {player['ipl_runs']:,} runs and taken "
                f"{player['ipl_wickets']} wickets, making him a valuable asset in all phases of the game. "
                f"In T20 Internationals, he has scored {player['t20_runs']:,} runs and "
                f"picked up {player['t20_wickets']} wickets, showcasing his versatility. "
            )

        elif role == "Wicketkeeper":

            description += (
                f"He is a wicketkeeper-batter known for his aggressive batting and reliable work behind the stumps. "
                f"In the IPL, he has scored {player['ipl_runs']:,} runs in "
                f"{player['ipl_matches']} matches while also contributing with "
                f"{player['ipl_catches']} catches. "
                f"In T20 Internationals, he has scored {player['t20_runs']:,} runs and "
                f"continues to play an important role as a wicketkeeper and middle-order batter. "
            )

        # -------------------------
        # Auction
        # -------------------------

        description += (
            f"In the {player['auction_year']} IPL Auction, "
            f"{player['team']} {player['status'].lower()} him "
            f"for ₹{player['sold_price']:,}. "
        )

        # -------------------------
        # Special Achievements
        # -------------------------

        if special_stats:
            description += "Some notable achievements include "

            achievements = []

            for stat in special_stats:
                achievement = stat["stat_name"]

                if stat["stat_value"]:
                    achievement += f" ({stat['stat_value']})"

                if stat["season_year"]:
                    achievement += f" in {stat['season_year']}"

                achievements.append(achievement)

            description += ", ".join(achievements) + "."

        return description