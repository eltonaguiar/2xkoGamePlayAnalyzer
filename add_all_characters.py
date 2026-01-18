"""
Script to add all 2XKO characters with basic frame data.
Creates placeholder data for all characters so the system works with all of them.
"""

from character_data import CHARACTER_DATA, MoveData, GuardType
from typing import Dict, List

# 2XKO Character roster
ALL_CHARACTERS = [
    "Ahri", "Braum", "Darius", "Ekko", "Illaoi", 
    "Yasuo", "Jinx", "Vi", "Blitzcrank", "Teemo", "Warwick"
]

# Character archetypes and basic info
CHARACTER_INFO = {
    "Ahri": {
        "archetype": "Rushdown",
        "health": 1000,
        "playstyle": "Fast, mobile character with mix-up potential",
        "dash_speed": "Fast",
        "defense_rating": "Average"
    },
    "Braum": {
        "archetype": "Defensive",
        "health": 1100,
        "playstyle": "Tanky character with defensive tools",
        "dash_speed": "Slow",
        "defense_rating": "Excellent"
    },
    "Darius": {
        "archetype": "Grappler",
        "health": 1050,
        "playstyle": "Close-range powerhouse with command grabs",
        "dash_speed": "Medium",
        "defense_rating": "Good"
    },
    "Ekko": {
        "archetype": "Rushdown",
        "health": 1000,
        "playstyle": "Time manipulation and mix-ups",
        "dash_speed": "Fast",
        "defense_rating": "Average"
    },
    "Illaoi": {
        "archetype": "Zoner",
        "health": 1050,
        "playstyle": "Space control with tentacles",
        "dash_speed": "Medium",
        "defense_rating": "Good"
    },
    "Yasuo": {
        "archetype": "Rushdown",
        "health": 1000,
        "playstyle": "High mobility, sword-based combos",
        "dash_speed": "Fast",
        "defense_rating": "Average"
    },
    "Jinx": {
        "archetype": "Zoner",
        "health": 950,
        "playstyle": "Long-range projectile character",
        "dash_speed": "Medium",
        "defense_rating": "Poor"
    },
    "Vi": {
        "archetype": "Rushdown",
        "health": 1050,
        "playstyle": "Aggressive brawler with armor moves",
        "dash_speed": "Fast",
        "defense_rating": "Good"
    },
    "Teemo": {
        "archetype": "Zoner",
        "health": 900,
        "playstyle": "Trap-based zoner with stealth",
        "dash_speed": "Fast",
        "defense_rating": "Poor"
    },
    "Warwick": {
        "archetype": "Rushdown",
        "health": 1100,
        "playstyle": "Aggressive rushdown with life steal",
        "dash_speed": "Fast",
        "defense_rating": "Good"
    }
}


