# Quick Start Guide

## Installation

```bash
pip install -e .
```

## Basic Usage

### Run with sample data
```bash
2xko-analyzer
```

### Run with your own data
```bash
2xko-analyzer your_matches.json
```

## Creating Match Data

Create a JSON file with the following structure:

```json
[
  {
    "match_id": "unique_id",
    "player1": {
      "player_name": "Player Name",
      "character": "Character Name",
      "damage_dealt": 850,
      "damage_taken": 420,
      "combos_landed": 12,
      "rounds_won": 2,
      "special_moves_used": 8,
      "blocks_successful": 15
    },
    "player2": {
      "player_name": "Opponent Name",
      "character": "Opponent Character",
      "damage_dealt": 420,
      "damage_taken": 850,
      "combos_landed": 6,
      "rounds_won": 1,
      "special_moves_used": 5,
      "blocks_successful": 10
    },
    "winner": "Player Name",
    "timestamp": "2026-01-17T12:00:00",
    "total_rounds": 3,
    "match_duration_seconds": 180
  }
]
```

## Using as a Library

```python
from analyzer.models import Match, PlayerStats
from analyzer.analyzer import GameplayAnalyzer

# Create a match
player1 = PlayerStats("Alice", "Darius", 850, 420, 12, 2)
player2 = PlayerStats("Bob", "Ahri", 420, 850, 6, 1)
match = Match("match_001", player1, player2, "Alice")

# Analyze
analyzer = GameplayAnalyzer()
analyzer.add_match(match)
result = analyzer.analyze()

# View results
print(f"Most used character: {result.most_used_character}")
print(f"Average damage: {result.average_damage_per_match}")
```

## Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=analyzer
```
