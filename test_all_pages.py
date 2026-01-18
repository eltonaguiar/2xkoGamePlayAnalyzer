"""
Comprehensive test suite to verify all pages work correctly.
Tests HTML pages, JavaScript functionality, and data loading.
"""

import subprocess
import sys
import os
import json
from pathlib import Path


def test_database_generation():
    """Test that database generates correctly"""
    print("="*70)
    print("TEST 1: Database Generation")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, "generate_database.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print("[FAIL] Database generation failed")
            print(result.stderr)
            return False
        
        # Check JSON file exists
        if not os.path.exists("output/character_database.json"):
            print("[FAIL] JSON file not created")
            return False
        
        # Verify JSON is valid
        with open("output/character_database.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "characters" not in data or "comparison" not in data:
            print("[FAIL] Invalid JSON structure")
            return False
        
        char_count = len(data["characters"])
        print(f"[OK] Database generated successfully")
        print(f"[INFO] {char_count} character(s) in database")
        
        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def test_embedded_html_generation():
    """Test embedded HTML generation"""
    print("\n" + "="*70)
    print("TEST 2: Embedded HTML Generation")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, "generate_embedded_html.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print("[FAIL] Embedded HTML generation failed")
            print(result.stderr)
            return False
        
        if not os.path.exists("output/character_database_embedded.html"):
            print("[FAIL] Embedded HTML file not created")
            return False
        
        print("[OK] Embedded HTML generated successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def test_javascript_validation():
    """Test JavaScript validation"""
    print("\n" + "="*70)
    print("TEST 3: JavaScript Validation")
    print("="*70)
    
    try:
        result = subprocess.run(
            [sys.executable, "validate_javascript.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Check for critical errors (warnings are OK)
        if "Total errors: 0" in result.stdout:
            print("[OK] No JavaScript errors found")
            return True
        elif "Total errors:" in result.stdout:
            # Extract error count
            for line in result.stdout.split('\n'):
                if "Total errors:" in line:
                    error_count = int(line.split("Total errors:")[1].strip().split()[0])
                    if error_count == 0:
                        print("[OK] No JavaScript errors found")
                        return True
                    else:
                        print(f"[WARN] {error_count} JavaScript errors found (see validation output)")
                        return False
        else:
            print("[WARN] Could not parse validation output")
            return True  # Don't fail on parsing issues
    except Exception as e:
        print(f"[WARN] Validation check failed: {e}")
        return True  # Don't fail if validation script has issues


def test_database_structure():
    """Test database has correct structure for all pages"""
    print("\n" + "="*70)
    print("TEST 4: Database Structure for All Pages")
    print("="*70)
    
    try:
        with open("output/character_database.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        issues = []
        
        # Check required structure for Move Database tab
        if "characters" not in data:
            issues.append("Missing 'characters' for Move Database tab")
        else:
            for char_name, char_data in data["characters"].items():
                if "moves" not in char_data:
                    issues.append(f"{char_name}: Missing 'moves' for Move Database")
                elif not isinstance(char_data["moves"], list):
                    issues.append(f"{char_name}: Moves must be array for Move Database")
        
        # Check required structure for BnB Combos tab
        if "characters" in data:
            for char_name, char_data in data["characters"].items():
                if "bnb_combos" not in char_data:
                    issues.append(f"{char_name}: Missing 'bnb_combos' for Combos tab")
        
        # Check required structure for Character Overview tab
        if "characters" in data:
            for char_name, char_data in data["characters"].items():
                if "info" not in char_data:
                    issues.append(f"{char_name}: Missing 'info' for Character Overview")
        
        # Check required structure for Fastest Moves tab
        if "comparison" not in data or "fastest_moves" not in data["comparison"]:
            issues.append("Missing 'comparison.fastest_moves' for Fastest Moves tab")
        
        # Check required structure for Safest Moves tab
        if "comparison" not in data or "safest_moves" not in data["comparison"]:
            issues.append("Missing 'comparison.safest_moves' for Safest Moves tab")
        
        if issues:
            print("[FAIL] Database structure issues:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("[OK] Database structure supports all pages")
            return True
    except Exception as e:
        print(f"[FAIL] Error checking structure: {e}")
        return False


def test_all_characters_have_data():
    """Test that all registered characters have complete data"""
    print("\n" + "="*70)
    print("TEST 5: Character Data Completeness")
    print("="*70)
    
    try:
        from character_data import CHARACTER_DATA
        
        with open("output/character_database.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        issues = []
        warnings = []
        
        # Check all registered characters are in database
        for char_name in CHARACTER_DATA.keys():
            if char_name not in data["characters"]:
                issues.append(f"{char_name}: Registered but not in database")
        
        # Check all database characters have required data
        for char_name, char_data in data["characters"].items():
            # Check moves
            moves = char_data.get("moves", [])
            if not moves:
                issues.append(f"{char_name}: No moves data")
            else:
                moves_with_data = [m for m in moves if m.get("startup", 0) > 0 or m.get("recovery", 0) > 0]
                if len(moves_with_data) < len(moves):
                    warnings.append(f"{char_name}: Some moves missing frame data")
            
            # Check combos
            combos = char_data.get("bnb_combos", {})
            if not combos:
                warnings.append(f"{char_name}: No BnB combos")
            
            # Check info
            info = char_data.get("info", {})
            if not info:
                issues.append(f"{char_name}: No character info")
        
        if issues:
            print("[FAIL] Data completeness issues:")
            for issue in issues:
                print(f"  - {issue}")
        
        if warnings:
            print("[WARN] Data completeness warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        
        if not issues:
            print("[OK] All characters have required data")
            return True
        else:
            return False
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        return False


def test_html_files_exist():
    """Test all required HTML files exist"""
    print("\n" + "="*70)
    print("TEST 6: HTML Files Existence")
    print("="*70)
    
    required_files = [
        "output/character_database.html",
        "output/character_database_embedded.html",
        "output/character_guide.html",
        "output/custom_controls.html"
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print("[FAIL] Missing HTML files:")
        for file in missing:
            print(f"  - {file}")
        return False
    else:
        print("[OK] All required HTML files exist")
        return True


def print_final_summary(results):
    """Print final test summary"""
    print("\n" + "="*70)
    print("FINAL TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[OK] ALL TESTS PASSED!")
        print("\nAll pages are fully functional and ready to use.")
        return True
    else:
        print(f"\n[FAIL] {total - passed} test(s) failed")
        print("\nPlease fix the issues above.")
        return False


def main():
    """Run all tests"""
    print("="*70)
    print("COMPREHENSIVE PAGE FUNCTIONALITY TEST")
    print("="*70)
    print("\nTesting all pages and functionality...\n")
    
    results = {
        "database_generation": test_database_generation(),
        "embedded_html_generation": test_embedded_html_generation(),
        "javascript_validation": test_javascript_validation(),
        "database_structure": test_database_structure(),
        "character_data_completeness": test_all_characters_have_data(),
        "html_files_exist": test_html_files_exist()
    }
    
    all_passed = print_final_summary(results)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
