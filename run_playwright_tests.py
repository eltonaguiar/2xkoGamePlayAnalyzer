"""
Run Playwright tests with automatic server management.
Starts server on port 8002, runs tests, then stops server.
"""

import subprocess
import sys
import os
import time
import signal
import atexit
from pathlib import Path

PORT = 8002
SERVER_SCRIPT = "output/test_server.py"  # Use test server (no browser popup)
TEST_DIR = "tests"
BASE_URL = f"http://localhost:{PORT}"

server_process = None


def start_server():
    """Start the local server"""
    global server_process
    
    print("="*70)
    print("Starting local server on port 8002...")
    print("="*70)
    
    # Change to output directory for server
    server_path = Path(SERVER_SCRIPT).resolve()
    server_dir = server_path.parent
    
    # Start server in background
    server_process = subprocess.Popen(
        [sys.executable, str(server_path)],
        cwd=str(server_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
    )
    
    # Wait for server to start with retries
    print("Waiting for server to start...")
    max_retries = 10
    for i in range(max_retries):
        time.sleep(1)
        try:
            import urllib.request
            response = urllib.request.urlopen(f"{BASE_URL}/character_database.html", timeout=3)
            if response.status == 200:
                print(f"[OK] Server is running at {BASE_URL}")
                return True
        except Exception:
            if i < max_retries - 1:
                print(f"  Retry {i+1}/{max_retries}...")
            continue
    
    print(f"[ERROR] Server failed to start after {max_retries} attempts")
    return False


def stop_server():
    """Stop the local server"""
    global server_process
    
    if server_process:
        print("\n" + "="*70)
        print("Stopping server...")
        print("="*70)
        
        try:
            if sys.platform == "win32":
                server_process.terminate()
            else:
                server_process.send_signal(signal.SIGTERM)
            
            server_process.wait(timeout=5)
            print("[OK] Server stopped")
        except Exception as e:
            print(f"[WARNING] Error stopping server: {e}")
            try:
                server_process.kill()
            except:
                pass


def run_tests():
    """Run Playwright tests"""
    print("\n" + "="*70)
    print("Running Playwright tests...")
    print("="*70)
    print()
    
    # Check if tests directory exists
    if not os.path.exists(TEST_DIR):
        print(f"[ERROR] Test directory not found: {TEST_DIR}")
        return False
    
    # Check if test file exists
    test_file = os.path.join(TEST_DIR, "test_character_database.py")
    if not os.path.exists(test_file):
        print(f"[ERROR] Test file not found: {test_file}")
        return False
    
    # Run pytest with Playwright
    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                test_file,
                "-v",
                "--tb=short",
                f"--base-url={BASE_URL}"
            ],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            timeout=300  # 5 minute timeout
        )
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("[ERROR] Tests timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Error running tests: {e}")
        return False


def check_playwright_installed():
    """Check if Playwright is installed"""
    try:
        import playwright
        return True
    except ImportError:
        return False


def install_playwright_browsers():
    """Install Playwright browsers"""
    print("Installing Playwright browsers...")
    print("This may take a few minutes...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            timeout=600  # 10 minute timeout
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Failed to install browsers: {e}")
        return False


def main():
    """Main function"""
    print("="*70)
    print("PLAYWRIGHT TEST RUNNER")
    print("="*70)
    print()
    
    # Register cleanup
    atexit.register(stop_server)
    
    # Check if Playwright is installed
    if not check_playwright_installed():
        print("[ERROR] Playwright is not installed!")
        print("Please run: pip install playwright")
        print("Then run: playwright install chromium")
        sys.exit(1)
    
    # Check if browsers are installed
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
    except Exception as e:
        print(f"[WARNING] Playwright browsers may not be installed: {e}")
        print("Attempting to install...")
        if not install_playwright_browsers():
            print("[ERROR] Failed to install browsers")
            sys.exit(1)
    
    # Start server
    if not start_server():
        print("[WARNING] Server may not have started correctly")
        print("Continuing with tests anyway...")
    
    try:
        # Run tests
        success = run_tests()
        
        if success:
            print("\n" + "="*70)
            print("[OK] ALL TESTS PASSED!")
            print("="*70)
            sys.exit(0)
        else:
            print("\n" + "="*70)
            print("[ERROR] SOME TESTS FAILED")
            print("="*70)
            sys.exit(1)
    finally:
        # Stop server
        stop_server()


if __name__ == "__main__":
    main()
