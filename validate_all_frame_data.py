"""
Comprehensive frame data validation - identifies placeholder data and verifies accuracy.
Ensures all data is trustworthy for both high-level and beginner players.
"""

import json
import re
from character_data import CHARACTER_DATA, MoveData, GuardType
from typing import Dict, List, Tuple, Set

# Characters with verified real data
VERIFIED_CHARACTERS = {"Blitzcrank"}

# Patterns that indicate placeholder data
PLACEHOLDER_PATTERNS = [
    r"hash\(",
    r"char_hash",
    r"create_basic_moves",
    r"standing light attack",
    r"standing medium attack",
    r"standing heavy attack",
    r"crouching light attack",
    r"crouching medium attack",
    r"crouching heavy attack",
    r"primary special move",
    r"secondary special move",
]

# Expected move inputs for each character type
EXPECTED_MOVES = {
    "normals": ["5L", "5M", "5H", "2L", "2M", "2H"],
    "specials": ["5S1", "2S1"],
    "grabs": ["2S2"]  # Some characters may have command grabs
}

# Valid frame data ranges (reasonable bounds)
VALID_RANGES = {
    "startup": (1, 60),  # 1-60 frames is reasonable
    "active": (1, 30),   # 1-30 active frames
    "recovery": (1, 100), # 1-100 recovery frames
    "on_block": (-30, 20), # -30 to +20 on block
    "damage": (1, 500)   # 1-500 damage
}

# Common frame data patterns that might indicate errors
SUSPICIOUS_PATTERNS = {
    "startup_0": "Startup of 0f (should be at least 1f for most moves)",
    "recovery_0": "Recovery of 0f (very unusual)",
    "active_0": "Active frames of 0 (might be instant)",
    "on_block_extreme": "On block > +10 or < -20 (very unusual)",
    "damage_0": "Damage of 0 (might be a grab or special property)",
    "startup_too_high": "Startup > 40f (very slow, might be error)",
    "recovery_too_high": "Recovery > 80f (very long, might be error)",
}

def check_for_placeholder_data(character_name: str, moves: Dict[str, MoveData]) -> List[str]:
    """Check if character has placeholder data"""
    issues = []
    
    # Check if character uses create_basic_moves
    char_class = CHARACTER_DATA.get(character_name)
    if char_class:
        import inspect
        source = inspect.getsource(char_class.get_moves)
        if "create_basic_moves" in source:
            issues.append("Uses create_basic_moves() - PLACEHOLDER DATA")
    
    # Check descriptions for placeholder patterns
    for move_input, move_data in moves.items():
        desc = move_data.description.lower()
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern.lower() in desc:
                issues.append(f"{move_input}: Description matches placeholder pattern '{pattern}'")
    
    return issues

