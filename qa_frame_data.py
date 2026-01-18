"""
QA script to validate all characters' frame data and identify safest/dangerous moves.
"""

import json
from typing import Dict, List, Tuple
from character_data import CHARACTER_DATA

def validate_frame_data(character_name: str, moves: Dict) -> Tuple[List[str], List[Dict]]:
    """Validate frame data for a character"""
    errors = []
    warnings = []
    
    for move_input, move_data in moves.items():
        # Check startup
        if move_data.startup < 0:
            errors.append(f"{character_name} {move_input}: Negative startup ({move_data.startup})")
        elif move_data.startup == 0 and not move_data.is_grab:
            warnings.append(f"{character_name} {move_input}: 0f startup (might be grab/special)")
        
        # Check recovery
        if move_data.recovery < 0:
            errors.append(f"{character_name} {move_input}: Negative recovery ({move_data.recovery})")
        elif move_data.recovery == 0:
            warnings.append(f"{character_name} {move_input}: 0f recovery (unusual)")
        
        # Check active frames
        if move_data.active < 0:
            errors.append(f"{character_name} {move_input}: Negative active frames ({move_data.active})")
        elif move_data.active == 0:
            warnings.append(f"{character_name} {move_input}: 0 active frames (might be instant)")
        
        # Check damage
        if move_data.damage < 0:
            errors.append(f"{character_name} {move_input}: Negative damage ({move_data.damage})")
        
        # Check guard types
        if not move_data.guard:
            warnings.append(f"{character_name} {move_input}: No guard types specified")
        
        # Check on_block makes sense with is_safe
        if move_data.on_block >= 0 and not move_data.is_safe:
            warnings.append(f"{character_name} {move_input}: on_block >= 0 but is_safe=False (should be safe)")
        elif move_data.on_block < 0 and move_data.is_safe and not move_data.is_grab:
            warnings.append(f"{character_name} {move_input}: on_block < 0 but is_safe=True (might be error)")
    
    return errors, warnings


def identify_safest_moves(character_name: str, moves: Dict) -> List[Dict]:
    """Identify safest moves (best on block)"""
    move_list = []
    
    for move_input, move_data in moves.items():
        # Skip grabs (they're unblockable, on_block doesn't apply)
        if move_data.is_grab:
            continue
        
        move_list.append({
            "move": move_input,
            "name": move_data.name,
            "on_block": move_data.on_block,
            "startup": move_data.startup,
            "recovery": move_data.recovery,
            "damage": move_data.damage,
            "is_safe": move_data.is_safe,
            "description": move_data.description
        })
    
    # Sort by on_block (highest first)
    move_list.sort(key=lambda x: x["on_block"], reverse=True)
    
    return move_list


def identify_most_dangerous_moves(character_name: str, moves: Dict) -> List[Dict]:
    """Identify most dangerous moves (worst on block, need assist)"""
    dangerous_moves = []
    
    for move_input, move_data in moves.items():
        # Skip grabs (they're unblockable)
        if move_data.is_grab:
            continue
        
        # Consider dangerous if:
        # 1. Very negative on block (< -8)
        # 2. Requires assist
        # 3. High risk level
        # 4. Long recovery
        
        danger_score = 0
        
        # On block penalty
        if move_data.on_block < -10:
            danger_score += 3
        elif move_data.on_block < -8:
            danger_score += 2
        elif move_data.on_block < -5:
            danger_score += 1
        
        # Recovery penalty
        if move_data.recovery > 30:
            danger_score += 2
        elif move_data.recovery > 20:
            danger_score += 1
        
        # Risk level
        if move_data.risk_level == "high":
            danger_score += 3
        elif move_data.risk_level == "medium":
            danger_score += 1
        
        # Requires assist
        if move_data.requires_assist:
            danger_score += 3
        
        if danger_score >= 3:  # Threshold for "dangerous"
            dangerous_moves.append({
                "move": move_input,
                "name": move_data.name,
                "on_block": move_data.on_block,
                "recovery": move_data.recovery,
                "risk_level": move_data.risk_level,
                "requires_assist": move_data.requires_assist,
                "danger_score": danger_score,
                "description": move_data.description,
                "usage_notes": move_data.usage_notes
            })
    
    # Sort by danger score (highest first)
    dangerous_moves.sort(key=lambda x: x["danger_score"], reverse=True)
    
    return dangerous_moves


