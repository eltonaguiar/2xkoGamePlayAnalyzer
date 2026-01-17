"""Data models for 2XKO gameplay analysis."""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class PlayerStats:
    """Statistics for a player in a match."""
    player_name: str
    character: str
    damage_dealt: int = 0
    damage_taken: int = 0
    combos_landed: int = 0
    rounds_won: int = 0
    special_moves_used: int = 0
    blocks_successful: int = 0


@dataclass
class Match:
    """Represents a 2XKO match."""
    match_id: str
    player1: PlayerStats
    player2: PlayerStats
    winner: str
    timestamp: datetime = field(default_factory=datetime.now)
    total_rounds: int = 3
    match_duration_seconds: int = 0

    def get_winner_stats(self) -> PlayerStats:
        """Get the stats of the winning player."""
        return self.player1 if self.winner == self.player1.player_name else self.player2

    def get_loser_stats(self) -> PlayerStats:
        """Get the stats of the losing player."""
        return self.player2 if self.winner == self.player1.player_name else self.player1


@dataclass
class AnalysisResult:
    """Results from gameplay analysis."""
    total_matches: int = 0
    total_players: int = 0
    character_usage: dict = field(default_factory=dict)
    character_win_rates: dict = field(default_factory=dict)
    player_win_rates: dict = field(default_factory=dict)
    average_damage_per_match: float = 0.0
    average_combos_per_match: float = 0.0
    most_used_character: Optional[str] = None
    highest_win_rate_character: Optional[str] = None
