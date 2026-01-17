"""Tests for the GameplayAnalyzer."""

import pytest
from analyzer.models import PlayerStats, Match
from analyzer.analyzer import GameplayAnalyzer


@pytest.fixture
def sample_matches():
    """Create sample matches for testing."""
    return [
        Match(
            match_id="match_001",
            player1=PlayerStats("Alice", "Darius", 850, 420, 12, 2),
            player2=PlayerStats("Bob", "Ahri", 420, 850, 6, 1),
            winner="Alice"
        ),
        Match(
            match_id="match_002",
            player1=PlayerStats("Bob", "Yasuo", 920, 380, 15, 2),
            player2=PlayerStats("Charlie", "Ekko", 380, 920, 5, 1),
            winner="Bob"
        ),
        Match(
            match_id="match_003",
            player1=PlayerStats("Alice", "Darius", 780, 520, 10, 2),
            player2=PlayerStats("Charlie", "Ahri", 520, 780, 7, 1),
            winner="Alice"
        ),
    ]


def test_analyzer_initialization():
    """Test analyzer initialization."""
    analyzer = GameplayAnalyzer()
    assert analyzer.matches == []


def test_add_match():
    """Test adding a single match."""
    analyzer = GameplayAnalyzer()
    match = Match(
        match_id="match_001",
        player1=PlayerStats("Alice", "Darius", 850, 420, 12, 2),
        player2=PlayerStats("Bob", "Ahri", 420, 850, 6, 1),
        winner="Alice"
    )
    
    analyzer.add_match(match)
    assert len(analyzer.matches) == 1
    assert analyzer.matches[0].match_id == "match_001"


def test_add_matches(sample_matches):
    """Test adding multiple matches."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    assert len(analyzer.matches) == 3


def test_analyze_empty():
    """Test analysis with no matches."""
    analyzer = GameplayAnalyzer()
    result = analyzer.analyze()
    
    assert result.total_matches == 0
    assert result.total_players == 0


def test_analyze_basic_stats(sample_matches):
    """Test basic analysis statistics."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    result = analyzer.analyze()
    
    assert result.total_matches == 3
    assert result.total_players == 3


def test_analyze_character_usage(sample_matches):
    """Test character usage tracking."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    result = analyzer.analyze()
    
    assert "Darius" in result.character_usage
    assert result.character_usage["Darius"] == 2
    assert "Ahri" in result.character_usage
    assert result.character_usage["Ahri"] == 2


def test_analyze_character_win_rates(sample_matches):
    """Test character win rate calculation."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    result = analyzer.analyze()
    
    assert "Darius" in result.character_win_rates
    assert result.character_win_rates["Darius"] == 100.0  # Won 2 out of 2


def test_analyze_player_win_rates(sample_matches):
    """Test player win rate calculation."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    result = analyzer.analyze()
    
    assert "Alice" in result.player_win_rates
    assert result.player_win_rates["Alice"] == 100.0  # Alice won 2 out of 2


def test_analyze_averages(sample_matches):
    """Test average calculations."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    result = analyzer.analyze()
    
    assert result.average_damage_per_match > 0
    assert result.average_combos_per_match > 0


def test_get_player_stats(sample_matches):
    """Test getting player-specific statistics."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    
    stats = analyzer.get_player_stats("Alice")
    
    assert stats["player_name"] == "Alice"
    assert stats["total_matches"] == 2
    assert stats["wins"] == 2
    assert stats["losses"] == 0
    assert stats["win_rate"] == 100.0
    assert stats["favorite_character"] == "Darius"


def test_get_player_stats_not_found():
    """Test getting stats for non-existent player."""
    analyzer = GameplayAnalyzer()
    stats = analyzer.get_player_stats("NonExistent")
    
    assert stats == {}


def test_get_character_matchup(sample_matches):
    """Test character matchup analysis."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    
    matchup = analyzer.get_character_matchup("Darius", "Ahri")
    
    assert matchup["character1"] == "Darius"
    assert matchup["character2"] == "Ahri"
    assert matchup["total_matches"] == 2
    assert matchup["character1_wins"] == 2


def test_get_character_matchup_not_found():
    """Test matchup for characters that haven't faced each other."""
    analyzer = GameplayAnalyzer()
    matchup = analyzer.get_character_matchup("Darius", "NonExistent")
    
    assert matchup == {}


def test_most_used_character(sample_matches):
    """Test finding the most used character."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    result = analyzer.analyze()
    
    # Both Darius and Ahri are used twice, so it will be one of them
    assert result.most_used_character in ["Darius", "Ahri"]


def test_highest_win_rate_character(sample_matches):
    """Test finding the character with highest win rate."""
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(sample_matches)
    result = analyzer.analyze()
    
    # Darius has 100% win rate (2/2), Yasuo has 100% (1/1)
    assert result.highest_win_rate_character in ["Darius", "Yasuo"]
