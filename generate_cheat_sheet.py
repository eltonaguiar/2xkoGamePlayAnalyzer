"""
Generate cheat sheet from character data
"""

from character_data import BlitzcrankData, CHARACTER_DATA
import json


def generate_text_cheat_sheet(character_name: str) -> str:
    """Generate a text-based cheat sheet for a character"""
    
    if character_name not in CHARACTER_DATA:
        return f"Character {character_name} not found in database"
    
    char_data = CHARACTER_DATA[character_name]
    moves = char_data.get_moves()
    char_info = char_data.get_character_info()
    recommendations = char_data.get_move_recommendations()
    recovery_analysis = char_data.get_recovery_analysis()
    bnb_combos = char_data.get_bnb_combos()
    combo_goals = char_data.get_combo_goals()
    
    output = []
    output.append("=" * 80)
    output.append(f"{character_name.upper()} CHEAT SHEET")
    output.append("=" * 80)
    output.append("")
    
    # Character Info
    output.append(f"Archetype: {char_info['archetype']}")
    output.append(f"Health: {char_info['health']}")
    output.append(f"Playstyle: {char_info['playstyle']}")
    output.append("")
    
    # BnB Combos Section
    output.append("=" * 80)
    output.append("BNB COMBOS (BREAD AND BUTTER)")
    output.append("=" * 80)
    output.append("")
    
    # Sort combos by difficulty
    sorted_combos = sorted(bnb_combos.items(), key=lambda x: x[1]['difficulty'])
    
    for combo_id, combo in sorted_combos:
        difficulty_stars = "*" * combo['difficulty']  # Use * instead of emoji
        output.append(f"--- {combo['name']} ({'*' * combo['difficulty']} difficulty) ---")
        output.append(f"  Notation: {combo['notation']}")
        output.append(f"  English: {combo['english']}")
        output.append(f"  Hits: {combo['hits']}")
        output.append(f"  Damage: {combo['damage_estimate']}")
        output.append(f"  Situation: {combo['situation']}")
        output.append(f"  Notes: {combo['notes']}")
        output.append("")
    
    # Combo Goals by Skill Level
    output.append("--- COMBO GOALS BY SKILL LEVEL ---")
    output.append("")
    for level, goals in combo_goals.items():
        output.append(f"{level.upper()}:")
        output.append(f"  Average Combo Length: {goals['avg_combo_length']} hits")
        output.append(f"  Max Combo Length: {goals['max_combo_length']} hits")
        if isinstance(goals['combos_to_learn'], list):
            combos_list = ', '.join([bnb_combos[c]['name'] for c in goals['combos_to_learn'] 
                                    if c in bnb_combos])
            output.append(f"  Combos to Learn: {combos_list}")
        output.append("")
    
    # Move Data
    output.append("=" * 80)
    output.append("MOVE DATA WITH RECOVERY TIMES")
    output.append("=" * 80)
    output.append("")
    
    # Sort moves by risk level and type
    safe_moves = []
    unsafe_moves = []
    high_risk_moves = []
    
    for move_input, move_data in moves.items():
        move_info = {
            "input": move_input,
            "name": move_data.name,
            "data": move_data
        }
        
        if move_data.risk_level == "high":
            high_risk_moves.append(move_info)
        elif move_data.is_safe:
            safe_moves.append(move_info)
        else:
            unsafe_moves.append(move_info)
    
    # Display safe moves first
    if safe_moves:
        output.append("--- SAFE MOVES (Can use freely) ---")
        output.append("")
        for move_info in safe_moves:
            move = move_info["data"]
            output.append(f"{move_info['input']} - {move_info['name']}")
            output.append(f"  Recovery: {move.recovery} frames")
            output.append(f"  Total Frames: {move.startup + move.active + move.recovery}")
            output.append(f"  On Block: {move.on_block:+d} frames")
            output.append(f"  Risk Level: {move.risk_level.upper()}")
            if move.usage_notes:
                output.append(f"  Usage: {move.usage_notes}")
            output.append("")
    
    # Display unsafe but usable moves
    if unsafe_moves:
        output.append("--- UNSAFE MOVES (Use with caution) ---")
        output.append("")
        for move_info in unsafe_moves:
            move = move_info["data"]
            output.append(f"{move_info['input']} - {move_info['name']}")
            output.append(f"  Recovery: {move.recovery} frames")
            output.append(f"  Total Frames: {move.startup + move.active + move.recovery}")
            output.append(f"  On Block: {move.on_block:+d} frames")
            output.append(f"  Risk Level: {move.risk_level.upper()}")
            if move.usage_notes:
                output.append(f"  Usage: {move.usage_notes}")
            output.append("")
    
    # Display high risk moves
    if high_risk_moves:
        output.append("--- HIGH RISK MOVES (Only use with setup/assist) ---")
        output.append("")
        for move_info in high_risk_moves:
            move = move_info["data"]
            output.append(f"{move_info['input']} - {move_info['name']}")
            output.append(f"  Recovery: {move.recovery} frames")
            output.append(f"  Total Frames: {move.startup + move.active + move.recovery}")
            output.append(f"  On Block: {move.on_block:+d} frames")
            output.append(f"  Risk Level: {move.risk_level.upper()}")
            output.append(f"  Requires Assist: {move.requires_assist}")
            output.append(f"  Requires Setup: {move.requires_setup}")
            if move.usage_notes:
                output.append(f"  Usage: {move.usage_notes}")
            output.append("")
    
    # Strategic Recommendations
    output.append("=" * 80)
    output.append("STRATEGIC RECOMMENDATIONS")
    output.append("=" * 80)
    output.append("")
    
    output.append("SAFE TO USE FREELY:")
    for rec in recommendations["safe_to_use_freely"]:
        output.append(f"  - {rec}")
    output.append("")
    
    output.append("REQUIRES ASSIST COVER:")
    for rec in recommendations["requires_assist_cover"]:
        output.append(f"  - {rec}")
    output.append("")
    
    output.append("ONLY ON OPPONENT MISTAKE:")
    for rec in recommendations["only_on_opponent_mistake"]:
        output.append(f"  - {rec}")
    output.append("")
    
    output.append("ANTI-AIR OPTIONS:")
    for rec in recommendations["anti_air_options"]:
        output.append(f"  - {rec}")
    output.append("")
    
    # Punish Opportunities
    output.append("=" * 80)
    output.append("PUNISH OPPORTUNITIES")
    output.append("=" * 80)
    output.append("")
    
    punish = recommendations["punish_opportunities"]
    
    output.append("WHEN OPPONENT WHIFFS:")
    for rec in punish["opponent_whiffs"]:
        output.append(f"  - {rec}")
    output.append("")
    
    output.append("WHEN OPPONENT BLOCKS TOO MUCH:")
    for rec in punish["opponent_blocking_too_much"]:
        output.append(f"  - {rec}")
    output.append("")
    
    output.append("WHEN OPPONENT IS VERY MINUS:")
    for rec in punish["opponent_very_minus"]:
        output.append(f"  - {rec}")
    output.append("")
    
    # Frame Advantage Guide
    output.append("=" * 80)
    output.append("FRAME ADVANTAGE GUIDE")
    output.append("=" * 80)
    output.append("")
    output.append("+10 or more: HUGE advantage - guaranteed pressure or mixup")
    output.append("+1 to +9: Good advantage - your turn to attack")
    output.append("0 to -2: Slightly unsafe - can contest or retreat")
    output.append("-3 to -5: Unsafe - opponent can attack")
    output.append("-6 or worse: VERY UNSAFE - opponent gets full punish")
    output.append("")
    
    # Strengths and Weaknesses
    output.append("=" * 80)
    output.append("STRENGTHS")
    output.append("=" * 80)
    for strength in char_info["strengths"]:
        output.append(f"  + {strength}")
    output.append("")
    
    output.append("=" * 80)
    output.append("WEAKNESSES")
    output.append("=" * 80)
    for weakness in char_info["weaknesses"]:
        output.append(f"  - {weakness}")
    output.append("")
    
    return "\n".join(output)


