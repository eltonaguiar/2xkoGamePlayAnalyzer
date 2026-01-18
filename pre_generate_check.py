"""
Pre-generation validation script.
Run this before generating HTML files to catch JavaScript errors early.
"""

import subprocess
import sys
import os


def run_validation():
    """Run JavaScript validation"""
    print("="*70)
    print("PRE-GENERATION JAVASCRIPT VALIDATION")
    print("="*70)
    print()
    
    if not os.path.exists('validate_javascript.py'):
        print("[ERROR] validate_javascript.py not found!")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, 'validate_javascript.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(result.stdout)
        
        if result.stderr:
            print("\n[STDERR]:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n[OK] All JavaScript validation passed!")
            return True
        else:
            print("\n[WARNING] Some validation issues found (see above)")
            print("Generation will continue, but please review warnings.")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERROR] Validation timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Could not run validation: {e}")
        return False


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
