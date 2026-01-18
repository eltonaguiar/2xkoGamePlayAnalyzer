"""
Comprehensive verification script to ensure all pages work correctly
with all characters in the database.
"""

import json
import os
import sys
from generate_database import generate_character_database
from character_data import CHARACTER_DATA


def verify_database_structure():
    """Verify database has correct structure"""
    print("="*70)
    print("VERIFYING DATABASE STRUCTURE")
    print("="*70)
    
    database = generate_character_database()
    
    issues = []
    
    # Check top-level structure
    if "characters" not in database:
        issues.append("Missing 'characters' key in database")
    if "comparison" not in database:
        issues.append("Missing 'comparison' key in database")
    
    # Check comparison structure
    if "comparison" in database:
        required_comparison_keys = ["stats", "fastest_moves", "safest_moves", "assist_dependent", "bnb_combos"]
        for key in required_comparison_keys:
            if key not in database["comparison"]:
                issues.append(f"Missing '{key}' in comparison data")
    
    # Check each character
    if "characters" in database:
        for char_name, char_data in database["characters"].items():
            # Check required character fields
            required_fields = ["info", "moves", "bnb_combos"]
            for field in required_fields:
                if field not in char_data:
                    issues.append(f"{char_name}: Missing '{field}' field")
            
            # Check moves format
            if "moves" in char_data:
                if not isinstance(char_data["moves"], list):
                    issues.append(f"{char_name}: Moves should be array, got {type(char_data['moves'])}")
                else:
                    for move in char_data["moves"]:
                        required_move_fields = ["move", "name", "startup", "recovery", "on_block", "damage"]
                        for field in required_move_fields:
                            if field not in move:
                                issues.append(f"{char_name} {move.get('move', 'unknown')}: Missing '{field}' field")
            
            # Check combos
            if "bnb_combos" in char_data:
                if not isinstance(char_data["bnb_combos"], dict):
                    issues.append(f"{char_name}: BnB combos should be dict")
    
    if issues:
        print("\n[ERROR] Database structure issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n[OK] Database structure is valid!")
        return True