def generate_json_cheat_sheet(character_name: str) -> str:
    """Generate a JSON-based cheat sheet for programmatic use"""
    
    if character_name not in CHARACTER_DATA:
        return json.dumps({"error": f"Character {character_name} not found"})
    
    char_data = CHARACTER_DATA[character_name]
    
    cheat_sheet = {
        "character": character_name,
        "info": char_data.get_character_info(),
        "moves": {},
        "recommendations": char_data.get_move_recommendations(),
        "recovery_analysis": char_data.get_recovery_analysis(),
        "bnb_combos": char_data.get_bnb_combos(),
        "combo_goals": char_data.get_combo_goals()
    }
    
    # Add move data
    moves = char_data.get_moves()
    for move_input, move_data in moves.items():
        cheat_sheet["moves"][move_input] = {
            "name": move_data.name,
            "input": move_data.input,
            "damage": move_data.damage,
            "startup": move_data.startup,
            "active": move_data.active,
            "recovery": move_data.recovery,
            "total_frames": move_data.startup + move_data.active + move_data.recovery,
            "on_block": move_data.on_block,
            "is_safe": move_data.is_safe,
            "is_special": move_data.is_special,
            "is_super": move_data.is_super,
            "is_grab": move_data.is_grab,
            "requires_assist": move_data.requires_assist,
            "requires_setup": move_data.requires_setup,
            "usage_notes": move_data.usage_notes,
            "risk_level": move_data.risk_level,
            "description": move_data.description
        }
    
    return json.dumps(cheat_sheet, indent=2)


def save_cheat_sheets(character_name: str = "Blitzcrank"):
    """Save both text and JSON cheat sheets to files"""
    
    # Generate text version
    text_output = generate_text_cheat_sheet(character_name)
    text_filename = f"output/{character_name}_cheat_sheet.txt"
    with open(text_filename, "w", encoding="utf-8") as f:
        f.write(text_output)
    print(f"Text cheat sheet saved to: {text_filename}")
    
    # Generate JSON version
    json_output = generate_json_cheat_sheet(character_name)
    json_filename = f"output/{character_name}_cheat_sheet.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        f.write(json_output)
    print(f"JSON cheat sheet saved to: {json_filename}")
    
    # Print text version to console
    print("\n" + text_output)


if __name__ == "__main__":
    import sys
    
    character = "Blitzcrank"
    if len(sys.argv) > 1:
        character = sys.argv[1]
    
    save_cheat_sheets(character)