def create_basic_moves(character_name: str) -> Dict[str, MoveData]:
    """Create basic move set for a character"""
    moves = {}
    
    # Typical frame data ranges for fighting games
    # Standing normals
    moves["5L"] = MoveData(
        name="5L",
        input="5L",
        damage=40 + (hash(character_name) % 20),  # Vary damage slightly
        guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
        startup=5 + (hash(character_name + "5L") % 4),  # 5-8f range
        active=3,
        recovery=8 + (hash(character_name + "5L") % 5),  # 8-12f range
        on_block=-1 - (hash(character_name + "5L") % 3),  # -1 to -3
        cancel_options=["N", "SP", "SU"],
        description=f"{character_name}'s standing light attack",
        is_safe=False,
        move_category="normal",
        move_type="ground",
        range="close",
        risk_level="low"
    )
    
    moves["5M"] = MoveData(
        name="5M",
        input="5M",
        damage=55 + (hash(character_name) % 15),
        guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
        startup=9 + (hash(character_name + "5M") % 4),  # 9-12f
        active=4,
        recovery=15 + (hash(character_name + "5M") % 5),  # 15-19f
        on_block=-3 - (hash(character_name + "5M") % 3),  # -3 to -5
        cancel_options=["N", "SP", "SU"],
        description=f"{character_name}'s standing medium attack",
        is_safe=False,
        move_category="normal",
        move_type="ground",
        range="mid",
        risk_level="low"
    )
    
    moves["5H"] = MoveData(
        name="5H",
        input="5H",
        damage=75 + (hash(character_name) % 15),
        guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
        startup=12 + (hash(character_name + "5H") % 4),  # 12-15f
        active=5,
        recovery=20 + (hash(character_name + "5H") % 6),  # 20-25f
        on_block=-5 - (hash(character_name + "5H") % 4),  # -5 to -8
        cancel_options=["N", "SP", "SU"],
        description=f"{character_name}'s standing heavy attack",
        is_safe=False,
        move_category="normal",
        move_type="ground",
        range="mid",
        risk_level="medium"
    )
    
    # Crouching normals
    moves["2L"] = MoveData(
        name="2L",
        input="2L",
        damage=35 + (hash(character_name) % 15),
        guard=[GuardType.LOW],
        startup=5 + (hash(character_name + "2L") % 3),  # 5-7f
        active=3,
        recovery=8 + (hash(character_name + "2L") % 4),  # 8-11f
        on_block=-1 - (hash(character_name + "2L") % 3),  # -1 to -3
        cancel_options=["N", "SP", "SU"],
        description=f"{character_name}'s crouching light attack",
        is_safe=False,
        move_category="normal",
        move_type="ground",
        range="close",
        risk_level="low"
    )
    
    moves["2M"] = MoveData(
        name="2M",
        input="2M",
        damage=50 + (hash(character_name) % 15),
        guard=[GuardType.LOW],
        startup=8 + (hash(character_name + "2M") % 3),  # 8-10f
        active=4,
        recovery=14 + (hash(character_name + "2M") % 4),  # 14-17f
        on_block=-3 - (hash(character_name + "2M") % 3),  # -3 to -5
        cancel_options=["N", "SP", "SU"],
        description=f"{character_name}'s crouching medium attack",
        is_safe=False,
        move_category="normal",
        move_type="ground",
        range="mid",
        risk_level="low"
    )
    
    moves["2H"] = MoveData(
        name="2H",
        input="2H",
        damage=70 + (hash(character_name) % 15),
        guard=[GuardType.LOW],
        startup=10 + (hash(character_name + "2H") % 4),  # 10-13f
        active=6,
        recovery=18 + (hash(character_name + "2H") % 6),  # 18-23f
        on_block=-6 - (hash(character_name + "2H") % 4),  # -6 to -9
        cancel_options=["N", "SP", "SU"],
        description=f"{character_name}'s crouching heavy attack",
        is_safe=False,
        move_category="normal",
        move_type="ground",
        range="mid",
        risk_level="medium"
    )
    
    # Special moves (character-specific)
    moves["5S1"] = MoveData(
        name=f"{character_name} Special 1",
        input="5S1",
        damage=60 + (hash(character_name) % 20),
        guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
        startup=15 + (hash(character_name + "5S1") % 6),  # 15-20f
        active=6,
        recovery=25 + (hash(character_name + "5S1") % 10),  # 25-34f
        on_block=-4 - (hash(character_name + "5S1") % 4),  # -4 to -7
        cancel_options=[],
        description=f"{character_name}'s primary special move",
        is_special=True,
        is_safe=False,
        move_category="special",
        move_type="ground",
        range="mid",
        risk_level="medium"
    )
    
    moves["2S1"] = MoveData(
        name=f"{character_name} Special 2",
        input="2S1",
        damage=55 + (hash(character_name) % 20),
        guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
        startup=18 + (hash(character_name + "2S1") % 8),  # 18-25f
        active=8,
        recovery=30 + (hash(character_name + "2S1") % 15),  # 30-44f
        on_block=-2 - (hash(character_name + "2S1") % 5),  # -2 to -6
        cancel_options=[],
        description=f"{character_name}'s secondary special move",
        is_special=True,
        is_safe=False,
        move_category="special",
        move_type="ground",
        range="mid",
        risk_level="medium"
    )
    
    # Calculate safety
    for move in moves.values():
        if move.on_block >= 0:
            move.is_safe = True
    
    return moves


