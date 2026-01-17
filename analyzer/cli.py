"""Command-line interface for 2XKO Gameplay Analyzer."""

import json
import sys
from datetime import datetime
from analyzer.models import Match, PlayerStats
from analyzer.analyzer import GameplayAnalyzer


def print_analysis_results(result):
    """Pretty print analysis results."""
    print("\n" + "=" * 60)
    print("2XKO GAMEPLAY ANALYSIS RESULTS")
    print("=" * 60)
    print(f"\nTotal Matches Analyzed: {result.total_matches}")
    print(f"Total Players: {result.total_players}")
    
    print("\n--- CHARACTER STATISTICS ---")
    print(f"Most Used Character: {result.most_used_character}")
    print(f"Highest Win Rate Character: {result.highest_win_rate_character}")
    
    print("\nCharacter Usage:")
    for char, count in sorted(result.character_usage.items(), key=lambda x: x[1], reverse=True):
        print(f"  {char}: {count} times")
    
    print("\nCharacter Win Rates:")
    for char, rate in sorted(result.character_win_rates.items(), key=lambda x: x[1], reverse=True):
        print(f"  {char}: {rate:.1f}%")
    
    print("\n--- PLAYER STATISTICS ---")
    print("Player Win Rates:")
    for player, rate in sorted(result.player_win_rates.items(), key=lambda x: x[1], reverse=True):
        print(f"  {player}: {rate:.1f}%")
    
    print("\n--- GAMEPLAY METRICS ---")
    print(f"Average Damage per Match: {result.average_damage_per_match:.1f}")
    print(f"Average Combos per Match: {result.average_combos_per_match:.1f}")
    print("=" * 60 + "\n")


def print_player_stats(stats):
    """Pretty print player statistics."""
    if not stats:
        print("No data found for this player.")
        return
    
    print("\n" + "=" * 60)
    print(f"PLAYER STATISTICS: {stats['player_name']}")
    print("=" * 60)
    print(f"\nTotal Matches: {stats['total_matches']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Win Rate: {stats['win_rate']:.1f}%")
    print(f"\nTotal Damage Dealt: {stats['total_damage_dealt']}")
    print(f"Total Damage Taken: {stats['total_damage_taken']}")
    print(f"Average Damage Dealt: {stats['average_damage_dealt']:.1f}")
    print(f"Average Damage Taken: {stats['average_damage_taken']:.1f}")
    print(f"\nTotal Combos: {stats['total_combos']}")
    print(f"Average Combos per Match: {stats['average_combos']:.1f}")
    print(f"\nFavorite Character: {stats['favorite_character']}")
    print("\nCharacters Used:")
    for char, count in sorted(stats['characters_used'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {char}: {count} times")
    print("=" * 60 + "\n")


def load_matches_from_json(file_path):
    """Load match data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        matches = []
        for match_data in data:
            player1 = PlayerStats(**match_data['player1'])
            player2 = PlayerStats(**match_data['player2'])
            
            match = Match(
                match_id=match_data['match_id'],
                player1=player1,
                player2=player2,
                winner=match_data['winner'],
                timestamp=datetime.fromisoformat(match_data.get('timestamp', datetime.now().isoformat())),
                total_rounds=match_data.get('total_rounds', 3),
                match_duration_seconds=match_data.get('match_duration_seconds', 0)
            )
            matches.append(match)
        
        return matches
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file_path}'.")
        return None
    except Exception as e:
        print(f"Error loading matches: {e}")
        return None


def create_sample_data():
    """Create sample match data for demonstration."""
    matches = [
        Match(
            match_id="match_001",
            player1=PlayerStats("Alice", "Darius", 850, 420, 12, 2, 8, 15),
            player2=PlayerStats("Bob", "Ahri", 420, 850, 6, 1, 5, 10),
            winner="Alice",
            total_rounds=3,
            match_duration_seconds=180
        ),
        Match(
            match_id="match_002",
            player1=PlayerStats("Bob", "Yasuo", 920, 380, 15, 2, 10, 12),
            player2=PlayerStats("Charlie", "Ekko", 380, 920, 5, 1, 4, 8),
            winner="Bob",
            total_rounds=3,
            match_duration_seconds=165
        ),
        Match(
            match_id="match_003",
            player1=PlayerStats("Alice", "Darius", 780, 520, 10, 2, 7, 14),
            player2=PlayerStats("Charlie", "Ahri", 520, 780, 7, 1, 6, 11),
            winner="Alice",
            total_rounds=3,
            match_duration_seconds=195
        ),
        Match(
            match_id="match_004",
            player1=PlayerStats("Charlie", "Ekko", 900, 450, 14, 2, 9, 13),
            player2=PlayerStats("Alice", "Yasuo", 450, 900, 8, 1, 5, 9),
            winner="Charlie",
            total_rounds=3,
            match_duration_seconds=172
        ),
        Match(
            match_id="match_005",
            player1=PlayerStats("Bob", "Ahri", 650, 600, 9, 2, 7, 11),
            player2=PlayerStats("Alice", "Darius", 600, 650, 8, 1, 6, 10),
            winner="Bob",
            total_rounds=3,
            match_duration_seconds=188
        ),
    ]
    return matches


def main():
    """Main CLI entry point."""
    print("2XKO Gameplay Analyzer v0.1.0")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Loading matches from: {file_path}")
        matches = load_matches_from_json(file_path)
        if matches is None:
            return
    else:
        print("No input file provided. Using sample data for demonstration.")
        print("Usage: 2xko-analyzer <json_file>")
        print()
        matches = create_sample_data()
    
    analyzer = GameplayAnalyzer()
    analyzer.add_matches(matches)
    
    # Perform overall analysis
    result = analyzer.analyze()
    print_analysis_results(result)
    
    # Show player-specific stats if there are players
    if result.total_players > 0:
        print("\n--- DETAILED PLAYER ANALYSIS ---")
        players = set()
        for match in matches:
            players.add(match.player1.player_name)
            players.add(match.player2.player_name)
        
        for player in sorted(players):
            stats = analyzer.get_player_stats(player)
            print_player_stats(stats)
    
    print("Analysis complete!")


if __name__ == "__main__":
    main()
