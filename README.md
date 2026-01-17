# 2XKO Gameplay Analyzer

A Python-based gameplay analyzer for 2XKO (formerly Project L) fighting game. This tool helps track, analyze, and visualize gameplay statistics including character usage, win rates, player performance, and matchup data.

## Features

- 📊 **Match Tracking**: Record detailed match statistics including damage, combos, and round outcomes
- 🎮 **Player Analytics**: Track individual player performance, win rates, and character preferences
- ⚔️ **Character Statistics**: Analyze character usage, win rates, and matchup data
- 📈 **Comprehensive Analysis**: Calculate averages, trends, and identify top performers
- 🖥️ **CLI Interface**: Easy-to-use command-line tool with sample data

## Installation

### Using pip (recommended)

```bash
pip install -e .
```

### For development

```bash
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

Run the analyzer with sample data:

```bash
python -m analyzer.cli
```

Or use the installed command:

```bash
2xko-analyzer
```

Load match data from a JSON file:

```bash
2xko-analyzer matches.json
```

### As a Python Library

```python
from analyzer.models import Match, PlayerStats
from analyzer.analyzer import GameplayAnalyzer

# Create match data
player1 = PlayerStats("Alice", "Darius", 850, 420, 12, 2)
player2 = PlayerStats("Bob", "Ahri", 420, 850, 6, 1)

match = Match(
    match_id="match_001",
    player1=player1,
    player2=player2,
    winner="Alice"
)

# Analyze matches
analyzer = GameplayAnalyzer()
analyzer.add_match(match)
result = analyzer.analyze()

print(f"Total matches: {result.total_matches}")
print(f"Most used character: {result.most_used_character}")

# Get player-specific stats
player_stats = analyzer.get_player_stats("Alice")
print(f"Win rate: {player_stats['win_rate']:.1f}%")

# Get character matchup data
matchup = analyzer.get_character_matchup("Darius", "Ahri")
print(f"Matchup win rate: {matchup['character1_win_rate']:.1f}%")
```

## Match Data Format

The analyzer accepts match data in JSON format:

```json
[
  {
    "match_id": "match_001",
    "player1": {
      "player_name": "Alice",
      "character": "Darius",
      "damage_dealt": 850,
      "damage_taken": 420,
      "combos_landed": 12,
      "rounds_won": 2,
      "special_moves_used": 8,
      "blocks_successful": 15
    },
    "player2": {
      "player_name": "Bob",
      "character": "Ahri",
      "damage_dealt": 420,
      "damage_taken": 850,
      "combos_landed": 6,
      "rounds_won": 1,
      "special_moves_used": 5,
      "blocks_successful": 10
    },
    "winner": "Alice",
    "timestamp": "2026-01-17T12:00:00",
    "total_rounds": 3,
    "match_duration_seconds": 180
  }
]
```

## Statistics Provided

### Overall Analysis
- Total matches and players
- Character usage counts
- Character win rates
- Player win rates
- Average damage per match
- Average combos per match
- Most used character
- Highest win rate character

### Player-Specific Analysis
- Total matches played
- Wins and losses
- Win rate percentage
- Total and average damage dealt/taken
- Total and average combos
- Characters used and favorite character

### Matchup Analysis
- Head-to-head statistics between two characters
- Win rates for each character in the matchup
- Total matches in the matchup

## Development

### Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=analyzer --cov-report=html
```

### Project Structure

```
2xkoGamePlayAnalyzer/
├── analyzer/
│   ├── __init__.py
│   ├── models.py       # Data models
│   ├── analyzer.py     # Analysis logic
│   └── cli.py          # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_analyzer.py
├── setup.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This is an unofficial fan-made tool and is not affiliated with Riot Games or the official 2XKO game.