def create_basic_combos(character_name: str) -> Dict[str, Dict]:
    """Create basic combo set for a character"""
    return {
        "basic_combo": {
            "name": "Basic BnB",
            "notation": "5L > 5M > 5H",
            "english": "Light into medium into heavy",
            "inputs": "J > K > L",
            "hits": 3,
            "difficulty": 1,
            "damage_estimate": "~150",
            "meter_use": 0,
            "starter": "5L",
            "ender": "5H",
            "situation": "Basic hit confirm",
            "notes": f"{character_name}'s basic combo"
        },
        "low_combo": {
            "name": "Low Starter",
            "notation": "2L > 2M > 5S1",
            "english": "Crouching light into medium into special",
            "inputs": "Hold S+J > Hold S+K > M",
            "hits": 3,
            "difficulty": 2,
            "damage_estimate": "~180",
            "meter_use": 0,
            "starter": "2L",
            "ender": "5S1",
            "situation": "Low hit confirm",
            "notes": f"{character_name}'s low combo"
        }
    }


def create_character_class(character_name: str):
    """Create a character data class for a character"""
    
    info = CHARACTER_INFO.get(character_name, {
        "archetype": "Rushdown",
        "health": 1000,
        "playstyle": "Balanced character",
        "dash_speed": "Medium",
        "defense_rating": "Average"
    })
    
    class CharacterData:
        """Character data class"""
        
        @staticmethod
        def get_character_info() -> Dict:
            return {
                "name": character_name,
                "archetype": info["archetype"],
                "health": info["health"],
                "playstyle": info["playstyle"],
                "strengths": [f"{character_name}'s strengths"],
                "weaknesses": [f"{character_name}'s weaknesses"],
                "dash_speed": info["dash_speed"],
                "defense_rating": info["defense_rating"]
            }
        
        @staticmethod
        def get_moves() -> Dict[str, MoveData]:
            return create_basic_moves(character_name)
        
        @staticmethod
        def get_bnb_combos() -> Dict[str, Dict]:
            return create_basic_combos(character_name)
        
        @staticmethod
        def get_top_strategies() -> List[Dict]:
            return [
                {
                    "name": f"{character_name} Strategy 1",
                    "priority": 1,
                    "description": f"Basic strategy for {character_name}",
                    "key_moves": ["5L", "5M"],
                    "execution": ["Use 5L to poke", "Confirm into 5M"],
                    "success_rate": "Medium",
                    "difficulty": "Easy"
                }
            ]
        
        @staticmethod
        def get_most_used_moves() -> Dict:
            return {
                "neutral_game": [
                    {
                        "move": "5L",
                        "usage_frequency": "High",
                        "purpose": "Quick poke",
                        "when_to_use": "In neutral"
                    }
                ]
            }
        
        @staticmethod
        def get_matchup_guide() -> Dict:
            return {
                "toughest_matchups": [],
                "favorable_matchups": [],
                "universal_tips": [f"Learn {character_name}'s frame data"],
                "counter_strategies": {}
            }
        
        @staticmethod
        def get_move_recommendations() -> Dict:
            return {}
        
        @staticmethod
        def get_recovery_analysis() -> Dict:
            return {}
        
        @staticmethod
        def get_combo_goals() -> Dict:
            return {}
    
    # Set class name
    CharacterData.__name__ = f"{character_name}Data"
    
    return CharacterData


def add_all_characters():
    """Add all 2XKO characters to CHARACTER_DATA"""
    from character_data import CHARACTER_DATA
    
    added = 0
    for char_name in ALL_CHARACTERS:
        if char_name not in CHARACTER_DATA:
            char_class = create_character_class(char_name)
            CHARACTER_DATA[char_name] = char_class
            added += 1
            print(f"[OK] Added {char_name}")
        else:
            print(f"[SKIP] {char_name} already exists")
    
    print(f"\n[OK] Added {added} new characters")
    print(f"[OK] Total characters: {len(CHARACTER_DATA)}")
    
    return CHARACTER_DATA


if __name__ == "__main__":
    print("Adding all 2XKO characters...")
    print("="*70)
    
    # Import and modify CHARACTER_DATA
    import character_data
    add_all_characters()
    
    print("\n" + "="*70)
    print("[OK] All characters added!")
    print("\nNext steps:")
    print("1. Run: python generate_database.py")
    print("2. Run: python generate_embedded_html.py")
    print("3. Open: output/character_database_embedded.html")
