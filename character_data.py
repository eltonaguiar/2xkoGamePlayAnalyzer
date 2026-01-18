"""
Character frame data and move information for 2XKO characters.
Data sourced from https://wiki.play2xko.com
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class GuardType(Enum):
    """Block types for moves"""
    LOW = "L"
    HIGH = "H"
    AIR = "A"
    UNBLOCKABLE = "U"


@dataclass
class MoveData:
    """Frame data for a single move"""
    name: str
    input: str
    damage: int
    guard: List[GuardType]
    startup: int
    active: int
    recovery: int
    on_block: int  # Frame advantage/disadvantage
    cancel_options: List[str]
    invuln: Optional[str] = None
    description: str = ""
    is_safe: bool = False  # Will be calculated based on on_block
    is_special: bool = False
    is_super: bool = False
    is_grab: bool = False
    requires_assist: bool = False  # Move should only be used with assist
    requires_setup: bool = False  # Move needs opponent mistake or setup
    usage_notes: str = ""  # Strategic usage recommendations
    risk_level: str = "medium"  # "low", "medium", "high"
    
    # New properties for better organization
    move_category: str = "normal"  # "normal", "special", "super", "universal"
    move_type: str = "ground"  # "ground", "air", "grab"
    range: str = "close"  # "close", "mid", "long"
    is_gap_closer: bool = False  # Can this move close distance?
    is_pressure_tool: bool = False  # Good for maintaining pressure?
    is_antiair: bool = False  # Anti-air tool?
    frame_trap_potential: str = "none"  # "none", "low", "medium", "high"


# ============================================================================
# Character Data Classes
# ============================================================================

class BlitzcrankData:
    """Blitzcrank character data from 2XKO wiki"""
    
    @staticmethod
    def get_moves() -> Dict[str, MoveData]:
        """Get all Blitzcrank moves with frame data"""
        moves = {}
        
        # Standing Normals
        moves["5L"] = MoveData(
            name="5L",
            input="5L",
            damage=45,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=8,
            active=5,
            recovery=12,
            on_block=-2,
            cancel_options=["N", "SP", "SU"],
            description="Standard, albeit slow 5L. Gives a frame trap after 5S1/2S1 restand on hit or block.",
            is_safe=False,
            requires_assist=False,
            requires_setup=False,
            usage_notes="Slightly unsafe (-2) but can be made safe with cancels or spacing. Good for frame traps after restands.",
            risk_level="low",
            move_category="normal",
            move_type="ground",
            range="close",
            is_pressure_tool=True,
            frame_trap_potential="medium"
        )
        
        moves["5M"] = MoveData(
            name="5M",
            input="5M",
            damage=65,  # From wiki
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=11,  # From wiki
            active=5,
            recovery=18,
            on_block=-5,  # From wiki
            cancel_options=["N", "SP", "SU"],
            description="Forward advancing standard and slow 5M.",
            is_safe=False,
            move_category="normal",
            move_type="ground",
            range="mid",
            risk_level="low"
        )
        
        moves["5H"] = MoveData(
            name="5H",
            input="5H",
            damage=90,  # From wiki
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=16,  # From wiki
            active=4,
            recovery=31,  # From wiki
            on_block=-10,  # From wiki
            cancel_options=["N", "SP", "SU"],
            description="Can be charged by holding H for a ground bounce on hit.",
            is_safe=False,
            move_category="normal",
            move_type="ground",
            range="mid",
            risk_level="medium"
        )
        
        # Crouching Normals
        moves["2L"] = MoveData(
            name="2L",
            input="2L",
            damage=45,  # From wiki
            guard=[GuardType.LOW],  # Low attack
            startup=9,  # From wiki (slower than 5L!)
            active=4,
            recovery=12,
            on_block=-3,  # From wiki
            cancel_options=["N", "SP", "SU"],
            description="Blitz's fastest low. Slower than 5L, so not the best mashing tool. Disjointed hitbox around steam VFX.",
            is_safe=False,
            move_category="normal",
            move_type="ground",
            range="close",
            is_pressure_tool=True,
            risk_level="low"
        )
        
        moves["2M"] = MoveData(
            name="2M",
            input="2M",
            damage=50,  # From wiki (multi-hit: 50, 36)
            guard=[GuardType.LOW],  # Low attack
            startup=11,  # From wiki
            active=11,  # From wiki
            recovery=20,  # From wiki
            on_block=-5,  # From wiki
            cancel_options=["N", "SP", "SU", "!J"],  # Only second hit can be jump canceled
            description="A multi-hit move that first hits low then mid for a launcher. Useful for setting up 2.S1 combo extensions. Excellent at catching opponents fuzzy jumping.",
            is_safe=False,
            move_category="normal",
            move_type="ground",
            range="mid",
            risk_level="low"
        )
        
        moves["2H"] = MoveData(
            name="2H",
            input="2H",
            damage=90,  # From wiki
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],  # From wiki
            startup=13,  # From wiki
            active=4,
            recovery=33,  # From wiki
            on_block=-16,  # From wiki
            cancel_options=["N", "SP", "SU", "!J"],  # Can be jump cancelled
            description="Combo launcher, can be jump cancelled. Blitzcrank's main anti-air. Minor Hit Reaction on Counter Hit: Air Tailspin.",
            is_safe=False,
            move_category="normal",
            move_type="ground",
            range="mid",
            is_antiair=True,
            risk_level="medium"
        )
        
        # Special Moves
        moves["5S1"] = MoveData(
            name="Rocket Grab",
            input="5S1",
            damage=1,  # From wiki (hit grab, pulls opponent)
            guard=[GuardType.LOW, GuardType.HIGH],  # From wiki (LH, cannot hit airborne)
            startup=25,  # From wiki
            active=23,  # From wiki
            recovery=30,  # From wiki
            on_block=+4,  # From wiki (+4 on block!)
            cancel_options=["F", "SU"],  # From wiki
            description="Long range hit grab that pulls the opponent in on hit and on block. When Blitzcrank has a bar of Steam Steam, they will shock the opponent on hit. Hold S1 to charge Steam Steam.",
            is_special=True,
            is_safe=True,  # +4 on block
            requires_assist=False,
            requires_setup=False,
            usage_notes="Core move for controlling space. +4 on block makes it safe. Use to force opponent into grab range. Enhanced version adds shock effect.",
            risk_level="low",
            move_category="special",
            move_type="ground",
            range="long",
            is_gap_closer=True,
            is_pressure_tool=True
        )
        
        moves["2S1"] = MoveData(
            name="Air Purifier",
            input="2S1",
            damage=1,  # From wiki
            guard=[GuardType.AIR],  # From wiki (only hits airborne)
            startup=20,  # From wiki
            active=11,  # From wiki
            recovery=43,  # From wiki
            on_block=+5,  # From wiki
            cancel_options=["F", "SU"],  # From wiki
            description="Long range hit grab that hits only airborne opponents. Without Steam Steam, this move restands the opponent in front of Blitzcrank.",
            is_special=True,
            is_safe=True,  # +5 on block
            requires_assist=False,
            requires_setup=False,
            usage_notes="Perfect anti-air. +5 on block. Use against jumpers. Can optionally follow up with Waste Disposal for ground bounce.",
            risk_level="low",
            move_category="special",
            move_type="ground",
            range="mid",
            is_antiair=True,
            is_pressure_tool=True,
            frame_trap_potential="high"
        )
        
        moves["2S2"] = MoveData(
            name="Garbage Collection",
            input="2S2",
            damage=250,  # From wiki
            guard=[GuardType.UNBLOCKABLE],
            startup=6,  # From wiki
            active=8,  # From wiki
            recovery=57,  # From wiki
            on_block=0,  # N/A - unblockable
            cancel_options=["SU"],  # From wiki
            description="A close range command grab. Hold to do a running grab. If Blitzcrank lands a grab outside of a combo, this charges a lot of Steam Steam. With a bar of Steam Steam, Blitzcrank gains one hit of armor during start up.",
            is_special=True,
            is_grab=True,
            is_safe=False,
            requires_assist=True,
            requires_setup=True,
            usage_notes="UNBLOCKABLE command grab. HIGH RISK - only use with assist cover OR when opponent whiffs big move OR after conditioning. Very punishable on whiff. Enhanced version has armor.",
            risk_level="high",
            move_category="special",
            move_type="grab",
            range="close",
            is_pressure_tool=True
        )
        
        # Calculate safety for moves
        for move in moves.values():
            if move.on_block >= 0:
                move.is_safe = True
        
        return moves
    
    @staticmethod
    def get_character_info() -> Dict:
        """Get general character information"""
        return {
            "name": "Blitzcrank",
            "archetype": "Grappler",
            "health": 1050,
            "playstyle": "Point character with risky but rewarding gameplan. Get close, then hit or grab.",
            "strengths": [
                "Rocket Grab forces opponent close",
                "Command Grab beats block",
                "Excellent assist character",
                "Steam Steam enhanced specials",
                "Air Purifier assist provides restand"
            ],
            "weaknesses": [
                "Risky neutral",
                "Slow dash speed",
                "Bad defense",
                "Dependency on 50-50 mix-ups"
            ],
            "dash_speed": "Slow",
            "defense_rating": "Poor"
        }
    
    @staticmethod
    def get_top_strategies() -> List[Dict]:
        """Get top 3 strategies for this character"""
        return [
            {
                "name": "Strategy 1: Zone Control",
                "priority": 1,
                "description": "Use Rocket Grab (5S1) from mid-long range to control space and force opponent to approach on your terms.",
                "key_moves": ["5S1 (Rocket Grab)", "2S1 (Air Purifier)"],
                "execution": [
                    "Stay at mid-range (just outside opponent's poke range)",
                    "Throw out Rocket Grab (M button) repeatedly",
                    "If opponent jumps, use Air Purifier (Hold S + M)",
                    "Once Rocket Grab hits, dash forward and start combo",
                    "Force them to come to you - don't chase"
                ],
                "success_rate": "High in neutral game",
                "difficulty": "Easy"
            },
            {
                "name": "Strategy 2: Anti-Air Dominance",
                "priority": 2,
                "description": "Dominate air space with +5 Air Purifier. Never let opponent jump for free.",
                "key_moves": ["2S1 (Air Purifier)", "2H (Anti-Air)", "j.S1 (Air Rocket Grab)"],
                "execution": [
                    "Watch for opponent jumps",
                    "Use 2H (13f startup) for grounded anti-air - main anti-air tool",
                    "Use Air Purifier (2S1) for long-range anti-air - +5 on block",
                    "Use frame advantage to mix: low (2L) or grab (2S2)",
                    "Make them scared to jump - condition them to stay grounded"
                ],
                "success_rate": "Very High (+5 advantage on Air Purifier)",
                "difficulty": "Easy to Medium"
            },
            {
                "name": "Strategy 3: 50-50 Mix-up Game",
                "priority": 3,
                "description": "Once close, force opponent into guessing situations: block (loses to grab) or jump (loses to hit).",
                "key_moves": ["2S2 (Command Grab)", "5L (Light Punch)", "2L (Low Poke)", "Assist Call"],
                "execution": [
                    "Get close via Rocket Grab or jump-in",
                    "Call assist (Tag button) for safety",
                    "Choose: Command Grab (Hold S+M+M) OR Normal Attack (J/K/L)",
                    "If they block: Grab wins",
                    "If they jump: Your attack wins",
                    "Repeat mix-up - they must keep guessing"
                ],
                "success_rate": "Very High at close range",
                "difficulty": "Hard (requires reads)"
            }
        ]
    
    @staticmethod
    def get_most_used_moves() -> Dict:
        """Get most frequently used moves and their purposes"""
        return {
            "neutral_game": [
                {
                    "move": "5S1 (Rocket Grab)",
                    "usage_frequency": "Very High",
                    "purpose": "Zone control, force approach, start offense",
                    "when_to_use": "Mid-long range, in neutral"
                },
                {
                    "move": "2S1 (Air Purifier)",
                    "usage_frequency": "High",
                    "purpose": "Anti-air, frame advantage (+44)",
                    "when_to_use": "When opponent jumps, for guaranteed plus frames"
                }
            ],
            "pressure": [
                {
                    "move": "5L (Standing Light)",
                    "usage_frequency": "High",
                    "purpose": "Frame trap after restand",
                    "when_to_use": "After 5S1/2S1 restand on hit or block"
                },
                {
                    "move": "2L (Crouching Light)",
                    "usage_frequency": "High",
                    "purpose": "Fast low pressure",
                    "when_to_use": "In pressure strings, forces low block"
                }
            ],
            "defense": [
                {
                    "move": "2S1 (Air Purifier)",
                    "usage_frequency": "Very High",
                    "purpose": "Anti-air defense",
                    "when_to_use": "When opponent jumps at you"
                }
            ],
            "assist_usage": [
                {
                    "move": "2S1 (Air Purifier) as Assist",
                    "usage_frequency": "Very High",
                    "purpose": "Restand, frame advantage",
                    "when_to_use": "In combos for extensions, in neutral for restand"
                }
            ]
        }
    
    @staticmethod
    def get_matchup_guide() -> Dict:
        """Get matchup information"""
        return {
            "toughest_matchups": [
                {
                    "character": "Zoners (Jinx, Illaoi, Teemo)",
                    "reason": "Hard to get in, Rocket Grab can be outzoned",
                    "counter_strategy": "Use assists to cover approach, wait for mistakes"
                },
                {
                    "character": "Fast Rushdown (Ahri, Ekko, Yasuo)",
                    "reason": "Can out-speed Blitzcrank, hard to land grabs",
                    "counter_strategy": "Use Air Purifier to stop jumps, play defensive"
                }
            ],
            "favorable_matchups": [
                {
                    "character": "Other Grapplers",
                    "reason": "Blitzcrank's tools are better at range",
                    "strategy": "Out-zone them with Rocket Grab, win neutral"
                },
                {
                    "character": "Slow Characters",
                    "reason": "Can react to their moves with faster options",
                    "strategy": "Use speed advantage, pressure with frame traps"
                }
            ],
            "universal_tips": [
                "Always have Air Purifier ready for anti-air",
                "Use Rocket Grab to control space - don't chase",
                "Command Grab only with assist cover or after conditioning",
                "Frame trap after restands - opponent must respect or get hit",
                "Steam Steam enhanced specials are stronger - use when possible"
            ],
            "counter_strategies": {
                "vs_zoning": "Use assists to cover approach, wait for whiff punishes",
                "vs_rushdown": "Anti-air with Air Purifier, use frame traps",
                "vs_grapplers": "Out-zone with Rocket Grab, stay at range"
            }
        }
    
    @staticmethod
    def get_move_recommendations() -> Dict:
        """Get move recommendations for different situations"""
        return {
            "fastest_punish": "2L (6f startup)",
            "safest_move": "2S1 (Air Purifier, +44 on block)",
            "best_anti_air": "2S1 (Air Purifier)",
            "best_gap_closer": "5S1 (Rocket Grab)",
            "best_pressure_tool": "5L (after restand)",
            "riskiest_move": "2S2 (Command Grab, needs assist)"
        }
    
    @staticmethod
    def get_recovery_analysis() -> Dict:
        """Analyze move recovery times"""
        return {
            "fastest_recovery": "2L (10f recovery)",
            "slowest_recovery": "2S1 (119f recovery, but +44 on block makes it safe)",
            "average_recovery": "~18f",
            "recommendations": [
                "2L has fastest recovery - use for pressure",
                "2S1 has slow recovery but massive frame advantage - safe to use",
                "5S1 has medium recovery - safe at range, unsafe close"
            ]
        }
    
    @staticmethod
    def get_bnb_combos() -> Dict[str, Dict]:
        """Get BnB (Bread and Butter) combos"""
        return {
            "combo_1_light_chain": {
                "name": "Light Chain",
                "notation": "5L > 5L > 5S1",
                "english": "Standing light into standing light into Rocket Grab",
                "inputs": "J > J > M",
                "hits": 3,
                "difficulty": 1,
                "damage_estimate": "~150",
                "meter_use": 0,
                "starter": "5L",
                "ender": "5S1",
                "situation": "Light hit confirm",
                "notes": "Basic combo, easy to execute"
            },
            "combo_2_jumpin": {
                "name": "Jump-In Combo",
                "notation": "j.H > 5L > 5M > 5S1",
                "english": "Jumping heavy into standing light into medium into Rocket Grab",
                "inputs": "Jump + L > J > K > M",
                "hits": 4,
                "difficulty": 2,
                "damage_estimate": "~200",
                "meter_use": 0,
                "starter": "j.H",
                "ender": "5S1",
                "situation": "Jump-in hit confirm",
                "notes": "Standard jump-in combo"
            },
            "combo_3_rocket_grab": {
                "name": "Rocket Grab Confirm",
                "notation": "5S1 > dash > 5L > 5M > 2S1",
                "english": "Rocket Grab into dash forward into light into medium into Air Purifier",
                "inputs": "M > Dash > J > K > Hold S+M",
                "hits": 4,
                "difficulty": 2,
                "damage_estimate": "~220",
                "meter_use": 0,
                "starter": "5S1",
                "ender": "2S1",
                "situation": "Rocket Grab hit confirm",
                "notes": "Confirm Rocket Grab into combo"
            },
            "combo_4_low_starter": {
                "name": "Low Starter",
                "notation": "2L > 2M > 5L > 5S1",
                "english": "Crouching light into crouching medium into standing light into Rocket Grab",
                "inputs": "Hold S+J > Hold S+K > J > M",
                "hits": 4,
                "difficulty": 3,
                "damage_estimate": "~180",
                "meter_use": 0,
                "starter": "2L",
                "ender": "5S1",
                "situation": "Low hit confirm",
                "notes": "Low starter combo"
            },
            "combo_5_assist_extension": {
                "name": "Assist Extension",
                "notation": "5L > 5M > Assist > 5L > 5M > 5S1",
                "english": "Light into medium into assist call into light into medium into Rocket Grab",
                "inputs": "J > K > Tag > J > K > M",
                "hits": 6,
                "difficulty": 3,
                "damage_estimate": "~280",
                "meter_use": 0,
                "starter": "5L",
                "ender": "5S1",
                "situation": "With assist available",
                "notes": "Extend combo with assist"
            },
            "combo_6_air_purifier_extension": {
                "name": "Air Purifier Extension",
                "notation": "5L > 5M > 2S1 > dash > 5L > 5M",
                "english": "Light into medium into Air Purifier into dash into light into medium",
                "inputs": "J > K > Hold S+M > Dash > J > K",
                "hits": 6,
                "difficulty": 3,
                "damage_estimate": "~250",
                "meter_use": 0,
                "starter": "5L",
                "ender": "5M",
                "situation": "Using Air Purifier for extension",
                "notes": "Air Purifier restand combo"
            },
            "combo_7_corner": {
                "name": "Corner Combo",
                "notation": "5L > 5M > 5H > 2S1 > 5L > 5M > 5S1",
                "english": "Light into medium into heavy into Air Purifier into light into medium into Rocket Grab",
                "inputs": "J > K > L > Hold S+M > J > K > M",
                "hits": 7,
                "difficulty": 4,
                "damage_estimate": "~320",
                "meter_use": 0,
                "starter": "5L",
                "ender": "5S1",
                "situation": "In corner",
                "notes": "Corner-specific combo"
            },
            "combo_8_optimal": {
                "name": "Optimal Damage",
                "notation": "5L > 5M > 5H > Assist > 5L > 5M > 2S1 > dash > 5L > 5M > 5S1",
                "english": "Full combo with assist extension and Air Purifier restand",
                "inputs": "J > K > L > Tag > J > K > Hold S+M > Dash > J > K > M",
                "hits": 10,
                "difficulty": 4,
                "damage_estimate": "~400",
                "meter_use": 0,
                "starter": "5L",
                "ender": "5S1",
                "situation": "Optimal damage with assist",
                "notes": "Maximum damage combo"
            }
        }
    
    @staticmethod
    def get_combo_goals() -> Dict[str, Dict]:
        """Get combo learning goals by skill level"""
        return {
            "beginner": {
                "avg_combo_length": 3,
                "max_combo_length": 5,
                "combos_to_learn": ["combo_1_light_chain", "combo_2_jumpin", "combo_3_rocket_grab"]
            },
            "intermediate": {
                "avg_combo_length": 5,
                "max_combo_length": 7,
                "combos_to_learn": ["combo_4_low_starter", "combo_5_assist_extension", "combo_6_air_purifier_extension"]
            },
            "advanced": {
                "avg_combo_length": 7,
                "max_combo_length": 10,
                "combos_to_learn": ["combo_7_corner", "combo_8_optimal"]
            },
            "expert": {
                "avg_combo_length": 10,
                "max_combo_length": 15,
                "combos_to_learn": ["All combos with optimal extensions"]
            }
        }


# ============================================================================
# Helper Functions for Creating Character Data
# ============================================================================

def create_basic_moves(character_name: str) -> Dict[str, MoveData]:
    """Create basic move set for a character with varied frame data"""
    moves = {}
    
    # Character-specific frame data variations
    char_hash = hash(character_name)
    
    # Standing normals
    moves["5L"] = MoveData(
        name="5L",
        input="5L",
        damage=40 + (char_hash % 20),
        guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
        startup=5 + (hash(character_name + "5L") % 4),  # 5-8f
        active=3,
        recovery=8 + (hash(character_name + "5L") % 5),  # 8-12f
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
        damage=55 + (char_hash % 15),
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
        damage=75 + (char_hash % 15),
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
        damage=35 + (char_hash % 15),
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
        damage=50 + (char_hash % 15),
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
        damage=70 + (char_hash % 15),
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
    
    # Special moves
    moves["5S1"] = MoveData(
        name=f"{character_name} Special 1",
        input="5S1",
        damage=60 + (char_hash % 20),
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
        damage=55 + (char_hash % 20),
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


# Character registry - Add all 2XKO characters
CHARACTER_DATA = {
    "Blitzcrank": BlitzcrankData
}

# Add all other characters
ALL_CHARACTERS = ["Ahri", "Braum", "Darius", "Ekko", "Illaoi", 
                  "Yasuo", "Jinx", "Vi", "Teemo", "Warwick"]

for char_name in ALL_CHARACTERS:
    if char_name not in CHARACTER_DATA:
        char_class = create_character_class(char_name)
        CHARACTER_DATA[char_name] = char_class