def analyze_all_characters() -> Dict:
    """Analyze all characters"""
    results = {
        "validation": {},
        "safest_moves": {},
        "dangerous_moves": {},
        "summary": {
            "total_characters": 0,
            "total_errors": 0,
            "total_warnings": 0
        }
    }
    
    for char_name, char_class in CHARACTER_DATA.items():
        moves = char_class.get_moves()
        
        # Validate
        errors, warnings = validate_frame_data(char_name, moves)
        results["validation"][char_name] = {
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings)
        }
        
        # Safest moves
        safest = identify_safest_moves(char_name, moves)
        results["safest_moves"][char_name] = safest[:5]  # Top 5 safest
        
        # Dangerous moves
        dangerous = identify_most_dangerous_moves(char_name, moves)
        results["dangerous_moves"][char_name] = dangerous
        
        # Update summary
        results["summary"]["total_characters"] += 1
        results["summary"]["total_errors"] += len(errors)
        results["summary"]["total_warnings"] += len(warnings)
    
    return results


def print_qa_report(results: Dict):
    """Print comprehensive QA report"""
    print("="*70)
    print("FRAME DATA QA REPORT")
    print("="*70)
    
    # Validation Summary
    print("\n[VALIDATION] Frame Data Validation")
    print("-"*70)
    
    all_errors = []
    all_warnings = []
    
    for char_name, validation in results["validation"].items():
        if validation["errors"]:
            print(f"\n[ERROR] {char_name}:")
            for error in validation["errors"]:
                print(f"  - {error}")
                all_errors.append(error)
        
        if validation["warnings"]:
            print(f"\n[WARN] {char_name}:")
            for warning in validation["warnings"]:
                print(f"  - {warning}")
                all_warnings.append(warning)
    
    if not all_errors and not all_warnings:
        print("[OK] No validation errors or warnings found!")
    
    # Safest Moves
    print("\n" + "="*70)
    print("[SAFEST MOVES] Top Safest Moves Per Character")
    print("-"*70)
    
    for char_name, safest in results["safest_moves"].items():
        if safest:
            top_safe = safest[0]
            print(f"\n{char_name}:")
            print(f"  Safest: {top_safe['move']} ({top_safe['name']})")
            print(f"    On Block: {top_safe['on_block']:+d}")
            print(f"    Startup: {top_safe['startup']}f, Recovery: {top_safe['recovery']}f")
            if safest[1:]:
                print(f"  Other safe moves:")
                for move in safest[1:3]:  # Show next 2
                    print(f"    - {move['move']}: {move['on_block']:+d} on block")
    
    # Dangerous Moves
    print("\n" + "="*70)
    print("[DANGEROUS MOVES] Moves That Need Assist/Special Care")
    print("-"*70)
    
    for char_name, dangerous in results["dangerous_moves"].items():
        if dangerous:
            print(f"\n{char_name}:")
            for move in dangerous[:3]:  # Top 3 most dangerous
                print(f"  {move['move']} ({move['name']})")
                print(f"    Danger Score: {move['danger_score']}/10")
                print(f"    On Block: {move['on_block']:+d}")
                print(f"    Recovery: {move['recovery']}f")
                print(f"    Risk Level: {move['risk_level'].upper()}")
                print(f"    Requires Assist: {'YES' if move['requires_assist'] else 'NO'}")
                if move['usage_notes']:
                    print(f"    Usage: {move['usage_notes'][:100]}...")
        else:
            print(f"\n{char_name}: No highly dangerous moves identified")
    
    # Summary
    print("\n" + "="*70)
    print("[SUMMARY]")
    print("-"*70)
    print(f"Total Characters: {results['summary']['total_characters']}")
    print(f"Total Errors: {results['summary']['total_errors']}")
    print(f"Total Warnings: {results['summary']['total_warnings']}")
    
    if results['summary']['total_errors'] == 0:
        print("[OK] No frame data errors found!")
    else:
        print(f"[ERROR] Found {results['summary']['total_errors']} errors that need fixing!")
    
    if results['summary']['total_warnings'] == 0:
        print("[OK] No frame data warnings!")
    else:
        print(f"[WARN] Found {results['summary']['total_warnings']} warnings to review")


