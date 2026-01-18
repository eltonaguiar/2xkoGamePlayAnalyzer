"""
Verify that all characters are properly displayed in the HTML files.
"""

import json
import re

def check_json_database():
    """Check JSON database has all characters"""
    print("="*70)
    print("Checking JSON Database")
    print("="*70)
    
    with open('output/character_database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    characters = list(data['characters'].keys())
    print(f"\n[OK] Total characters in JSON: {len(characters)}")
    for char in characters:
        moves_count = len(data['characters'][char].get('moves', []))
        combos_count = len(data['characters'][char].get('bnb_combos', {}))
        print(f"  - {char}: {moves_count} moves, {combos_count} combos")
    
    return characters


def check_embedded_html():
    """Check embedded HTML has all characters"""
    print("\n" + "="*70)
    print("Checking Embedded HTML")
    print("="*70)
    
    with open('output/character_database_embedded.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check for character names in the embedded JSON
    characters_found = []
    for char in ["Blitzcrank", "Ahri", "Braum", "Darius", "Ekko", "Illaoi", 
                 "Yasuo", "Jinx", "Vi", "Teemo", "Warwick"]:
        # Look for character in JSON structure
        pattern = f'"{char}":{{"info"'
        if pattern in html_content:
            characters_found.append(char)
            print(f"  [OK] {char} found in embedded HTML")
        else:
            print(f"  [WARN] {char} NOT found in embedded HTML")
    
    print(f"\n[OK] Found {len(characters_found)}/11 characters in embedded HTML")
    return characters_found


def check_regular_html():
    """Check regular HTML loads from JSON"""
    print("\n" + "="*70)
    print("Checking Regular HTML")
    print("="*70)
    
    with open('output/character_database.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Check if it has loadDatabase function
    if 'loadDatabase' in html_content and 'character_database.json' in html_content:
        print("[OK] HTML has loadDatabase function")
        print("[OK] HTML references character_database.json")
    else:
        print("[WARN] HTML might not load database correctly")
    
    # Check initializeUI
    if 'initializeUI' in html_content:
        print("[OK] HTML has initializeUI function")
    
    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("VERIFYING ALL CHARACTERS ARE AVAILABLE")
    print("="*70)
    
    json_chars = check_json_database()
    html_chars = check_embedded_html()
    check_regular_html()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if len(json_chars) == 11:
        print("[OK] JSON database has all 11 characters")
    else:
        print(f"[ERROR] JSON database missing characters! Only {len(json_chars)}/11")
    
    if len(html_chars) == 11:
        print("[OK] Embedded HTML has all 11 characters")
    else:
        print(f"[WARN] Embedded HTML missing some characters! Only {len(html_chars)}/11")
        print("       This might be why only Blitzcrank shows in UI")
    
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    print("1. Open: output/character_database_embedded.html (works standalone)")
    print("2. Check Character Overview tab - should show all 11 characters")
    print("3. Check Move Database tab - dropdown should list all 11 characters")
    print("4. If only Blitzcrank shows, check browser console for errors")