def validate_frame_values(character_name: str, moves: Dict[str, MoveData]) -> Tuple[List[str], List[str]]:
    """Validate frame data values are within reasonable ranges"""
    errors = []
    warnings = []
    
    for move_input, move_data in moves.items():
        # Check startup
        if move_data.startup < VALID_RANGES["startup"][0]:
            errors.append(f"{character_name} {move_input}: Startup {move_data.startup}f is too low (minimum 1f)")
        elif move_data.startup == 0 and not move_data.is_grab:
            warnings.append(f"{character_name} {move_input}: Startup is 0f (unusual, might be grab)")
        elif move_data.startup > VALID_RANGES["startup"][1]:
            warnings.append(f"{character_name} {move_input}: Startup {move_data.startup}f is very high (>60f)")
        
        # Check recovery
        if move_data.recovery < VALID_RANGES["recovery"][0]:
            errors.append(f"{character_name} {move_input}: Recovery {move_data.recovery}f is too low (minimum 1f)")
        elif move_data.recovery == 0:
            warnings.append(f"{character_name} {move_input}: Recovery is 0f (very unusual)")
        elif move_data.recovery > VALID_RANGES["recovery"][1]:
            warnings.append(f"{character_name} {move_input}: Recovery {move_data.recovery}f is very high (>100f)")
        
        # Check active
        if move_data.active < 0:
            errors.append(f"{character_name} {move_input}: Active frames {move_data.active} is negative")
        elif move_data.active == 0:
            warnings.append(f"{character_name} {move_input}: Active frames is 0 (might be instant)")
        
        # Check on_block
        if move_data.on_block < VALID_RANGES["on_block"][0]:
            warnings.append(f"{character_name} {move_input}: On block {move_data.on_block} is very negative (<-30)")
        elif move_data.on_block > VALID_RANGES["on_block"][1]:
            warnings.append(f"{character_name} {move_input}: On block {move_data.on_block} is very positive (>+20)")
        
        # Check damage
        if move_data.damage < 0:
            errors.append(f"{character_name} {move_input}: Damage {move_data.damage} is negative")
        elif move_data.damage == 0 and not move_data.is_grab:
            warnings.append(f"{character_name} {move_input}: Damage is 0 (might be grab or special property)")
        elif move_data.damage > VALID_RANGES["damage"][1]:
            warnings.append(f"{character_name} {move_input}: Damage {move_data.damage} is very high (>500)")
        
        # Check guard types
        if not move_data.guard:
            warnings.append(f"{character_name} {move_input}: No guard types specified")
        
        # Check consistency: is_safe should match on_block
        if move_data.on_block >= 0 and not move_data.is_safe:
            warnings.append(f"{character_name} {move_input}: on_block >= 0 but is_safe=False (inconsistent)")
        elif move_data.on_block < -5 and move_data.is_safe and not move_data.is_grab:
            warnings.append(f"{character_name} {move_input}: on_block < -5 but is_safe=True (might be error)")
    
    return errors, warnings

def check_move_completeness(character_name: str, moves: Dict[str, MoveData]) -> List[str]:
    """Check if character has expected moves"""
    issues = []
    
    move_inputs = set(moves.keys())
    
    # Check for expected normals
    for normal in EXPECTED_MOVES["normals"]:
        if normal not in move_inputs:
            issues.append(f"Missing expected normal: {normal}")
    
    # Check for at least one special
    has_special = any(move_input.startswith("5S") or move_input.startswith("2S") for move_input in move_inputs)
    if not has_special:
        issues.append("No special moves found")
    
    return issues

def analyze_all_characters() -> Dict:
    """Comprehensive analysis of all character data"""
    results = {
        "verified_characters": [],
        "placeholder_characters": [],
        "validation_errors": {},
        "validation_warnings": {},
        "placeholder_issues": {},
        "completeness_issues": {},
        "summary": {
            "total_characters": 0,
            "verified_count": 0,
            "placeholder_count": 0,
            "total_errors": 0,
            "total_warnings": 0
        }
    }
    
    for char_name, char_class in CHARACTER_DATA.items():
        moves = char_class.get_moves()
        results["summary"]["total_characters"] += 1
        
        # Check if verified
        if char_name in VERIFIED_CHARACTERS:
            results["verified_characters"].append(char_name)
            results["summary"]["verified_count"] += 1
        else:
            results["placeholder_characters"].append(char_name)
            results["summary"]["placeholder_count"] += 1
        
        # Check for placeholder data
        placeholder_issues = check_for_placeholder_data(char_name, moves)
        if placeholder_issues:
            results["placeholder_issues"][char_name] = placeholder_issues
        
        # Validate frame values
        errors, warnings = validate_frame_values(char_name, moves)
        if errors:
            results["validation_errors"][char_name] = errors
        if warnings:
            results["validation_warnings"][char_name] = warnings
        
        # Check completeness
        completeness_issues = check_move_completeness(char_name, moves)
        if completeness_issues:
            results["completeness_issues"][char_name] = completeness_issues
        
        # Update summary
        results["summary"]["total_errors"] += len(errors)
        results["summary"]["total_warnings"] += len(warnings)
    
    return results