def verify_character_data():
    """Verify all characters have complete data"""
    print("\n" + "="*70)
    print("VERIFYING CHARACTER DATA COMPLETENESS")
    print("="*70)
    
    issues = []
    warnings = []
    
    for char_name, char_class in CHARACTER_DATA.items():
        print(f"\nChecking {char_name}...")
        
        # Check moves
        moves = char_class.get_moves()
        if not moves:
            issues.append(f"{char_name}: No moves defined")
        else:
            moves_with_zero_data = []
            for move_input, move_data in moves.items():
                if move_data.startup == 0 and move_data.recovery == 0:
                    moves_with_zero_data.append(move_input)
            
            if moves_with_zero_data:
                warnings.append(f"{char_name}: {len(moves_with_zero_data)} moves with 0/0 frame data: {', '.join(moves_with_zero_data)}")
        
        # Check combos
        combos = char_class.get_bnb_combos()
        if not combos:
            warnings.append(f"{char_name}: No BnB combos defined")
        
        # Check character info
        info = char_class.get_character_info()
        if not info:
            issues.append(f"{char_name}: No character info")
        else:
            required_info = ["name", "health", "archetype", "playstyle"]
            for field in required_info:
                if field not in info:
                    issues.append(f"{char_name}: Missing '{field}' in character info")
    
    if issues:
        print("\n[ERROR] Character data issues:")
        for issue in issues:
            print(f"  - {issue}")
    
    if warnings:
        print("\n[WARNING] Character data warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not issues:
        print("\n[OK] All character data is valid!")
        return True
    else:
        return False


def verify_comparison_data():
    """Verify comparison data is generated correctly"""
    print("\n" + "="*70)
    print("VERIFYING COMPARISON DATA")
    print("="*70)
    
    database = generate_character_database()
    
    if "comparison" not in database:
        print("[ERROR] No comparison data found")
        return False
    
    comp = database["comparison"]
    issues = []
    
    # Check fastest moves
    if "fastest_moves" in comp:
        for char_name, moves in comp["fastest_moves"].items():
            if not moves:
                issues.append(f"{char_name}: No fastest moves data")
            else:
                # Verify moves are sorted by startup
                startups = [m["startup"] for m in moves if m["startup"] > 0]
                if startups != sorted(startups):
                    issues.append(f"{char_name}: Fastest moves not properly sorted")
    
    # Check safest moves
    if "safest_moves" in comp:
        for char_name, moves in comp["safest_moves"].items():
            if not moves:
                issues.append(f"{char_name}: No safest moves data")
            else:
                # Verify moves are sorted by on_block (descending)
                on_blocks = [m["on_block"] for m in moves]
                if on_blocks != sorted(on_blocks, reverse=True):
                    issues.append(f"{char_name}: Safest moves not properly sorted")
    
    if issues:
        print("\n[ERROR] Comparison data issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n[OK] Comparison data is valid!")
        return True


def verify_html_files():
    """Verify HTML files exist and are accessible"""
    print("\n" + "="*70)
    print("VERIFYING HTML FILES")
    print("="*70)
    
    required_files = [
        "output/character_database.html",
        "output/character_database_embedded.html",
        "output/character_guide.html",
        "output/custom_controls.html"
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print("\n[ERROR] Missing HTML files:")
        for file in missing:
            print(f"  - {file}")
        return False
    else:
        print("\n[OK] All required HTML files exist!")
        return True


def verify_json_file():
    """Verify JSON database file exists and is valid"""
    print("\n" + "="*70)
    print("VERIFYING JSON DATABASE FILE")
    print("="*70)
    
    json_file = "output/character_database.json"
    
    if not os.path.exists(json_file):
        print(f"\n[ERROR] JSON file not found: {json_file}")
        print("Run: python generate_database.py")
        return False
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "characters" not in data:
            print("\n[ERROR] Invalid JSON structure: missing 'characters'")
            return False
        
        char_count = len(data["characters"])
        print(f"\n[OK] JSON file is valid!")
        print(f"[INFO] Contains {char_count} character(s)")
        
        for char_name in data["characters"].keys():
            moves_count = len(data["characters"][char_name].get("moves", []))
            combos_count = len(data["characters"][char_name].get("bnb_combos", {}))
            print(f"  - {char_name}: {moves_count} moves, {combos_count} combos")
        
        return True
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] Error reading JSON: {e}")
        return False


def print_summary():
    """Print summary of current system state"""
    print("\n" + "="*70)
    print("SYSTEM SUMMARY")
    print("="*70)
    
    print(f"\nRegistered Characters: {len(CHARACTER_DATA)}")
    for char_name in CHARACTER_DATA.keys():
        print(f"  - {char_name}")
    
    print(f"\n2XKO Roster (11 characters):")
    all_characters = ["Ahri", "Braum", "Darius", "Ekko", "Illaoi", "Yasuo", 
                      "Jinx", "Vi", "Blitzcrank", "Teemo", "Warwick"]
    
    implemented = [c for c in all_characters if c in CHARACTER_DATA]
    missing = [c for c in all_characters if c not in CHARACTER_DATA]
    
    print(f"\n  Implemented ({len(implemented)}):")
    for char in implemented:
        print(f"    [OK] {char}")
    
    print(f"\n  Missing ({len(missing)}):")
    for char in missing:
        print(f"    [MISSING] {char}")
    
    print(f"\n[INFO] To add more characters, see: ADDING_CHARACTERS.md")


def main():
    """Run all verification checks"""
    print("="*70)
    print("COMPREHENSIVE PAGE VERIFICATION")
    print("="*70)
    print("\nVerifying all pages and character data...")
    
    results = {
        "database_structure": verify_database_structure(),
        "character_data": verify_character_data(),
        "comparison_data": verify_comparison_data(),
        "html_files": verify_html_files(),
        "json_file": verify_json_file()
    }
    
    print_summary()
    
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "[OK]" if passed else "[FAIL]"
        print(f"{status} {check.replace('_', ' ').title()}")
    
    if all_passed:
        print("\n[OK] ALL CHECKS PASSED!")
        print("\nAll pages should be fully functional.")
        return 0
    else:
        print("\n[FAIL] SOME CHECKS FAILED")
        print("\nPlease fix the issues above before using the system.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
