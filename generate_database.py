"""
Generate complete character database JSON for web interface.
"""

import json
import sys
from character_data import CHARACTER_DATA
from character_comparison import CharacterComparison


def generate_character_database():
    """Generate complete database with all character data"""
    
    comparison = CharacterComparison(CHARACTER_DATA)
    
    database = {
        "characters": {},
        "comparison": {
            "stats": comparison.get_all_character_stats(),
            "fastest_moves": comparison.compare_fastest_moves(),
            "fastest_moves_in_game": comparison.get_fastest_moves_in_game(limit=50),  # Top 50 fastest moves across all characters (includes more poke moves)
            "safest_moves": comparison.compare_safest_moves(),
            "assist_dependent": comparison.compare_assist_dependent_moves(),
            "bnb_combos": comparison.compare_bnb_combos()
        }
    }
    
    # Add detailed data for each character
    for char_name in CHARACTER_DATA.keys():
        char_class = CHARACTER_DATA[char_name]
        summary = comparison.get_character_summary(char_name)
        
        # Convert moves dict to array format for easier HTML consumption
        moves_array = []
        for move_input, move_data in summary["moves"].items():
            moves_array.append({
                "move": move_input,
                "character": char_name,
                **move_data
            })
        
        # Add data quality indicator
        is_verified = char_name in ["Blitzcrank"]  # Characters with real wiki data
        has_placeholder = any("standing light attack" in m.get("description", "").lower() 
                             or "primary special move" in m.get("description", "").lower() 
                             for m in moves_array)
        
        database["characters"][char_name] = {
            **summary,
            "moves": moves_array,  # Array format for HTML
            "data_quality": {
                "is_verified": is_verified,
                "has_placeholder": has_placeholder,
                "status": "verified" if is_verified else ("placeholder" if has_placeholder else "unknown")
            }
        }
    
    return database


def save_database(filename="output/character_database.json"):
    """Save database to JSON file"""
    try:
        database = generate_character_database()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2)
        
        print(f"[OK] Character database saved to: {filename}")
        print(f"Total characters: {len(database['characters'])}")
        
        # Print summary
        for char_name, char_data in database['characters'].items():
            moves_count = len(char_data['moves'])
            combos_count = len(char_data['bnb_combos'])
            print(f"  - {char_name}: {moves_count} moves, {combos_count} combos")
        
        return database
        
    except Exception as e:
        print(f"[ERROR] Error generating database: {e}")
        import traceback
        traceback.print_exc()
        return None


def print_comparison_stats(database):
    """Print interesting comparison statistics"""
    print("\n" + "="*60)
    print("CHARACTER COMPARISON STATISTICS")
    print("="*60)
    
    # Fastest move overall
    print("\n[FASTEST] FASTEST MOVES ACROSS ALL CHARACTERS:")
    all_fastest = []
    for char, moves in database['comparison']['fastest_moves'].items():
        if moves:
            move = moves[0]
            all_fastest.append((char, move['move'], move['startup']))
    
    all_fastest.sort(key=lambda x: x[2])
    for char, move, startup in all_fastest[:5]:
        print(f"  {char}: {move} ({startup}f)")
    
    # Safest move overall
    print("\n[SAFEST] SAFEST MOVES ACROSS ALL CHARACTERS:")
    all_safest = []
    for char, moves in database['comparison']['safest_moves'].items():
        if moves:
            move = moves[0]
            all_safest.append((char, move['move'], move['on_block']))
    
    all_safest.sort(key=lambda x: x[2], reverse=True)
    for char, move, on_block in all_safest[:5]:
        print(f"  {char}: {move} ({on_block:+d} on block)")
    
    # Characters with most assist-dependent moves
    print("\n[ASSIST] MOST ASSIST-DEPENDENT CHARACTERS:")
    assist_counts = []
    for char, moves in database['comparison']['assist_dependent'].items():
        assist_counts.append((char, len(moves)))
    
    assist_counts.sort(key=lambda x: x[1], reverse=True)
    for char, count in assist_counts:
        if count > 0:
            print(f"  {char}: {count} moves require assist/setup")
    
    # Health rankings
    print("\n[HEALTH] HEALTH RANKINGS:")
    health_ranks = [(c['name'], c['health']) for c in database['comparison']['stats']]
    health_ranks.sort(key=lambda x: x[1], reverse=True)
    for char, health in health_ranks:
        print(f"  {char}: {health} HP")


if __name__ == "__main__":
    print("Generating 2XKO Character Database...")
    print()
    
    database = save_database()
    
    if database:
        print_comparison_stats(database)
        
        print("\n" + "="*60)
        print("[OK] DATABASE GENERATION COMPLETE!")
        print("="*60)
        print("\nNext steps:")
        print("1. Open output/character_database.html in your browser")
        print("2. The interface will load data from character_database.json")
        print("3. Compare characters, moves, and combos!")