def save_qa_report(results: Dict, filename: str = "output/QA_FRAME_DATA_REPORT.md"):
    """Save QA report to markdown file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Frame Data QA Report\n\n")
        f.write("## Validation Results\n\n")
        
        # Errors
        f.write("### Errors\n\n")
        has_errors = False
        for char_name, validation in results["validation"].items():
            if validation["errors"]:
                has_errors = True
                f.write(f"#### {char_name}\n\n")
                for error in validation["errors"]:
                    f.write(f"- {error}\n")
                f.write("\n")
        
        if not has_errors:
            f.write("✅ No errors found!\n\n")
        
        # Warnings
        f.write("### Warnings\n\n")
        has_warnings = False
        for char_name, validation in results["validation"].items():
            if validation["warnings"]:
                has_warnings = True
                f.write(f"#### {char_name}\n\n")
                for warning in validation["warnings"]:
                    f.write(f"- {warning}\n")
                f.write("\n")
        
        if not has_warnings:
            f.write("✅ No warnings found!\n\n")
        
        # Safest Moves
        f.write("## Safest Moves Per Character\n\n")
        f.write("Moves with best frame advantage on block.\n\n")
        
        for char_name, safest in results["safest_moves"].items():
            if safest:
                f.write(f"### {char_name}\n\n")
                f.write("| Move | Name | On Block | Startup | Recovery | Safe |\n")
                f.write("|------|------|----------|---------|----------|------|\n")
                for move in safest[:5]:
                    safe_mark = "✅" if move['is_safe'] else "❌"
                    f.write(f"| {move['move']} | {move['name']} | {move['on_block']:+d} | {move['startup']}f | {move['recovery']}f | {safe_mark} |\n")
                f.write("\n")
        
        # Dangerous Moves
        f.write("## Most Dangerous Moves Per Character\n\n")
        f.write("Moves that are unsafe on block and may need assist cover.\n\n")
        
        for char_name, dangerous in results["dangerous_moves"].items():
            if dangerous:
                f.write(f"### {char_name}\n\n")
                f.write("| Move | Name | On Block | Recovery | Risk | Needs Assist | Danger Score |\n")
                f.write("|------|------|----------|----------|------|--------------|--------------|\n")
                for move in dangerous:
                    assist_mark = "⚠️ YES" if move['requires_assist'] else "No"
                    f.write(f"| {move['move']} | {move['name']} | {move['on_block']:+d} | {move['recovery']}f | {move['risk_level'].upper()} | {assist_mark} | {move['danger_score']}/10 |\n")
                f.write("\n")
            else:
                f.write(f"### {char_name}\n\n")
                f.write("✅ No highly dangerous moves identified.\n\n")
        
        # Summary
        f.write("## Summary\n\n")
        f.write(f"- **Total Characters**: {results['summary']['total_characters']}\n")
        f.write(f"- **Total Errors**: {results['summary']['total_errors']}\n")
        f.write(f"- **Total Warnings**: {results['summary']['total_warnings']}\n")
        
        if results['summary']['total_errors'] == 0:
            f.write("\n✅ **All frame data is valid!**\n")
    
    print(f"\n[OK] QA report saved to: {filename}")


if __name__ == "__main__":
    print("Running Frame Data QA...")
    print("="*70)
    
    results = analyze_all_characters()
    print_qa_report(results)
    save_qa_report(results)
    
    print("\n" + "="*70)
    print("[OK] QA Complete!")
    print("="*70)
