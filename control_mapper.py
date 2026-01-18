"""
Keyboard control mapping system for 2XKO.
Allows users to customize controls and see moves with their custom mappings.
"""

import json
from typing import Dict, List
from dataclasses import dataclass, asdict


@dataclass
class ControlScheme:
    """Represents a keyboard control scheme"""
    name: str
    # Movement
    up: str
    down: str
    left: str
    right: str
    # Attacks
    light: str
    medium: str
    heavy: str
    special: str
    # Actions
    grab: str
    parry: str
    break_action: str
    tag: str
    # Modifier (for charged moves)
    charge_modifier: str = "Hold "
    

# Default 2XKO keyboard controls
DEFAULT_CONTROLS = ControlScheme(
    name="Default 2XKO",
    up="W",
    down="S",
    left="A",
    right="D",
    light="J",
    medium="K",
    heavy="L",
    special="M",
    grab="I",
    parry="U",
    break_action="O",
    tag="T",
    charge_modifier="Hold "
)

# Alternative common schemes
ALTERNATIVE_SCHEMES = {
    "WASD_UIOP": ControlScheme(
        name="WASD + UIOP",
        up="W", down="S", left="A", right="D",
        light="U", medium="I", heavy="O", special="P",
        grab="[", parry="]", break_action="\\", tag="Enter"
    ),
    "Arrow_Keys": ControlScheme(
        name="Arrow Keys",
        up="↑", down="↓", left="←", right="→",
        light="Z", medium="X", heavy="C", special="V",
        grab="A", parry="S", break_action="D", tag="F"
    ),
    "Numpad": ControlScheme(
        name="Numpad Layout",
        up="8", down="2", left="4", right="6",
        light="7", medium="4", heavy="1", special="0",
        grab="9", parry="3", break_action=".", tag="Enter"
    ),
    "FGC_Hitbox": ControlScheme(
        name="Hitbox Style",
        up="Space", down="V", left="D", right="F",
        light="U", medium="I", heavy="O", special="P",
        grab="J", parry="K", break_action="L", tag=";"
    )
}


class ControlMapper:
    """Maps move notation to keyboard controls"""
    
    def __init__(self, control_scheme: ControlScheme = DEFAULT_CONTROLS):
        self.controls = control_scheme
    
    def parse_direction(self, notation: str) -> str:
        """
        Parse directional input from notation
        
        Examples:
        - "5" = neutral (no direction)
        - "2" = down
        - "6" = forward
        - "8" = up
        - "j." = jump
        """
        if notation.startswith("j."):
            return f"Press {self.controls.up}, then "
        
        direction_map = {
            "1": f"{self.controls.down}+{self.controls.left}",  # Down-back
            "2": self.controls.down,  # Down
            "3": f"{self.controls.down}+{self.controls.right}",  # Down-forward
            "4": self.controls.left,  # Back
            "5": "",  # Neutral (no direction)
            "6": self.controls.right,  # Forward
            "7": f"{self.controls.up}+{self.controls.left}",  # Up-back
            "8": self.controls.up,  # Up
            "9": f"{self.controls.up}+{self.controls.right}",  # Up-forward
        }
        
        # Get first character as direction
        if notation and notation[0] in direction_map:
            return direction_map[notation[0]]
        
        return ""
    
    def parse_button(self, notation: str) -> str:
        """
        Parse button input from notation
        
        Examples:
        - "L" = Light
        - "M" = Medium
        - "H" = Heavy
        - "S1" or "S" = Special
        """
        button_map = {
            "L": self.controls.light,
            "M": self.controls.medium,
            "H": self.controls.heavy,
            "S": self.controls.special,
            "S1": self.controls.special,
            "S2": self.controls.special,
        }
        
        # Find button in notation
        for button_key, button_value in button_map.items():
            if button_key in notation:
                return button_value
        
        # Check for grab
        if "grab" in notation.lower() or "throw" in notation.lower():
            return self.controls.grab
        
        return ""
    
    def notation_to_keys(self, notation: str, is_charged: bool = False) -> str:
        """
        Convert FGC notation to keyboard instructions
        
        Examples:
        - "5L" -> "Press J"
        - "2S1" -> "Hold S + Press M"
        - "j.H" -> "Press W, then Press L"
        """
        direction = self.parse_direction(notation)
        button = self.parse_button(notation)
        
        if not button:
            return f"[Unknown: {notation}]"
        
        # Build instruction
        if is_charged:
            if direction:
                return f"{self.controls.charge_modifier}{direction} + {self.controls.charge_modifier}{button}"
            return f"{self.controls.charge_modifier}{button}"
        
        if direction:
            if notation.startswith("j."):
                # Jumping move
                return f"{direction}{button}"
            else:
                # Directional move (hold direction + press button)
                return f"Hold {direction} + Press {button}"
        else:
            # No direction (neutral)
            return f"Press {button}"
    
    def combo_to_keys(self, combo_notation: str) -> str:
        """
        Convert combo notation to keyboard sequence
        
        Examples:
        - "5L > 5M > 5S1" -> "Press J > Press K > Press M"
        - "2L, 2M, j.H" -> "Hold S+Press J, Hold S+Press K, Press W then Press L"
        """
        # Split combo by common separators
        moves = combo_notation.replace(" > ", ",").replace(">", ",").split(",")
        
        key_sequence = []
        for move in moves:
            move = move.strip()
            is_charged = "charge" in move.lower() or "[" in move
            key_sequence.append(self.notation_to_keys(move, is_charged))
        
        return " > ".join(key_sequence)
    
    def get_control_legend(self) -> Dict:
        """Get legend showing all controls"""
        return {
            "Movement": {
                "Up/Jump": self.controls.up,
                "Down/Crouch": self.controls.down,
                "Left/Back": self.controls.left,
                "Right/Forward": self.controls.right
            },
            "Attacks": {
                "Light": self.controls.light,
                "Medium": self.controls.medium,
                "Heavy": self.controls.heavy,
                "Special": self.controls.special
            },
            "Actions": {
                "Grab/Throw": self.controls.grab,
                "Parry": self.controls.parry,
                "Break": self.controls.break_action,
                "Tag/Assist": self.controls.tag
            }
        }
    
    def save_scheme(self, filename: str):
        """Save control scheme to JSON"""
        with open(filename, 'w') as f:
            json.dump(asdict(self.controls), f, indent=2)
    
    @classmethod
    def load_scheme(cls, filename: str) -> 'ControlMapper':
        """Load control scheme from JSON"""
        with open(filename, 'r') as f:
            data = json.load(f)
            scheme = ControlScheme(**data)
            return cls(scheme)


