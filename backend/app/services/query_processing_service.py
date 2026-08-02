import re
import unicodedata
from dataclasses import dataclass, field

from rapidfuzz import fuzz, process
from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class ParsedPlayerQuery:
    original_text: str
    normalized_text: str
    player_names: list[str] = field(default_factory=list)
    country: str | None = None
    role: str | None = None
    team: str | None = None
    max_price: int | None = None
    corrections: dict[str, str] = field(default_factory=dict)


class QueryProcessingService:

    ROLE_ALIASES = {
        "Batter": {
            "batter",
            "batters",
            "batsman",
            "batsmen",
            "batting",
            "batting specialist",
        },
        "Bowler": {
            "bowler",
            "bowlers",
            "bowling",
            "bowling specialist",
        },
        "WK-Batter": {
            "wk batter",
            "wicketkeeper batter",
            "wicket keeper batter",
            "wicketkeeper",
            "wicket keeper",
            "keeper",
        },
        "All-rounder": {
            "all rounder",
            "all rounders",
            "allrounder",
            "allrounders",
        },
    }

    PRICE_UNITS = {
        "crore": 10_000_000,
        "lakh": 100_000,
        "million": 1_000_000,
    }

    def __init__(self, db: Session):
        self.db = db

    def parse(self, user_text: str) -> ParsedPlayerQuery:
        normalized_text = self.normalize(user_text)

        if not normalized_text:
            raise ValueError("Question cannot be empty.")

        player_names = self._database_values("name")
        countries = self._database_values("country")
        teams = self._database_values("current_ipl_team")
        corrections = {}

        matched_players = self._find_fuzzy_phrases(
            normalized_text,
            player_names,
            cutoff=80,
            max_matches=5,
        )
        for typed_value, canonical_value in matched_players:
            if self.normalize(typed_value) != self.normalize(canonical_value):
                corrections[typed_value] = canonical_value

        country_match = self._find_fuzzy_phrases(
            normalized_text,
            countries,
            cutoff=85,
            max_matches=1,
            scorer=fuzz.partial_ratio,
        )
        team_match = self._find_fuzzy_phrases(
            normalized_text,
            teams,
            cutoff=86,
            max_matches=1,
        )
        role, role_correction = self._extract_role(normalized_text)

        if country_match:
            typed_country, country = country_match[0]
            if self.normalize(typed_country) != self.normalize(country):
                corrections[typed_country] = country
        else:
            country = None

        if team_match:
            typed_team, team = team_match[0]
            if self.normalize(typed_team) != self.normalize(team):
                corrections[typed_team] = team
        else:
            team = None

        if role_correction:
            corrections[role_correction[0]] = role_correction[1]

        max_price, price_correction = self._extract_max_price(normalized_text)
        if price_correction:
            corrections[price_correction[0]] = price_correction[1]

        return ParsedPlayerQuery(
            original_text=user_text,
            normalized_text=normalized_text,
            player_names=[match[1] for match in matched_players],
            country=country,
            role=role,
            team=team,
            max_price=max_price,
            corrections=corrections,
        )

    @staticmethod
    def normalize(value: str) -> str:
        value = unicodedata.normalize("NFKC", value).casefold()
        value = value.replace("-", " ")
        value = re.sub(r"[^\w\s.₹]", " ", value)
        return re.sub(r"\s+", " ", value).strip()

    def _database_values(self, column: str) -> list[str]:
        allowed_columns = {"name", "country", "current_ipl_team"}

        if column not in allowed_columns:
            raise ValueError("Unsupported query-processing column.")

        result = self.db.execute(
            text(
                f"SELECT DISTINCT {column} FROM players "
                f"WHERE {column} IS NOT NULL ORDER BY {column}"
            )
        ).scalars().all()

        return list(result)

    def _extract_role(self, normalized_text: str) -> tuple[str | None, tuple | None]:
        alias_to_role = {
            alias: role
            for role, aliases in self.ROLE_ALIASES.items()
            for alias in aliases
        }

        for alias in sorted(alias_to_role, key=len, reverse=True):
            if re.search(rf"\b{re.escape(alias)}\b", normalized_text):
                return alias_to_role[alias], None

        matches = self._find_fuzzy_phrases(
            normalized_text,
            list(alias_to_role),
            cutoff=80,
            max_matches=1,
        )

        if not matches:
            return None, None

        typed_alias, matched_alias = matches[0]
        return alias_to_role[matched_alias], (typed_alias, alias_to_role[matched_alias])

    def _extract_max_price(
        self,
        normalized_text: str,
    ) -> tuple[int | None, tuple | None]:
        price_match = re.search(
            r"\b(?:under|below|within|max|maximum|less than)\s*"
            r"(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*([a-z]+)?\b",
            normalized_text,
        )

        if not price_match:
            return None, None

        amount = float(price_match.group(1))
        typed_unit = price_match.group(2)

        if typed_unit is None:
            return int(amount), None

        unit_match = process.extractOne(
            typed_unit,
            list(self.PRICE_UNITS),
            scorer=fuzz.ratio,
            score_cutoff=75,
        )

        if unit_match is None:
            return None, None

        canonical_unit = unit_match[0]
        correction = None

        if typed_unit != canonical_unit:
            correction = (typed_unit, canonical_unit)

        return int(amount * self.PRICE_UNITS[canonical_unit]), correction

    def _find_fuzzy_phrases(
        self,
        normalized_text: str,
        canonical_values: list[str],
        cutoff: int,
        max_matches: int,
        scorer=fuzz.ratio,
    ) -> list[tuple[str, str]]:
        if not canonical_values:
            return []

        tokens = normalized_text.split()
        normalized_to_canonical = {
            self.normalize(value): value for value in canonical_values
        }
        normalized_choices = list(normalized_to_canonical)
        word_counts = [len(choice.split()) for choice in normalized_choices]
        minimum_words = min(word_counts)
        maximum_words = max(word_counts)
        candidates = []

        for size in range(minimum_words, maximum_words + 1):
            for start in range(0, len(tokens) - size + 1):
                end = start + size
                typed_phrase = " ".join(tokens[start:end])
                match = process.extractOne(
                    typed_phrase,
                    normalized_choices,
                    scorer=scorer,
                    score_cutoff=cutoff,
                )

                if match is not None:
                    matched_value, score, _ = match
                    candidates.append(
                        (
                            score,
                            start,
                            end,
                            typed_phrase,
                            normalized_to_canonical[matched_value],
                        )
                    )

        selected = []
        occupied_positions = set()
        selected_values = set()

        for score, start, end, typed_phrase, canonical_value in sorted(
            candidates,
            key=lambda candidate: (candidate[0], candidate[2] - candidate[1]),
            reverse=True,
        ):
            positions = set(range(start, end))

            if positions & occupied_positions or canonical_value in selected_values:
                continue

            selected.append((typed_phrase, canonical_value))
            occupied_positions.update(positions)
            selected_values.add(canonical_value)

            if len(selected) == max_matches:
                break

        return selected
