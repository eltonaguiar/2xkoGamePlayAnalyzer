"""
Translates FGC notation to plain English descriptions.
"""

from typing import Dict, Optional


class MoveTranslator:
    """Translates fighting game notation to plain English"""
    
    # Move name translations
    MOVE_NAMES = {
        # Normals
        "5L": "Light Punch",
        "5M": "Medium Punch", 
        "5H": "Heavy Punch",
        "2L": "Crouching Light Kick",
        "2M": "Crouching Medium Kick",
        "2H": "Crouching Heavy Kick",
        "j.L": "Jumping Light Attack",
        "j.M": "Jumping Medium Attack",
        "j.H": "Jumping Heavy Attack",
        "j.2H": "Jumping Down Heavy",
        
        # Specials
        "5S1": "Rocket Grab",
        "2S1": "Air Purifier (Down Special)",
        "2S2": "Garbage Collection (Command Grab)",
        "6S2": "Spinning Turbine",
        "j.S1": "Air Rocket Grab",
        "j.S2": "Wrecking Ball",
        
        # Supers
        "Super 1": "Helping Hand",
        "Super 2": "Static Field",
        
        # Universal
        "Throw": "Throw",
        "Air Throw": "Air Throw",
        "Tag": "Tag Assist",
        "Back Tag": "Back Tag Assist",
    }
    
    # Direction translations
    DIRECTIONS = {
        "5": "Neutral",
        "2": "Down",
        "6": "Forward",
        "4": "Back",
        "8": "Up",
        "j.": "Jumping",
    }
    
    # Button translations
    BUTTONS = {
        "L": "Light",
        "M": "Medium",
        "H": "Heavy",
        "S": "Special",
        "S1": "Special 1",
        "S2": "Special 2",
    }
    
    @classmethod
    def translate_move(cls, move_input: str) -> str:
        """
        Translate FGC notation to plain English
        
        Args:
            move_input: FGC notation (e.g., "5L", "2S1")
        
        Returns:
            Plain English description
        """
        # Check if we have a direct translation
        if move_input in cls.MOVE_NAMES:
            return cls.MOVE_NAMES[move_input]
        
        # Try to parse and translate
        if move_input.startswith("j."):
            direction = "Jumping"
            button = move_input[2:]
        elif len(move_input) >= 2 and move_input[0].isdigit():
            dir_num = move_input[0]
            direction = cls.DIRECTIONS.get(dir_num, "")
            button = move_input[1:]
        else:
            return move_input  # Return as-is if we can't translate
        
        # Translate button
        button_name = cls.BUTTONS.get(button, button)
        
        # Build description
        if direction:
            return f"{direction} {button_name}"
        else:
            return f"{button_name}"
    
    @classmethod
    def describe_move_sequence(cls, moves: list) -> str:
        """
        Describe a sequence of moves in plain English
        
        Args:
            moves: List of move inputs (e.g., ["5L", "2S2", "5L"])
        
        Returns:
            Plain English description
        """
        if not moves:
            return "No moves detected"
        
        translated = [cls.translate_move(m) for m in moves]
        
        if len(translated) == 1:
            return translated[0]
        elif len(translated) == 2:
            return f"{translated[0]}, then {translated[1]}"
        else:
            # Join with commas and "and" for last item
            return ", ".join(translated[:-1]) + f", and {translated[-1]}"
    
    @classmethod
    def describe_mistake_context(cls, mistake_move: str, opponent_response: list) -> str:
        """
        Describe a mistake in context with opponent's response
        
        Args:
            mistake_move: The move that was a mistake
            opponent_response: List of moves opponent did in response
        
        Returns:
            Plain English description
        """
        mistake_desc = cls.translate_move(mistake_move)
        
        if not opponent_response:
            return f"Used {mistake_desc}, but opponent did not respond"
        
        response_desc = cls.describe_move_sequence(opponent_response)
        
        return f"Used {mistake_desc}, then opponent responded with {response_desc}"
