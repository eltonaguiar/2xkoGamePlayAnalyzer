"""Tests for data models."""

import pytest
from datetime import datetime
from analyzer.models import PlayerStats, Match, AnalysisResult


def test_player_stats_creation():
    """Test creating a PlayerStats object."""
    stats = PlayerStats(
        player_name="TestPlayer",
        character="Darius",
        damage_dealt=800,
        damage_taken=400,
        combos_landed=10,
        rounds_won=2
    )
    
    assert stats.player_name == "TestPlayer"
    assert stats.character == "Darius"
    assert stats.damage_dealt == 800
    assert stats.damage_taken == 400
    assert stats.combos_landed == 10
    assert stats.rounds_won == 2


def test_player_stats_defaults():
    """Test PlayerStats default values."""
    stats = PlayerStats(player_name="Player1", character="Ahri")
    
    assert stats.damage_dealt == 0
    assert stats.damage_taken == 0
    assert stats.combos_landed == 0
    assert stats.rounds_won == 0
    assert stats.special_moves_used == 0
    assert stats.blocks_successful == 0


def test_match_creation():
    """Test creating a Match object."""
    player1 = PlayerStats("Alice", "Darius", 850, 420, 12, 2)
    player2 = PlayerStats("Bob", "Ahri", 420, 850, 6, 1)
    
    match = Match(
        match_id="match_001",
        player1=player1,
        player2=player2,
        winner="Alice"
    )
    
    assert match.match_id == "match_001"
    assert match.player1.player_name == "Alice"
    assert match.player2.player_name == "Bob"
    assert match.winner == "Alice"
    assert match.total_rounds == 3


def test_match_get_winner_stats():
    """Test getting winner stats from a match."""
    player1 = PlayerStats("Alice", "Darius", 850, 420, 12, 2)
    player2 = PlayerStats("Bob", "Ahri", 420, 850, 6, 1)
    
    match = Match(
        match_id="match_001",
        player1=player1,
        player2=player2,
        winner="Alice"
    )
    
    winner_stats = match.get_winner_stats()
    assert winner_stats.player_name == "Alice"
    assert winner_stats.character == "Darius"


def test_match_get_loser_stats():
    """Test getting loser stats from a match."""
    player1 = PlayerStats("Alice", "Darius", 850, 420, 12, 2)
    player2 = PlayerStats("Bob", "Ahri", 420, 850, 6, 1)
    
    match = Match(
        match_id="match_001",
        player1=player1,
        player2=player2,
        winner="Alice"
    )
    
    loser_stats = match.get_loser_stats()
    assert loser_stats.player_name == "Bob"
    assert loser_stats.character == "Ahri"


def test_analysis_result_defaults():
    """Test AnalysisResult default values."""
    result = AnalysisResult()
    
    assert result.total_matches == 0
    assert result.total_players == 0
    assert result.character_usage == {}
    assert result.character_win_rates == {}
    assert result.player_win_rates == {}
    assert result.average_damage_per_match == 0.0
    assert result.average_combos_per_match == 0.0
    assert result.most_used_character is None
    assert result.highest_win_rate_character is None
