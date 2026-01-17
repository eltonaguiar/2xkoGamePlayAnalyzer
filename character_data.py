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
            is_safe=False
        )
        
        moves["5M"] = MoveData(
            name="5M",
            input="5M",
            damage=0,  # Wiki doesn't specify, placeholder
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=0,  # Wiki doesn't specify
            active=0,
            recovery=0,
            on_block=0,
            cancel_options=[],
            description="Medium standing normal",
            is_safe=False
        )
        
        moves["5H"] = MoveData(
            name="5H",
            input="5H",
            damage=0,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=0,
            active=0,
            recovery=0,
            on_block=0,
            cancel_options=[],
            description="Heavy standing normal",
            is_safe=False
        )
        
        # Crouching Normals
        moves["2L"] = MoveData(
            name="2L",
            input="2L",
            damage=0,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=0,
            active=0,
            recovery=0,
            on_block=0,
            cancel_options=[],
            description="Crouching light",
            is_safe=False
        )
        
        moves["2M"] = MoveData(
            name="2M",
            input="2M",
            damage=0,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=0,
            active=0,
            recovery=0,
            on_block=0,
            cancel_options=[],
            description="Crouching medium",
            is_safe=False
        )
        
        moves["2H"] = MoveData(
            name="2H",
            input="2H",
            damage=0,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=0,
            active=0,
            recovery=0,
            on_block=0,
            cancel_options=[],
            description="Crouching heavy",
            is_safe=False
        )
        
        # Special Moves
        moves["5S1"] = MoveData(
            name="Rocket Grab",
            input="5S1",
            damage=0,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=0,
            active=0,
            recovery=0,
            on_block=0,
            cancel_options=[],
            description="Rocket Grab - pulls opponent close. Can be enhanced with Steam Steam to shock on hit.",
            is_special=True,
            is_safe=False
        )
        
        moves["2S1"] = MoveData(
            name="Air Purifier",
            input="2S1",
            damage=1,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=23,
            active=11,
            recovery=119,
            on_block=44,
            cancel_options=[],
            description="Diagonal long ranged hit grab that pulls the point opponent toward Blitzcrank. Anti-air version of Rocket Grab.",
            is_special=True,
            is_safe=True  # +44 on block is very safe
        )
        
        moves["2S2"] = MoveData(
            name="Garbage Collection",
            input="2S2",
            damage=0,
            guard=[GuardType.UNBLOCKABLE],
            startup=0,
            active=0,
            recovery=0,
            on_block=0,
            cancel_options=[],
            description="Command grab. Enhanced with Steam Steam adds 1 hit of armor and increases damage.",
            is_special=True,
            is_grab=True,
            is_safe=False
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
                "Command grab (Garbage Collection) for mix-ups",
                "Excellent assist character",
                "Steam Steam enhanced specials",
                "Air Purifier assist provides restand"
            ],
            "weaknesses": [
                "Risky neutral",
                "Slow dash speed",
                "Committal normals",
                "Bad defense",
                "Dependency on 50-50 mix-ups"
            ]
        }
    
    @staticmethod
    def is_unsafe_on_block(move_name: str) -> bool:
        """Check if a move is unsafe on block"""
        moves = BlitzcrankData.get_moves()
        if move_name in moves:
            return moves[move_name].on_block < -5  # Generally -5 or worse is punishable
        return False
    
    @staticmethod
    def get_punish_window(on_block: int) -> int:
        """Calculate punish window based on frame disadvantage"""
        if on_block >= 0:
            return 0
        return abs(on_block)


# Character registry
CHARACTER_DATA = {
    "Blitzcrank": BlitzcrankData
}
