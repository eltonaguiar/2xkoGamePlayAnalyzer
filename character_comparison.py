"""
Character comparison and analysis system for 2XKO.
Allows comparing moves, combos, and stats across all characters.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class CharacterStats:
    """Core character statistics"""
    name: str
    health: int
    archetype: str
    dash_speed: str  # "Fast", "Medium", "Slow"
    defense_rating: str  # "Excellent", "Good", "Average", "Poor"
    
    
class CharacterComparison:
    """Compare characters and their moves"""
    
    def __init__(self, character_data_registry: Dict):
        """
        Initialize with character data registry
        
        Args:
            character_data_registry: Dict of character name -> character data class
        """
        self.characters = character_data_registry
    
    def get_all_character_stats(self) -> List[Dict]:
        """Get basic stats for all characters"""
        stats = []
        for char_name, char_class in self.characters.items():
            info = char_class.get_character_info()
            stats.append({
                "name": char_name,
                "health": info["health"],
                "archetype": info["archetype"],
                "playstyle": info.get("playstyle", ""),
                "strengths": info.get("strengths", []),
                "weaknesses": info.get("weaknesses", [])
            })
        return stats
    
    def compare_fastest_moves(self) -> Dict[str, List[Dict]]:
        """Get fastest moves for each character"""
        comparison = {}
        
        for char_name, char_class in self.characters.items():
            moves = char_class.get_moves()
            move_list = []
            
            for move_input, move_data in moves.items():
                # Include ALL moves, even with 0 startup (grabs, specials, etc.)
                move_list.append({
                    "move": move_input,
                    "name": move_data.name,
                    "startup": move_data.startup,
                    "recovery": move_data.recovery,
                    "on_block": move_data.on_block,
                    "is_safe": move_data.is_safe,
                    "requires_assist": move_data.requires_assist,
                    "damage": move_data.damage,
                    "risk_level": move_data.risk_level,
                    "description": move_data.description,
                    "usage_notes": move_data.usage_notes
                })
            
            # Sort by startup (fastest first), but moves with 0 startup go to end
            move_list.sort(key=lambda x: (x["startup"] if x["startup"] > 0 else 999, x["move"]))
            comparison[char_name] = move_list
        
        return comparison
    
    def get_fastest_moves_in_game(self, limit: int = 20) -> List[Dict]:
        """Get fastest moves across ALL characters, ranked globally"""
        all_moves = []
        
        for char_name, char_class in self.characters.items():
            moves = char_class.get_moves()
            
            for move_input, move_data in moves.items():
                # Only include moves with valid startup (> 0)
                if move_data.startup > 0:
                    all_moves.append({
                        "character": char_name,
                        "move": move_input,
                        "name": move_data.name,
                        "startup": move_data.startup,
                        "recovery": move_data.recovery,
                        "on_block": move_data.on_block,
                        "damage": move_data.damage,
                        "is_safe": move_data.is_safe,
                        "requires_assist": move_data.requires_assist,
                        "risk_level": move_data.risk_level,
                        "description": move_data.description
                    })
        
        # Sort by startup (fastest first)
        all_moves.sort(key=lambda x: x["startup"])
        
        # Return top N fastest moves
        return all_moves[:limit]
    
    def compare_safest_moves(self) -> Dict[str, List[Dict]]:
        """Get safest moves (best on block) for each character"""
        comparison = {}
        
        for char_name, char_class in self.characters.items():
            moves = char_class.get_moves()
            move_list = []
            
            for move_input, move_data in moves.items():
                move_list.append({
                    "move": move_input,
                    "name": move_data.name,
                    "on_block": move_data.on_block,
                    "startup": move_data.startup,
                    "recovery": move_data.recovery,
                    "is_safe": move_data.is_safe,
                    "requires_assist": move_data.requires_assist,
                    "usage_notes": move_data.usage_notes
                })
            
            # Sort by on_block (most plus first)
            move_list.sort(key=lambda x: x["on_block"], reverse=True)
            comparison[char_name] = move_list
        
        return comparison
    
    def compare_assist_dependent_moves(self) -> Dict[str, List[Dict]]:
        """Get moves that require assists for each character"""
        comparison = {}
        
        for char_name, char_class in self.characters.items():
            moves = char_class.get_moves()
            assist_moves = []
            
            for move_input, move_data in moves.items():
                if move_data.requires_assist or move_data.requires_setup:
                    assist_moves.append({
                        "move": move_input,
                        "name": move_data.name,
                        "requires_assist": move_data.requires_assist,
                        "requires_setup": move_data.requires_setup,
                        "risk_level": move_data.risk_level,
                        "usage_notes": move_data.usage_notes
                    })
            
            comparison[char_name] = assist_moves
        
        return comparison
    
    def compare_bnb_combos(self) -> Dict[str, List[Dict]]:
        """Compare BnB combos across characters"""
        comparison = {}
        
        for char_name, char_class in self.characters.items():
            combos = char_class.get_bnb_combos()
            combo_list = []
            
            for combo_id, combo_data in combos.items():
                combo_list.append({
                    "name": combo_data["name"],
                    "notation": combo_data["notation"],
                    "hits": combo_data["hits"],
                    "damage": combo_data.get("damage_estimate", "Unknown"),
                    "difficulty": combo_data["difficulty"],
                    "meter_use": combo_data.get("meter_use", 0),
                    "starter": combo_data["starter"],
                    "situation": combo_data["situation"]
                })
            
            # Sort by difficulty then hits
            combo_list.sort(key=lambda x: (x["difficulty"], -x["hits"]))
            comparison[char_name] = combo_list
        
        return comparison
    
    def get_move_efficiency_ranking(self, character: str) -> List[Dict]:
        """
        Rank moves by efficiency (speed + safety + damage)
        
        Args:
            character: Character name
        
        Returns:
            List of moves ranked by efficiency score
        """
        if character not in self.characters:
            return []
        
        char_class = self.characters[character]
        moves = char_class.get_moves()
        ranked = []
        
        for move_input, move_data in moves.items():
            # Calculate efficiency score
            # Lower startup = better, higher on_block = better, higher damage = better
            startup_score = max(0, 30 - move_data.startup) if move_data.startup > 0 else 0
            safety_score = move_data.on_block + 10  # Normalize so -10 = 0, +10 = 20
            damage_score = move_data.damage / 10 if move_data.damage > 0 else 0
            
            efficiency = startup_score + safety_score + damage_score
            
            ranked.append({
                "move": move_input,
                "name": move_data.name,
                "efficiency_score": round(efficiency, 1),
                "startup": move_data.startup,
                "on_block": move_data.on_block,
                "damage": move_data.damage,
                "recovery": move_data.recovery,
                "is_safe": move_data.is_safe,
                "requires_assist": move_data.requires_assist,
                "risk_level": move_data.risk_level,
                "description": move_data.description
            })
        
        # Sort by efficiency score (highest first)
        ranked.sort(key=lambda x: x["efficiency_score"], reverse=True)
        
        return ranked
    
    def generate_comparison_table_markdown(self, sort_by: str = "health") -> str:
        """
        Generate markdown comparison table
        
        Args:
            sort_by: "health", "name", "archetype"
        
        Returns:
            Markdown table string
        """
        stats = self.get_all_character_stats()
        
        # Sort
        if sort_by == "health":
            stats.sort(key=lambda x: x["health"], reverse=True)
        elif sort_by == "name":
            stats.sort(key=lambda x: x["name"])
        elif sort_by == "archetype":
            stats.sort(key=lambda x: x["archetype"])
        
        # Build table
        lines = []
        lines.append("# Character Comparison Table")
        lines.append("")
        lines.append("| Character | Health | Archetype | Playstyle |")
        lines.append("|-----------|--------|-----------|-----------|")
        
        for char in stats:
            playstyle_short = char["playstyle"][:50] + "..." if len(char["playstyle"]) > 50 else char["playstyle"]
            lines.append(f"| {char['name']} | {char['health']} | {char['archetype']} | {playstyle_short} |")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Fastest moves comparison
        lines.append("## Fastest Moves by Character")
        lines.append("")
        fastest = self.compare_fastest_moves()
        
        for char_name, moves in fastest.items():
            if moves:
                fastest_move = moves[0]
                lines.append(f"**{char_name}**: {fastest_move['move']} ({fastest_move['startup']}f startup, {fastest_move['on_block']:+d} on block)")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Safest moves comparison
        lines.append("## Safest Moves by Character")
        lines.append("")
        safest = self.compare_safest_moves()
        
        for char_name, moves in safest.items():
            if moves:
                safest_move = moves[0]
                lines.append(f"**{char_name}**: {safest_move['move']} ({safest_move['on_block']:+d} on block)")
        
        return "\n".join(lines)
    
    def generate_move_comparison_json(self) -> str:
        """Generate JSON with all comparison data"""
        data = {
            "characters": self.get_all_character_stats(),
            "fastest_moves": self.compare_fastest_moves(),
            "safest_moves": self.compare_safest_moves(),
            "assist_dependent": self.compare_assist_dependent_moves(),
            "bnb_combos": self.compare_bnb_combos()
        }
        
        return json.dumps(data, indent=2)
    
    def get_character_summary(self, character: str) -> Dict:
        """Get complete summary for one character"""
        if character not in self.characters:
            return {"error": f"Character {character} not found"}
        
        char_class = self.characters[character]
        
        return {
            "info": char_class.get_character_info(),
            "moves": {k: {
                "name": v.name,
                "startup": v.startup,
                "recovery": v.recovery,
                "on_block": v.on_block,
                "damage": v.damage,
                "is_safe": v.is_safe,
                "requires_assist": v.requires_assist,
                "risk_level": v.risk_level,
                "description": v.description,
                "usage_notes": v.usage_notes,
                "is_special": v.is_special,
                "is_grab": v.is_grab,
                "range": v.range,
                "is_gap_closer": v.is_gap_closer,
                "is_antiair": v.is_antiair
            } for k, v in char_class.get_moves().items()},
            "bnb_combos": char_class.get_bnb_combos(),
            "recommendations": char_class.get_move_recommendations(),
            "efficiency_ranking": self.get_move_efficiency_ranking(character)
        }
