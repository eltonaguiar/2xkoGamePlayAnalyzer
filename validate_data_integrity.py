"""
Comprehensive data integrity validation script.
Checks for data inconsistencies, missing fields, and alignment issues.
"""

import json
import os
import sys
from typing import Dict, List, Tuple

def validate_character_data(database_path: str = 'output/character_database.json') -> Dict:
    """Validate character database for data integrity issues"""
    
    issues = {
        'errors': [],
        'warnings': [],
        'data_quality': {}
    }
    
    if not os.path.exists(database_path):
        issues['errors'].append(f'Database file not found: {database_path}')
        return issues
    
    try:
        with open(database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        issues['errors'].append(f'Failed to load database: {str(e)}')
        return issues
    
    if 'characters' not in data:
        issues['errors'].append('Missing "characters" key in database')
        return issues
    
    characters = data['characters']
    
    # Required fields for each character
    required_fields = ['info', 'moves', 'bnb_combos']
    required_move_fields = ['move', 'startup', 'recovery', 'on_block', 'damage']
    
    for char_name, char_data in characters.items():
        char_issues = []
        
        # Check required character fields
        for field in required_fields:
            if field not in char_data:
                char_issues.append(f'Missing required field: {field}')
        
        # Check info structure
        if 'info' in char_data:
            info = char_data['info']
            if 'name' not in info:
                char_issues.append('Missing info.name')
            if 'health' not in info:
                char_issues.append('Missing info.health')
        
        # Check moves
        if 'moves' in char_data:
            moves = char_data['moves']
            if not isinstance(moves, list):
                char_issues.append('moves is not an array')
            else:
                for i, move in enumerate(moves):
                    if not isinstance(move, dict):
                        char_issues.append(f'Move {i} is not an object')
                        continue
                    
                    # Check required move fields
                    for field in required_move_fields:
                        if field not in move:
                            char_issues.append(f'Move {i} ({move.get("move", "unknown")}) missing field: {field}')
                    
                    # Validate frame data ranges
                    if 'startup' in move:
                        if not isinstance(move['startup'], int) or move['startup'] < 0:
                            char_issues.append(f'Move {i} ({move.get("move", "unknown")}) has invalid startup: {move["startup"]}')
                    
                    if 'recovery' in move:
                        if not isinstance(move['recovery'], int) or move['recovery'] < 0:
                            char_issues.append(f'Move {i} ({move.get("move", "unknown")}) has invalid recovery: {move["recovery"]}')
                    
                    if 'on_block' in move:
                        if not isinstance(move['on_block'], (int, float)):
                            char_issues.append(f'Move {i} ({move.get("move", "unknown")}) has invalid on_block: {move["on_block"]}')
                    
                    if 'damage' in move:
                        if not isinstance(move['damage'], (int, float)) or move['damage'] < 0:
                            char_issues.append(f'Move {i} ({move.get("move", "unknown")}) has invalid damage: {move["damage"]}')
                    
                    # Check for placeholder data
                    description = move.get('description', '').lower()
                    if any(phrase in description for phrase in ['standing light attack', 'standing medium attack', 'standing heavy attack', 'crouching light attack', 'primary special move', 'secondary special move']):
                        issues['warnings'].append(f'{char_name} - Move {move.get("move", "unknown")} has placeholder description')
        
        # Check combos
        if 'bnb_combos' in char_data:
            combos = char_data['bnb_combos']
            if not isinstance(combos, dict):
                char_issues.append('bnb_combos is not an object')
        
        if char_issues:
            issues['data_quality'][char_name] = char_issues
            if any('Missing' in issue or 'invalid' in issue.lower() for issue in char_issues):
                issues['errors'].extend([f'{char_name}: {issue}' for issue in char_issues])
            else:
                issues['warnings'].extend([f'{char_name}: {issue}' for issue in char_issues])
    
    return issues

def check_video_file_references(html_path: str) -> Dict:
    """Check for video file references in HTML files"""
    
    issues = {
        'missing_files': [],
        'references_found': []
    }
    
    if not os.path.exists(html_path):
        return issues
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find video file references
    import re
    video_patterns = [
        r'clips[/\\][^"\']+\.(mp4|webm|gif)',
        r'"clips[^"]+\.(mp4|webm|gif)"',
        r"'clips[^']+\.(mp4|webm|gif)'"
    ]
    
    for pattern in video_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                file_path = match[0] if match[0] else match[1]
            else:
                file_path = match
            
            issues['references_found'].append(file_path)
            
            # Check if file exists
            full_path = os.path.join('output', file_path.replace('\\', '/'))
            if not os.path.exists(full_path):
                issues['missing_files'].append(file_path)
    
    return issues

def main():
    """Run comprehensive data validation"""
    
    print("="*70)
    print("COMPREHENSIVE DATA INTEGRITY VALIDATION")
    print("="*70)
    
    # Validate character database
    print("\n[1] Validating Character Database...")
    db_issues = validate_character_data()
    
    if db_issues['errors']:
        print(f"\n[ERROR] Found {len(db_issues['errors'])} errors:")
        for error in db_issues['errors'][:10]:
            print(f"  - {error}")
    
    if db_issues['warnings']:
        print(f"\n[WARN] Found {len(db_issues['warnings'])} warnings:")
        for warning in db_issues['warnings'][:10]:
            print(f"  - {warning}")
    
    if not db_issues['errors'] and not db_issues['warnings']:
        print("  ✅ No issues found!")
    
    # Check video file references
    print("\n[2] Checking Video File References...")
    video_issues = check_video_file_references('output/video_player.html')
    
    if video_issues['references_found']:
        print(f"  Found {len(video_issues['references_found'])} video references")
        if video_issues['missing_files']:
            print(f"  [WARN] {len(video_issues['missing_files'])} missing files:")
            for file in video_issues['missing_files'][:5]:
                print(f"    - {file}")
        else:
            print("  ✅ All referenced video files exist")
    else:
        print("  ℹ️  No video file references found")
    
    # Summary
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    print(f"Database Errors: {len(db_issues['errors'])}")
    print(f"Database Warnings: {len(db_issues['warnings'])}")
    print(f"Missing Video Files: {len(video_issues['missing_files'])}")
    
    if db_issues['errors']:
        print("\n[ERROR] Data integrity issues found!")
        sys.exit(1)
    else:
        print("\n[OK] Data integrity validation passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