def print_validation_report(results: Dict):
    """Print comprehensive validation report"""
    print("="*70)
    print("COMPREHENSIVE FRAME DATA VALIDATION REPORT")
    print("="*70)
    
    # Summary
    print("\n[SUMMARY]")
    print("-"*70)
    print(f"Total Characters: {results['summary']['total_characters']}")
    print(f"Verified (Real Data): {results['summary']['verified_count']}")
    print(f"Placeholder Data: {results['summary']['placeholder_count']}")
    print(f"Total Errors: {results['summary']['total_errors']}")
    print(f"Total Warnings: {results['summary']['total_warnings']}")
    
    # Verified characters
    print("\n" + "="*70)
    print("[VERIFIED CHARACTERS] - Real Wiki Data")
    print("-"*70)
    if results["verified_characters"]:
        for char in results["verified_characters"]:
            print(f"  [OK] {char}")
    else:
        print("  [WARN] No verified characters found!")
    
    # Placeholder characters
    print("\n" + "="*70)
    print("[PLACEHOLDER CHARACTERS] - Generated Data (NOT REAL)")
    print("-"*70)
    if results["placeholder_characters"]:
        for char in results["placeholder_characters"]:
            print(f"  [WARN] {char} - Uses placeholder/generated data")
            if char in results["placeholder_issues"]:
                for issue in results["placeholder_issues"][char][:3]:  # Show first 3
                    print(f"      - {issue}")
    else:
        print("  ✅ No placeholder characters found!")
    
    # Validation errors
    print("\n" + "="*70)
    print("[VALIDATION ERRORS] - Must Fix")
    print("-"*70)
    if results["validation_errors"]:
        for char, errors in results["validation_errors"].items():
            print(f"\n{char}:")
            for error in errors:
                print(f"  [ERROR] {error}")
    else:
        print("  [OK] No validation errors found!")
    
    # Validation warnings
    print("\n" + "="*70)
    print("[VALIDATION WARNINGS] - Should Review")
    print("-"*70)
    warning_count = 0
    for char, warnings in results["validation_warnings"].items():
        if warning_count < 20:  # Limit output
            print(f"\n{char}:")
            for warning in warnings[:5]:  # First 5 warnings
                print(f"  [WARN] {warning}")
            warning_count += len(warnings)
        else:
            remaining = sum(len(w) for w in list(results["validation_warnings"].values())[list(results["validation_warnings"].keys()).index(char):])
            print(f"\n... and {remaining} more warnings (truncated)")
            break
    
    # Completeness issues
    print("\n" + "="*70)
    print("[COMPLETENESS ISSUES] - Missing Moves")
    print("-"*70)
    if results["completeness_issues"]:
        for char, issues in results["completeness_issues"].items():
            print(f"\n{char}:")
            for issue in issues:
                print(f"  [WARN] {issue}")
    else:
        print("  [OK] All characters have expected moves!")
    
    # Recommendations
    print("\n" + "="*70)
    print("[RECOMMENDATIONS]")
    print("-"*70)
    
    if results["summary"]["placeholder_count"] > 0:
        print(f"\n[CRITICAL] {results['summary']['placeholder_count']} characters have placeholder data!")
        print("   These characters should NOT be trusted for competitive play.")
        print("   Action required: Update with real wiki data or mark clearly as placeholder.")
    
    if results["summary"]["total_errors"] > 0:
        print(f"\n[ERROR] {results['summary']['total_errors']} validation errors found!")
        print("   These must be fixed before data can be trusted.")
    
    if results["summary"]["total_warnings"] > 0:
        print(f"\n[WARN] {results['summary']['total_warnings']} warnings found.")
        print("   These should be reviewed for accuracy.")
    
    if results["summary"]["verified_count"] == results["summary"]["total_characters"]:
        print("\n[OK] All characters have verified real data!")
    elif results["summary"]["verified_count"] > 0:
        print(f"\n[OK] {results['summary']['verified_count']} character(s) have verified real data.")
        print(f"   [WARN] {results['summary']['placeholder_count']} character(s) need real data entry.")

