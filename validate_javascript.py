"""
JavaScript validation script for HTML files.
Checks for syntax errors, common issues, and validates JavaScript code.
"""

import re
import os
import sys
from typing import List, Dict, Tuple

try:
    import esprima
    ESPRIMA_AVAILABLE = True
except ImportError:
    ESPRIMA_AVAILABLE = False
    print("[WARNING] esprima not installed. Installing...")
    print("Run: pip install pyesprima")
    print("Falling back to basic validation only.")


class JavaScriptValidator:
    """Validate JavaScript code in HTML files"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.validated_files = []
    
    def extract_javascript_from_html(self, html_content: str) -> List[Tuple[str, int]]:
        """Extract all JavaScript code blocks from HTML"""
        scripts = []
        
        # Find all <script> tags (including inline and external)
        script_pattern = r'<script[^>]*>(.*?)</script>'
        matches = re.finditer(script_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            script_content = match.group(1)
            # Skip external scripts (src attribute)
            if not re.search(r'src\s*=', match.group(0), re.IGNORECASE):
                start_pos = match.start()
                line_number = html_content[:start_pos].count('\n') + 1
                scripts.append((script_content, line_number))
        
        return scripts
    
    def validate_syntax_with_esprima(self, js_code: str, filename: str, line_offset: int = 0) -> List[Dict]:
        """Validate JavaScript syntax using esprima"""
        errors = []
        
        if not ESPRIMA_AVAILABLE:
            return errors
        
        try:
            # Try to parse the JavaScript
            esprima.parseScript(js_code, {'tolerant': False})
        except Exception as e:
            error_msg = str(e)
            # Extract line number if available
            line_match = re.search(r'Line (\d+)', error_msg)
            if line_match:
                line_num = int(line_match.group(1)) + line_offset
            else:
                line_num = line_offset
            
            errors.append({
                'type': 'syntax_error',
                'file': filename,
                'line': line_num,
                'message': error_msg,
                'severity': 'error'
            })
        
        return errors
    
    def check_common_issues(self, js_code: str, filename: str, line_offset: int = 0) -> List[Dict]:
        """Check for common JavaScript issues"""
        issues = []
        lines = js_code.split('\n')
        
        for i, line in enumerate(lines):
            line_num = i + 1 + line_offset
            
            # Check for undefined variables (common patterns)
            if re.search(r'\bundefined\b', line) and 'typeof' not in line and '!==' not in line and '===' not in line:
                issues.append({
                    'type': 'potential_undefined',
                    'file': filename,
                    'line': line_num,
                    'message': 'Potential undefined variable usage without check',
                    'severity': 'warning',
                    'code': line.strip()
                })
            
            # Check for missing semicolons (optional but can cause issues)
            if line.strip() and not line.strip().startswith('//'):
                if re.match(r'^[^;{}()\[\]]+$', line.strip()) and not line.strip().endswith((';', '{', '}', ':', ',', ')')):
                    # Skip function declarations, if statements, etc.
                    if not re.search(r'\b(function|if|for|while|switch|try|catch|else)\b', line):
                        pass  # This is too noisy, commented out
            
            # Check for console.log in production (warning)
            if 'console.log' in line or 'console.error' in line:
                issues.append({
                    'type': 'console_usage',
                    'file': filename,
                    'line': line_num,
                    'message': 'Console statement found (consider removing for production)',
                    'severity': 'info',
                    'code': line.strip()
                })
            
            # Check for missing error handling (but only if not in try-catch)
            if 'fetch(' in line:
                # Check if there's a try-catch in the surrounding code
                context_start = max(0, i - 30)
                context_end = min(len(lines), i + 30)
                context = '\n'.join(lines[context_start:context_end])
                if 'try' not in context or 'catch' not in context:
                    issues.append({
                        'type': 'missing_error_handling',
                        'file': filename,
                        'line': line_num,
                        'message': 'fetch() call may need error handling',
                        'severity': 'warning',
                        'code': line.strip()
                    })
            
            # Check for potential null/undefined access (but skip if already has checks)
            if (re.search(r'\.\w+\s*[;=]', line) and '?' not in line and 
                'if' not in line[max(0, i-3):i] and 
                '||' not in line and '&&' not in line and
                'getElementById' not in line):  # getElementById is safe to check later
                # Check if it's accessing a property without optional chaining
                if re.search(r'\w+\.\w+', line) and not re.search(r'(if\s*\(|&&|\|\|)', line):
                    # Skip template literals and string operations
                    if not (line.strip().startswith('`') or '"' in line or "'" in line):
                        issues.append({
                            'type': 'potential_null_access',
                            'file': filename,
                            'line': line_num,
                            'message': 'Property access without null check (consider optional chaining ?.)',
                            'severity': 'warning',
                            'code': line.strip()
                        })
        
        return issues
    
    def check_function_definitions(self, js_code: str, filename: str) -> List[Dict]:
        """Check that all called functions are defined"""
        issues = []
        
        # File-specific required functions
        file_requirements = {
            'character_database.html': ['loadDatabase', 'initializeUI', 'loadMoves', 'loadCombos', 'loadCharacterOverview'],
            'character_database_embedded.html': ['loadDatabase', 'initializeUI', 'loadMoves', 'loadCombos', 'loadCharacterOverview'],
            'character_guide.html': [],  # Different page, different functions - no requirements
            'custom_controls.html': [],  # Different page - has its own functions (updateMoves, loadPreset, etc.)
        }
        
        # Get filename only
        basename = os.path.basename(filename)
        required_functions = file_requirements.get(basename, [])
        
        # Check for required functions
        for func in required_functions:
            if func not in js_code:
                issues.append({
                    'type': 'missing_function',
                    'file': filename,
                    'line': 0,
                    'message': f'Required function "{func}" not found',
                    'severity': 'error'
                })
        
        return issues
    
    def validate_html_file(self, filepath: str) -> Dict:
        """Validate JavaScript in an HTML file"""
        print(f"\n[CHECKING] {filepath}")
        
        if not os.path.exists(filepath):
            return {
                'file': filepath,
                'status': 'error',
                'message': 'File not found',
                'errors': [],
                'warnings': []
            }
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Extract JavaScript
        scripts = self.extract_javascript_from_html(html_content)
        
        if not scripts:
            return {
                'file': filepath,
                'status': 'warning',
                'message': 'No JavaScript found in file',
                'errors': [],
                'warnings': []
            }
        
        all_errors = []
        all_warnings = []
        all_info = []
        
        # Combine all scripts for full validation
        full_js = '\n'.join([script[0] for script in scripts])
        
        # Validate syntax
        if ESPRIMA_AVAILABLE:
            for script_content, line_offset in scripts:
                syntax_errors = self.validate_syntax_with_esprima(script_content, filepath, line_offset)
                all_errors.extend(syntax_errors)
        else:
            all_warnings.append({
                'type': 'no_parser',
                'file': filepath,
                'line': 0,
                'message': 'esprima not available - skipping syntax validation',
                'severity': 'warning'
            })
        
        # Check common issues
        for script_content, line_offset in scripts:
            issues = self.check_common_issues(script_content, filepath, line_offset)
            for issue in issues:
                if issue['severity'] == 'error':
                    all_errors.append(issue)
                elif issue['severity'] == 'warning':
                    all_warnings.append(issue)
                else:
                    all_info.append(issue)
        
        # Check function definitions
        func_issues = self.check_function_definitions(full_js, filepath)
        all_errors.extend([i for i in func_issues if i['severity'] == 'error'])
        all_warnings.extend([i for i in func_issues if i['severity'] == 'warning'])
        
        # Check for common HTML/JS integration issues
        if 'addEventListener' in full_js and 'DOMContentLoaded' not in full_js:
            all_warnings.append({
                'type': 'dom_ready',
                'file': filepath,
                'line': 0,
                'message': 'Using addEventListener but DOMContentLoaded not found - may cause timing issues',
                'severity': 'warning'
            })
        
        status = 'error' if all_errors else ('warning' if all_warnings else 'ok')
        
        return {
            'file': filepath,
            'status': status,
            'errors': all_errors,
            'warnings': all_warnings,
            'info': all_info,
            'scripts_found': len(scripts)
        }
    
    def validate_directory(self, directory: str, pattern: str = '*.html') -> List[Dict]:
        """Validate all HTML files in a directory"""
        results = []
        
        if not os.path.exists(directory):
            print(f"[ERROR] Directory not found: {directory}")
            return results
        
        html_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        
        for html_file in html_files:
            result = self.validate_html_file(html_file)
            results.append(result)
        
        return results
    
    def print_report(self, results: List[Dict]):
        """Print validation report"""
        print("\n" + "="*70)
        print("JAVASCRIPT VALIDATION REPORT")
        print("="*70)
        
        total_files = len(results)
        error_files = [r for r in results if r['status'] == 'error']
        warning_files = [r for r in results if r['status'] == 'warning']
        ok_files = [r for r in results if r['status'] == 'ok']
        
        print(f"\nTotal files checked: {total_files}")
        print(f"  [OK] OK: {len(ok_files)}")
        print(f"  [WARN] Warnings: {len(warning_files)}")
        print(f"  [ERROR] Errors: {len(error_files)}")
        
        # Print errors
        if error_files:
            print("\n" + "="*70)
            print("ERRORS FOUND:")
            print("="*70)
            for result in error_files:
                print(f"\n[ERROR] {result['file']}")
                for error in result['errors']:
                    print(f"   Line {error.get('line', '?')}: {error['message']}")
                    if 'code' in error:
                        print(f"   Code: {error['code']}")
        
        # Print warnings
        if warning_files:
            print("\n" + "="*70)
            print("WARNINGS:")
            print("="*70)
            for result in warning_files:
                if result['warnings']:
                    print(f"\n[WARN] {result['file']}")
                    for warning in result['warnings'][:5]:  # Limit to 5 per file
                        print(f"   Line {warning.get('line', '?')}: {warning['message']}")
        
        # Summary
        total_errors = sum(len(r['errors']) for r in results)
        total_warnings = sum(len(r['warnings']) for r in results)
        
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Total errors: {total_errors}")
        print(f"Total warnings: {total_warnings}")
        
        if total_errors == 0 and total_warnings == 0:
            print("\n[OK] All JavaScript is valid!")
        elif total_errors == 0:
            print("\n[WARN] No errors, but some warnings found")
        else:
            print("\n[ERROR] Errors found - please fix before deploying")
        
        return total_errors == 0


def main():
    """Main validation function"""
    validator = JavaScriptValidator()
    
    # Check if esprima is available
    if not ESPRIMA_AVAILABLE:
        print("\n[INFO] For full syntax validation, install esprima:")
        print("  pip install pyesprima")
        print("\nContinuing with basic validation...\n")
    
    # Validate output directory HTML files
    output_dir = 'output'
    html_files_to_check = [
        'output/character_database.html',
        'output/character_database_embedded.html',
        'output/character_guide.html',
        'output/custom_controls.html'
    ]
    
    results = []
    for html_file in html_files_to_check:
        if os.path.exists(html_file):
            result = validator.validate_html_file(html_file)
            results.append(result)
    
    # Print report
    all_ok = validator.print_report(results)
    
    # Return exit code
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
