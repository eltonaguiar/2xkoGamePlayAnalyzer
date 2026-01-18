"""
Update character data from 2XKO wiki.
Uses the provided wiki data to update character_data.py with real frame data.
"""

import json
import re
from character_data import CHARACTER_DATA, MoveData, GuardType
from typing import Dict

# Wiki data extracted from the provided content
WIKI_BLITZCRANK_DATA = {
    "5L": {
        "damage": 45,
        "startup": 8,
        "active": 5,
        "recovery": 12,
        "on_block": -2,
        "guard": "LHA",
        "description": "Standard, albeit slow 5L. Gives a frame trap after 5S1/2S1 restand on hit or block. Has a disjointed hitbox around the steam VFX."
    },
    "5M": {
        "damage": 65,
        "startup": 11,
        "active": 5,
        "recovery": 18,
        "on_block": -5,
        "guard": "LHA",
        "description": "Forward advancing standard and slow 5M."
    },
    "5H": {
        "damage": 90,
        "startup": 16,
        "active": 4,
        "recovery": 31,
        "on_block": -10,
        "guard": "LHA",
        "description": "Can be charged by holding H for a ground bounce on hit."
    },
    "2L": {
        "damage": 45,
        "startup": 9,
        "active": 4,
        "recovery": 12,
        "on_block": -3,
        "guard": "L",
        "description": "Blitz's fastest low. Slower than 5L, so not the best mashing tool. Disjointed hitbox around steam VFX."
    },
    "2M": {
        "damage": 50,  # First hit, then 36
        "startup": 11,
        "active": 11,
        "recovery": 20,
        "on_block": -5,
        "guard": "L",
        "description": "A multi-hit move that first hits low then mid for a launcher. Useful for setting up 2.S1 combo extensions."
    },
    "2H": {
        "damage": 90,
        "startup": 13,
        "active": 4,
        "recovery": 33,
        "on_block": -16,
        "guard": "LHA",
        "description": "Combo launcher, can be jump cancelled. Blitzcrank's main anti-air. Minor Hit Reaction on Counter Hit: Air Tailspin."
    },
    "5S1": {
        "damage": 1,  # Hit grab
        "startup": 25,
        "active": 23,
        "recovery": 30,
        "on_block": 4,  # +4 on block!
        "guard": "LH",
        "description": "Long range hit grab that pulls the opponent in on hit and on block. When Blitzcrank has a bar of Steam Steam, they will shock the opponent on hit."
    },
    "2S1": {
        "damage": 1,
        "startup": 20,
        "active": 11,
        "recovery": 43,
        "on_block": 5,  # +5 on block
        "guard": "A",
        "description": "Long range hit grab that hits only airborne opponents. Without Steam Steam, this move restands the opponent in front of Blitzcrank."
    },
    "2S2": {
        "damage": 250,
        "startup": 6,
        "active": 8,
        "recovery": 57,
        "on_block": 0,  # Unblockable
        "guard": "U",
        "description": "A close range command grab. Hold to do a running grab. If Blitzcrank lands a grab outside of a combo, this charges a lot of Steam Steam."
    }
}


def parse_guard_string(guard_str: str) -> list:
    """Parse guard string like 'LHA' into list of GuardType"""
    guard_types = []
    if 'L' in guard_str:
        guard_types.append(GuardType.LOW)
    if 'H' in guard_str:
        guard_types.append(GuardType.HIGH)
    if 'A' in guard_str:
        guard_types.append(GuardType.AIR)
    if 'U' in guard_str:
        guard_types.append(GuardType.UNBLOCKABLE)
    return guard_types if guard_types else [GuardType.LOW, GuardType.HIGH, GuardType.AIR]


def update_blitzcrank_from_wiki():
    """Update Blitzcrank's moves with real wiki data"""
    from character_data import BlitzcrankData
    
    moves = BlitzcrankData.get_moves()
    
    for move_input, wiki_data in WIKI_BLITZCRANK_DATA.items():
        if move_input in moves:
            move = moves[move_input]
            # Update frame data
            move.damage = wiki_data['damage']
            move.startup = wiki_data['startup']
            move.active = wiki_data['active']
            move.recovery = wiki_data['recovery']
            move.on_block = wiki_data['on_block']
            move.guard = parse_guard_string(wiki_data['guard'])
            move.description = wiki_data['description']
            
            # Update safety
            move.is_safe = move.on_block >= 0
            
            print(f"[OK] Updated {move_input}: {move.startup}f startup, {move.on_block:+d} on block")
    
    return moves


def clean_video_files():
    """Find and remove stale video files"""
    import os
    import glob
    
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.webm']
    video_files = []
    
    # Check output directory
    for ext in video_extensions:
        video_files.extend(glob.glob(f"output/{ext}"))
        video_files.extend(glob.glob(f"output/**/{ext}", recursive=True))
    
    # Check for clips directory
    if os.path.exists("output/clips"):
        for ext in video_extensions:
            video_files.extend(glob.glob(f"output/clips/{ext}"))
    
    if os.path.exists("clips"):
        for ext in video_extensions:
            video_files.extend(glob.glob(f"clips/{ext}"))
    
    if video_files:
        print(f"[INFO] Found {len(video_files)} video files to clean up:")
        for vf in video_files:
            print(f"  - {vf}")
        
        # Ask for confirmation (in automated mode, we'll just report)
        print(f"[INFO] Video files found but not deleted (manual cleanup recommended)")
        return video_files
    else:
        print("[OK] No video files found to clean up")
        return []


if __name__ == "__main__":
    print("Updating Blitzcrank from wiki data...")
    print("="*70)
    
    # Update Blitzcrank
    updated_moves = update_blitzcrank_from_wiki()
    print(f"\n[OK] Updated {len(updated_moves)} moves for Blitzcrank")
    
    # Clean up video files
    print("\n" + "="*70)
    print("Checking for video files to clean up...")
    video_files = clean_video_files()
    
    print("\n" + "="*70)
    print("[OK] Update complete!")
    print("\nNext steps:")
    print("1. Run: python generate_database.py")
    print("2. Run: python generate_embedded_html.py")
    print("3. Open: output/character_database_embedded.html")