def generate_custom_move_list(character_data, control_mapper: ControlMapper) -> str:
    """Generate move list with custom keyboard controls"""
    moves = character_data.get_moves()
    
    lines = []
    lines.append(f"# {character_data.get_character_info()['name']} - Custom Control Move List")
    lines.append("")
    lines.append(f"**Control Scheme**: {control_mapper.controls.name}")
    lines.append("")
    
    # Show control legend
    lines.append("## 🎮 Your Custom Controls")
    lines.append("")
    legend = control_mapper.get_control_legend()
    
    for category, controls in legend.items():
        lines.append(f"### {category}")
        for action, key in controls.items():
            lines.append(f"- **{action}**: {key}")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Basic Moves
    lines.append("## 🥊 Basic Moves")
    lines.append("")
    
    for move_input, move_data in moves.items():
        if not move_data.is_special and not move_data.is_super:
            keyboard_input = control_mapper.notation_to_keys(move_input)
            lines.append(f"### {move_data.name}")
            lines.append(f"- **Notation**: {move_input}")
            lines.append(f"- **Your Keys**: {keyboard_input}")
            lines.append(f"- **What it does**: {move_data.description}")
            lines.append("")
    
    # Special Moves
    lines.append("## ⚡ Special Moves")
    lines.append("")
    
    for move_input, move_data in moves.items():
        if move_data.is_special:
            keyboard_input = control_mapper.notation_to_keys(move_input)
            lines.append(f"### {move_data.name}")
            lines.append(f"- **Notation**: {move_input}")
            lines.append(f"- **Your Keys**: {keyboard_input}")
            lines.append(f"- **Usage**: {move_data.usage_notes}")
            lines.append("")
    
    # BnB Combos
    lines.append("## 💥 BnB Combos (With Your Controls)")
    lines.append("")
    
    combos = character_data.get_bnb_combos()
    sorted_combos = sorted(combos.items(), key=lambda x: x[1]['difficulty'])
    
    for combo_id, combo in sorted_combos:
        keyboard_combo = control_mapper.combo_to_keys(combo['notation'])
        lines.append(f"### {combo['name']}")
        lines.append(f"- **Notation**: {combo['notation']}")
        lines.append(f"- **Your Keys**: {keyboard_combo}")
        lines.append(f"- **Difficulty**: {'*' * combo['difficulty']}")
        lines.append(f"- **Situation**: {combo['situation']}")
        lines.append("")
    
    return "\n".join(lines)


def save_all_schemes():
    """Generate move lists for all control schemes"""
    from character_data import BlitzcrankData
    
    schemes = {
        "default": DEFAULT_CONTROLS,
        **ALTERNATIVE_SCHEMES
    }
    
    for scheme_id, scheme in schemes.items():
        mapper = ControlMapper(scheme)
        content = generate_custom_move_list(BlitzcrankData, mapper)
        
        filename = f"output/Blitzcrank_controls_{scheme_id}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[OK] Generated: {filename}")


if __name__ == "__main__":
    from character_data import BlitzcrankData
    
    # Generate for default controls
    mapper = ControlMapper(DEFAULT_CONTROLS)
    content = generate_custom_move_list(BlitzcrankData, mapper)
    
    with open("output/Blitzcrank_custom_controls.md", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[OK] Custom control move list generated!")
    print("\nTo generate all schemes, run:")
    print("  python control_mapper.py --all")
    
    # Show example
    print("\nExample conversions:")
    print(f"5L = {mapper.notation_to_keys('5L')}")
    print(f"2S1 = {mapper.notation_to_keys('2S1')}")
    print(f"j.H = {mapper.notation_to_keys('j.H')}")
    print(f"Combo: {mapper.combo_to_keys('5L > 5M > 5S1')}")
