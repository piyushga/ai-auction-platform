class PlayerMetricsService:

    CRORE = 10_000_000

    def calculate(self, player) -> dict:
        sold_price = self._number(player, "sold_price")
        price_in_crore = sold_price / self.CRORE if sold_price > 0 else None

        return {
            "recorded_matches": (
                self._number(player, "ipl_matches")
                + self._number(player, "t20_matches")
            ),
            "ipl_fifty_plus_rate": self._percentage(
                self._number(player, "ipl_fifties")
                + self._number(player, "ipl_hundreds"),
                self._number(player, "ipl_innings"),
            ),
            "t20_fifty_plus_rate": self._percentage(
                self._number(player, "t20_fifties")
                + self._number(player, "t20_hundreds"),
                self._number(player, "t20_innings"),
            ),
            "ipl_wickets_per_match": self._rate(
                self._number(player, "ipl_wickets"),
                self._number(player, "ipl_matches"),
            ),
            "t20_wickets_per_match": self._rate(
                self._number(player, "t20_wickets"),
                self._number(player, "t20_matches"),
            ),
            "ipl_runs_per_crore": self._per_crore(
                self._number(player, "ipl_runs"),
                price_in_crore,
            ),
            "ipl_wickets_per_crore": self._per_crore(
                self._number(player, "ipl_wickets"),
                price_in_crore,
            ),
        }

    @staticmethod
    def _number(player, key: str) -> float:
        value = player.get(key)
        return float(value) if value is not None else 0.0

    @staticmethod
    def _percentage(numerator: float, denominator: float) -> float:
        if denominator <= 0:
            return 0.0

        return round((numerator / denominator) * 100, 1)

    @staticmethod
    def _rate(numerator: float, denominator: float) -> float:
        if denominator <= 0:
            return 0.0

        return round(numerator / denominator, 2)

    @staticmethod
    def _per_crore(output: float, price_in_crore: float | None) -> float | None:
        if price_in_crore is None or price_in_crore <= 0:
            return None

        return round(output / price_in_crore, 1)
