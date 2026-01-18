"""
Generate comprehensive character page with organized move lists,
strategies, matchups, and combos.
"""

import json
from character_data import BlitzcrankData, CHARACTER_DATA


def generate_character_page(character_name: str) -> str:
    """Generate comprehensive character page in markdown"""
    
    if character_name not in CHARACTER_DATA:
        return f"Character {character_name} not found"
    
    char_class = CHARACTER_DATA[character_name]
    char_info = char_class.get_character_info()
    moves = char_class.get_moves()
    combos = char_class.get_bnb_combos()
    strategies = char_class.get_top_strategies()
    most_used = char_class.get_most_used_moves()
    matchups = char_class.get_matchup_guide()
    
    lines = []
    lines.append(f"# {character_name} - Complete Character Guide")
    lines.append("")
    lines.append("="*80)
    lines.append(f"**{char_info['name']}** - {char_info['archetype']}")
    lines.append("="*80)
    lines.append("")
    
    # Character Overview
    lines.append("## 📊 Character Overview")
    lines.append("")
    lines.append(f"**Health**: {char_info['health']} HP")
    lines.append(f"**Archetype**: {char_info['archetype']}")
    lines.append(f"**Dash Speed**: {char_info['dash_speed']}")
    lines.append(f"**Defense Rating**: {char_info['defense_rating']}")
    lines.append(f"**Playstyle**: {char_info['playstyle']}")
    lines.append("")
    
    lines.append("**Strengths:**")
    for strength in char_info['strengths']:
        lines.append(f"- {strength}")
    lines.append("")
    
    lines.append("**Weaknesses:**")
    for weakness in char_info['weaknesses']:
        lines.append(f"- {weakness}")
    lines.append("")
    
    # Top 3 Strategies
    lines.append("="*80)
    lines.append("## 🎯 TOP 3 STRATEGIES")
    lines.append("="*80)
    lines.append("")
    
    for strategy in strategies:
        lines.append(f"### {strategy['name']}")
        lines.append(f"**Difficulty**: {strategy['difficulty']} | **Success Rate**: {strategy['success_rate']}")
        lines.append("")
        lines.append(f"**Description**: {strategy['description']}")
        lines.append("")
        lines.append(f"**Key Moves**: {', '.join(strategy['key_moves'])}")
        lines.append("")
        lines.append("**How to Execute:**")
        for i, step in enumerate(strategy['execution'], 1):
            lines.append(f"{i}. {step}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Most Used Moves
    lines.append("="*80)
    lines.append("## 🔥 MOST FREQUENTLY USED MOVES")
    lines.append("="*80)
    lines.append("")
    
    lines.append("### In Neutral Game (Mid-Long Range):")
    lines.append("")
    for move_info in most_used['neutral_game']:
        lines.append(f"**{move_info['move']}**")
        lines.append(f"- **Frequency**: {move_info['usage_frequency']}")
        lines.append(f"- **Purpose**: {move_info['purpose']}")
        lines.append(f"- **When**: {move_info['when_to_use']}")
        lines.append("")
    
    lines.append("### In Pressure Game (Close Range):")
    lines.append("")
    for move_info in most_used['pressure_game']:
        lines.append(f"**{move_info['move']}**")
        lines.append(f"- **Frequency**: {move_info['usage_frequency']}")
        lines.append(f"- **Purpose**: {move_info['purpose']}")
        lines.append(f"- **When**: {move_info['when_to_use']}")
        lines.append("")
    
    lines.append("### Variety / Mix-up Options:")
    lines.append("")
    for move_info in most_used['variety_options']:
        lines.append(f"**{move_info['move']}**")
        lines.append(f"- **Frequency**: {move_info['usage_frequency']}")
        lines.append(f"- **Purpose**: {move_info['purpose']}")
        lines.append(f"- **When**: {move_info['when_to_use']}")
        lines.append("")
    
    # Basic Moves Section
    lines.append("="*80)
    lines.append("## 🥊 BASIC MOVES (Normals)")
    lines.append("="*80)
    lines.append("")
    lines.append("*Start here! Learn these before advanced combos*")
    lines.append("")
    
    # Organize moves by category
    normal_moves = {k: v for k, v in moves.items() if not v.is_special and not v.is_super}
    
    # Standing normals
    lines.append("### Standing Normals (No Direction Held)")
    lines.append("")
    lines.append("| Move | Startup | Recovery | On Block | Damage | Safety | Range | Notes |")
    lines.append("|------|---------|----------|----------|---------|--------|-------|-------|")
    
    for move_input in ["5L", "5M", "5H"]:
        if move_input in normal_moves:
            m = normal_moves[move_input]
            safety = "SAFE" if m.is_safe else "UNSAFE" if m.on_block < -5 else "NEUTRAL"
            lines.append(f"| **{move_input}** | {m.startup}f | {m.recovery}f | {m.on_block:+d}f | {m.damage} | {safety} | {m.range} | {m.usage_notes[:40]}... |")
    
    lines.append("")
    
    # Crouching normals
    lines.append("### Crouching Normals (Hold Down)")
    lines.append("")
    lines.append("| Move | Startup | Recovery | On Block | Damage | Safety | Range | Notes |")
    lines.append("|------|---------|----------|----------|---------|--------|-------|-------|")
    
    for move_input in ["2L", "2M", "2H"]:
        if move_input in moves:
            m = moves[move_input]
            safety = "SAFE" if m.is_safe else "UNSAFE" if m.on_block < -5 else "NEUTRAL"
            lines.append(f"| **{move_input}** | {m.startup}f | {m.recovery}f | {m.on_block:+d}f | {m.damage} | {safety} | {m.range} | Low attack |")
    
    lines.append("")
    
    # Special Moves Section
    lines.append("="*80)
    lines.append("## ⚡ SPECIAL MOVES")
    lines.append("="*80)
    lines.append("")
    
    special_moves = {k: v for k, v in moves.items() if v.is_special and not v.is_super}
    
    for move_input, move_data in special_moves.items():
        lines.append(f"### {move_input} - {move_data.name}")
        lines.append("")
        lines.append(f"**Frame Data:**")
        lines.append(f"- Startup: {move_data.startup}f" if move_data.startup > 0 else "- Startup: Unknown")
        lines.append(f"- Recovery: {move_data.recovery}f" if move_data.recovery > 0 else "- Recovery: Unknown")
        lines.append(f"- On Block: {move_data.on_block:+d}f" if move_data.on_block != 0 else "- On Block: N/A (Grab)")
        lines.append(f"- Damage: {move_data.damage}" if move_data.damage > 0 else "- Damage: Unknown")
        lines.append("")
        
        lines.append(f"**Properties:**")
        lines.append(f"- Range: {move_data.range.capitalize()}")
        lines.append(f"- Risk Level: {move_data.risk_level.upper()}")
        lines.append(f"- Safe on Block: {'YES' if move_data.is_safe else 'NO'}")
        lines.append(f"- Requires Assist: {'YES - Use with setup!' if move_data.requires_assist else 'NO'}")
        if move_data.is_gap_closer:
            lines.append(f"- Gap Closer: YES - Good for closing distance")
        if move_data.is_antiair:
            lines.append(f"- Anti-Air: YES - Use vs jumpers")
        if move_data.is_pressure_tool:
            lines.append(f"- Pressure Tool: YES")
        lines.append("")
        
        lines.append(f"**Usage**: {move_data.usage_notes}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # BnB Combos Section
    lines.append("="*80)
    lines.append("## 💥 BNB COMBOS (Bread and Butter)")
    lines.append("="*80)
    lines.append("")
    lines.append("*Learn in order of difficulty!*")
    lines.append("")
    
    # Sort by difficulty
    sorted_combos = sorted(combos.items(), key=lambda x: x[1]['difficulty'])
    
    for combo_id, combo in sorted_combos:
        diff_stars = "*" * combo['difficulty']
        lines.append(f"### {combo['name']} ({diff_stars} Difficulty)")
        lines.append("")
        lines.append(f"**Notation**: `{combo['notation']}`")
        lines.append(f"**Plain English**: {combo['english']}")
        lines.append("")
        lines.append(f"**Stats:**")
        lines.append(f"- Hits: {combo['hits']}")
        lines.append(f"- Damage: {combo['damage_estimate']}")
        lines.append(f"- Meter Use: {'Yes' if combo['meter_use'] > 0 else 'No'}")
        lines.append(f"- Difficulty: {diff_stars} ({combo['difficulty']}/5)")
        lines.append("")
        lines.append(f"**When to Use**: {combo['situation']}")
        lines.append(f"**Notes**: {combo['notes']}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Matchup Guide
    lines.append("="*80)
    lines.append("## ⚔️ MATCHUP GUIDE")
    lines.append("="*80)
    lines.append("")
    
    lines.append("### Tough Matchups:")
    lines.append("")
    for matchup in matchups['tough_matchups']:
        lines.append(f"#### vs {matchup['opponent']} - {matchup['difficulty']}")
        lines.append("")
        lines.append(f"**Why Difficult**: {matchup['why_difficult']}")
        lines.append("")
        lines.append(f"**Counter-Strategy**: {matchup['counter_strategy']['gameplan']}")
        lines.append("")
        lines.append("**Key Points:**")
        for point in matchup['counter_strategy']['key_points']:
            lines.append(f"- {point}")
        lines.append("")
        lines.append(f"**Moves to Use**: {', '.join(matchup['counter_strategy']['moves_to_use'])}")
        lines.append(f"**Moves to Avoid**: {', '.join(matchup['counter_strategy']['moves_to_avoid'])}")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    lines.append("### Favorable Matchups:")
    lines.append("")
    for matchup in matchups['favorable_matchups']:
        lines.append(f"#### vs {matchup['opponent']}")
        lines.append(f"- **Advantage**: {matchup['advantage']}")
        lines.append(f"- **How to Exploit**: {matchup['exploitation']}")
        lines.append("")
    
    lines.append("### Universal Tips:")
    lines.append("")
    for tip in matchups['universal_tips']:
        lines.append(f"- {tip}")
    lines.append("")
    
    # Move Rankings
    lines.append("="*80)
    lines.append("## 📈 MOVE RANKINGS")
    lines.append("="*80)
    lines.append("")
    
    # Fastest moves
    lines.append("### Fastest Moves (By Startup):")
    lines.append("")
    moves_with_startup = [(k, v) for k, v in moves.items() if v.startup > 0]
    moves_with_startup.sort(key=lambda x: x[1].startup)
    
    for i, (move_input, move_data) in enumerate(moves_with_startup[:5], 1):
        lines.append(f"{i}. **{move_input}** ({move_data.name}) - {move_data.startup}f startup")
    lines.append("")
    
    # Safest moves
    lines.append("### Safest Moves (By Frame Advantage):")
    lines.append("")
    moves_sorted = sorted(moves.items(), key=lambda x: x[1].on_block, reverse=True)
    
    for i, (move_input, move_data) in enumerate(moves_sorted[:5], 1):
        if move_data.on_block != 0 or i == 1:
            lines.append(f"{i}. **{move_input}** ({move_data.name}) - {move_data.on_block:+d}f on block")
    lines.append("")
    
    # Gap closers
    lines.append("### Gap Closers (Good for Approaching):")
    lines.append("")
    gap_closers = [(k, v) for k, v in moves.items() if v.is_gap_closer]
    for move_input, move_data in gap_closers:
        lines.append(f"- **{move_input}** ({move_data.name}) - Range: {move_data.range}")
    if not gap_closers:
        lines.append("- (No specific gap closers - use jump-ins or dash)")
    lines.append("")
    
    # Anti-airs
    lines.append("### Anti-Air Options:")
    lines.append("")
    antiairs = [(k, v) for k, v in moves.items() if v.is_antiair]
    for move_input, move_data in antiairs:
        lines.append(f"- **{move_input}** ({move_data.name}) - {move_data.on_block:+d}f on block")
    lines.append("")
    
    # Assist-dependent
    lines.append("### Moves Requiring Assist:")
    lines.append("")
    assist_moves = [(k, v) for k, v in moves.items() if v.requires_assist]
    for move_input, move_data in assist_moves:
        lines.append(f"- **{move_input}** ({move_data.name}) - Risk: {move_data.risk_level.upper()}")
    if not assist_moves:
        lines.append("- (No moves strictly require assist)")
    lines.append("")
    
    # Footer
    lines.append("="*80)
    lines.append(f"**Data Source**: https://wiki.play2xko.com")
    lines.append(f"**Last Updated**: 2026-01-17")
    lines.append("="*80)
    
    return "\n".join(lines)


def generate_character_page_json(character_name: str) -> str:
    """Generate character page data in JSON format"""
    
    if character_name not in CHARACTER_DATA:
        return json.dumps({"error": f"Character {character_name} not found"})
    
    char_class = CHARACTER_DATA[character_name]
    
    # Organize moves by category
    moves = char_class.get_moves()
    
    organized_moves = {
        "normals": {
            "standing": {},
            "crouching": {},
            "jumping": {}
        },
        "specials": {},
        "grabs": {},
        "universal": {}
    }
    
    for move_input, move_data in moves.items():
        move_dict = {
            "name": move_data.name,
            "startup": move_data.startup,
            "recovery": move_data.recovery,
            "on_block": move_data.on_block,
            "damage": move_data.damage,
            "is_safe": move_data.is_safe,
            "requires_assist": move_data.requires_assist,
            "risk_level": move_data.risk_level,
            "range": move_data.range,
            "is_gap_closer": move_data.is_gap_closer,
            "is_antiair": move_data.is_antiair,
            "is_pressure_tool": move_data.is_pressure_tool,
            "usage_notes": move_data.usage_notes,
            "description": move_data.description
        }
        
        # Categorize
        if move_data.is_grab:
            organized_moves["grabs"][move_input] = move_dict
        elif move_data.is_special:
            organized_moves["specials"][move_input] = move_dict
        elif move_input.startswith("j."):
            organized_moves["normals"]["jumping"][move_input] = move_dict
        elif move_input.startswith("2"):
            organized_moves["normals"]["crouching"][move_input] = move_dict
        elif move_input.startswith("5"):
            organized_moves["normals"]["standing"][move_input] = move_dict
        else:
            organized_moves["universal"][move_input] = move_dict
    
    page_data = {
        "character": character_name,
        "info": char_class.get_character_info(),
        "strategies": char_class.get_top_strategies(),
        "most_used_moves": char_class.get_most_used_moves(),
        "moves": organized_moves,
        "bnb_combos": char_class.get_bnb_combos(),
        "matchups": char_class.get_matchup_guide(),
        "combo_goals": char_class.get_combo_goals()
    }
    
    return json.dumps(page_data, indent=2)


def save_character_page(character_name: str = "Blitzcrank"):
    """Save character page in both formats"""
    
    # Markdown
    md_content = generate_character_page(character_name)
    md_file = f"output/{character_name}_COMPLETE_GUIDE.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"[OK] Markdown guide saved: {md_file}")
    
    # JSON
    json_content = generate_character_page_json(character_name)
    json_file = f"output/{character_name}_page_data.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json_content)
    print(f"[OK] JSON data saved: {json_file}")
    
    print(f"\n[OK] Complete character page generated for {character_name}!")
    
    return md_content


if __name__ == "__main__":
    import sys
    
    character = "Blitzcrank"
    if len(sys.argv) > 1:
        character = sys.argv[1]
    
    save_character_page(character)