def save_validation_report(results: Dict, filename: str = "output/FRAME_DATA_VALIDATION_REPORT.md"):
    """Save validation report to markdown file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Frame Data Validation Report\n\n")
        f.write("## ⚠️ CRITICAL: Placeholder Data Detected\n\n")
        f.write("This report identifies which characters have **real verified data** vs **placeholder/generated data**.\n\n")
        
        f.write("## Summary\n\n")
        f.write(f"- **Total Characters**: {results['summary']['total_characters']}\n")
        f.write(f"- **Verified (Real Data)**: {results['summary']['verified_count']}\n")
        f.write(f"- **⚠️ Placeholder Data**: {results['summary']['placeholder_count']}\n")
        f.write(f"- **Validation Errors**: {results['summary']['total_errors']}\n")
        f.write(f"- **Validation Warnings**: {results['summary']['total_warnings']}\n\n")
        
        # Verified characters
        f.write("## ✅ Verified Characters (Real Wiki Data)\n\n")
        if results["verified_characters"]:
            for char in results["verified_characters"]:
                f.write(f"- **{char}** - Real frame data from wiki\n")
        else:
            f.write("⚠️ No verified characters found!\n\n")
        
        # Placeholder characters
        f.write("\n## ⚠️ Placeholder Characters (Generated Data - NOT REAL)\n\n")
        f.write("**These characters use generated placeholder data and should NOT be trusted for competitive play.**\n\n")
        if results["placeholder_characters"]:
            for char in results["placeholder_characters"]:
                f.write(f"### {char}\n\n")
                f.write("**Status**: ⚠️ PLACEHOLDER DATA - NOT REAL\n\n")
                if char in results["placeholder_issues"]:
                    f.write("**Issues**:\n")
                    for issue in results["placeholder_issues"][char]:
                        f.write(f"- {issue}\n")
                f.write("\n")
        
        # Validation errors
        if results["validation_errors"]:
            f.write("\n## ❌ Validation Errors (Must Fix)\n\n")
            for char, errors in results["validation_errors"].items():
                f.write(f"### {char}\n\n")
                for error in errors:
                    f.write(f"- {error}\n")
                f.write("\n")
        
        # Recommendations
        f.write("\n## 🎯 Recommendations\n\n")
        if results["summary"]["placeholder_count"] > 0:
            f.write("### ⚠️ CRITICAL ACTION REQUIRED\n\n")
            f.write(f"{results['summary']['placeholder_count']} characters have placeholder data:\n")
            for char in results["placeholder_characters"]:
                f.write(f"- {char}\n")
            f.write("\n**These must be updated with real wiki data before the system can be trusted.**\n\n")
        
        if results["summary"]["total_errors"] > 0:
            f.write(f"### ❌ Fix Validation Errors\n\n")
            f.write(f"{results['summary']['total_errors']} validation errors must be fixed.\n\n")
        
        f.write("### Next Steps\n\n")
        f.write("1. Update placeholder characters with real wiki data\n")
        f.write("2. Fix all validation errors\n")
        f.write("3. Review validation warnings\n")
        f.write("4. Re-run validation to confirm fixes\n\n")
    
    print(f"\n[OK] Validation report saved to: {filename}")

if __name__ == "__main__":
    print("Running comprehensive frame data validation...")
    print("="*70)
    
    results = analyze_all_characters()
    print_validation_report(results)
    save_validation_report(results)
    
    print("\n" + "="*70)
    print("[OK] Validation Complete!")
    print("="*70)
    
    # Exit with error code if critical issues found
    if results["summary"]["placeholder_count"] > 0 or results["summary"]["total_errors"] > 0:
        print("\n[CRITICAL] ISSUES FOUND - Data cannot be fully trusted!")
        exit(1)
    else:
        print("\n[OK] All data validated successfully!")
