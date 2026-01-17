"""Core analysis functions for 2XKO gameplay data."""

from typing import List, Dict
from collections import defaultdict
from analyzer.models import Match, AnalysisResult


class GameplayAnalyzer:
    """Analyzer for 2XKO gameplay statistics."""

    def __init__(self):
        self.matches: List[Match] = []

    def add_match(self, match: Match) -> None:
        """Add a match to the analyzer."""
        self.matches.append(match)

    def add_matches(self, matches: List[Match]) -> None:
        """Add multiple matches to the analyzer."""
        self.matches.extend(matches)

    def analyze(self) -> AnalysisResult:
        """Perform comprehensive analysis on all matches."""
        if not self.matches:
            return AnalysisResult()

        result = AnalysisResult()
        result.total_matches = len(self.matches)

        # Track statistics
        character_usage = defaultdict(int)
        character_wins = defaultdict(int)
        character_matches = defaultdict(int)
        player_wins = defaultdict(int)
        player_matches = defaultdict(int)
        players_set = set()
        total_damage = 0
        total_combos = 0

        for match in self.matches:
            # Player 1 stats
            players_set.add(match.player1.player_name)
            character_usage[match.player1.character] += 1
            character_matches[match.player1.character] += 1
            player_matches[match.player1.player_name] += 1
            total_damage += match.player1.damage_dealt
            total_combos += match.player1.combos_landed

            # Player 2 stats
            players_set.add(match.player2.player_name)
            character_usage[match.player2.character] += 1
            character_matches[match.player2.character] += 1
            player_matches[match.player2.player_name] += 1
            total_damage += match.player2.damage_dealt
            total_combos += match.player2.combos_landed

            # Winner stats
            winner_stats = match.get_winner_stats()
            character_wins[winner_stats.character] += 1
            player_wins[match.winner] += 1

        result.total_players = len(players_set)
        result.character_usage = dict(character_usage)

        # Calculate win rates
        result.character_win_rates = {
            char: (character_wins[char] / character_matches[char] * 100)
            for char in character_matches
        }

        result.player_win_rates = {
            player: (player_wins[player] / player_matches[player] * 100)
            for player in player_matches
        }

        # Calculate averages
        result.average_damage_per_match = total_damage / result.total_matches
        result.average_combos_per_match = total_combos / result.total_matches

        # Find most used character
        if character_usage:
            result.most_used_character = max(character_usage, key=character_usage.get)

        # Find highest win rate character
        if result.character_win_rates:
            result.highest_win_rate_character = max(
                result.character_win_rates, key=result.character_win_rates.get
            )

        return result

    def get_player_stats(self, player_name: str) -> Dict:
        """Get detailed statistics for a specific player."""
        player_matches = [
            m for m in self.matches
            if m.player1.player_name == player_name or m.player2.player_name == player_name
        ]

        if not player_matches:
            return {}

        wins = sum(1 for m in player_matches if m.winner == player_name)
        total_matches = len(player_matches)
        win_rate = (wins / total_matches * 100) if total_matches > 0 else 0

        total_damage_dealt = 0
        total_damage_taken = 0
        total_combos = 0
        characters_used = defaultdict(int)

        for match in player_matches:
            if match.player1.player_name == player_name:
                stats = match.player1
            else:
                stats = match.player2

            total_damage_dealt += stats.damage_dealt
            total_damage_taken += stats.damage_taken
            total_combos += stats.combos_landed
            characters_used[stats.character] += 1

        return {
            "player_name": player_name,
            "total_matches": total_matches,
            "wins": wins,
            "losses": total_matches - wins,
            "win_rate": win_rate,
            "total_damage_dealt": total_damage_dealt,
            "total_damage_taken": total_damage_taken,
            "average_damage_dealt": total_damage_dealt / total_matches,
            "average_damage_taken": total_damage_taken / total_matches,
            "total_combos": total_combos,
            "average_combos": total_combos / total_matches,
            "characters_used": dict(characters_used),
            "favorite_character": max(characters_used, key=characters_used.get) if characters_used else None
        }

    def get_character_matchup(self, char1: str, char2: str) -> Dict:
        """Analyze matchup between two characters."""
        matchup_matches = [
            m for m in self.matches
            if (m.player1.character == char1 and m.player2.character == char2) or
               (m.player1.character == char2 and m.player2.character == char1)
        ]

        if not matchup_matches:
            return {}

        char1_wins = sum(
            1 for m in matchup_matches
            if (m.player1.character == char1 and m.winner == m.player1.player_name) or
               (m.player2.character == char1 and m.winner == m.player2.player_name)
        )

        total_matches = len(matchup_matches)

        return {
            "character1": char1,
            "character2": char2,
            "total_matches": total_matches,
            "character1_wins": char1_wins,
            "character2_wins": total_matches - char1_wins,
            "character1_win_rate": (char1_wins / total_matches * 100) if total_matches > 0 else 0,
            "character2_win_rate": ((total_matches - char1_wins) / total_matches * 100) if total_matches > 0 else 0
        }
