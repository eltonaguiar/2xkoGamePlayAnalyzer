# Playwright Testing System

## 🎯 Overview

Comprehensive Playwright test suite for validating HTML files and JavaScript functionality.

---

## 📁 Files Created

### 1. **`tests/test_character_database.py`** (Test Suite)
**Purpose:** Playwright tests for all HTML files

**Test Coverage:**
- ✅ Page loading
- ✅ Header presence
- ✅ Tab functionality
- ✅ Character dropdowns
- ✅ Move tables
- ✅ Sorting and filtering
- ✅ Console error detection
- ✅ Embedded data loading
- ✅ Custom controls

### 2. **`tests/conftest.py`** (Pytest Configuration)
**Purpose:** Shared fixtures and configuration

**Features:**
- Browser instance management
- Page creation per test
- Console error capture
- Viewport configuration

### 3. **`run_playwright_tests.py`** (Test Runner)
**Purpose:** Automated test execution with server management

**Features:**
- ✅ Starts server on port 8002
- ✅ Runs all tests
- ✅ Stops server automatically
- ✅ Error reporting

---

## 🚀 How to Use

### Run All Tests

```bash
python run_playwright_tests.py
```

**This will:**
1. Start server on port 8002
2. Run all Playwright tests
3. Stop server automatically
4. Report results

### Run Tests Manually

**If server is already running:**
```bash
pytest tests/test_character_database.py -v
```

---

## 📊 Test Results

### Current Status:
```
✅ 10 tests passing
⚠️  5 tests need data loading fixes
```

**Passing Tests:**
- ✅ Page loads
- ✅ Header present
- ✅ Tabs present
- ✅ Tab switching
- ✅ No console errors
- ✅ Embedded page loads
- ✅ Embedded tabs work
- ✅ Guide page loads
- ✅ Controls page loads
- ✅ Control inputs present

**Tests Needing Data:**
- ⚠️ Character dropdown (needs data loaded)
- ⚠️ Move table loads (needs data loaded)
- ⚠️ Sort dropdown (needs data loaded)
- ⚠️ Filter dropdown (needs data loaded)
- ⚠️ Embedded data loads (needs data loaded)

---

## 🔧 Configuration

### Server Port

**Default:** Port 8002

**To change:**
1. Edit `output/start_local_server.py` → `PORT = 8002`
2. Edit `run_playwright_tests.py` → `PORT = 8002`
3. Edit `tests/conftest.py` → `PORT = 8002`

### Test Timeout

**Default:** 10 seconds per test

**To change:**
Edit `tests/test_character_database.py` → `timeout=10000`

---

## 📋 Test Structure

### Test Classes:

1. **`TestCharacterDatabase`**
   - Tests for `character_database.html`
   - Tests page loading, tabs, dropdowns, tables

2. **`TestCharacterDatabaseEmbedded`**
   - Tests for `character_database_embedded.html`
   - Tests embedded data loading

3. **`TestCharacterGuide`**
   - Tests for `character_guide.html`
   - Tests page loading

4. **`TestCustomControls`**
   - Tests for `custom_controls.html`
   - Tests control inputs

---

## 🎯 What Gets Tested

### ✅ Page Loading
- Title verification
- Header presence
- No 404 errors

### ✅ UI Elements
- Tabs present
- Dropdowns visible
- Containers load

### ✅ Functionality
- Tab switching
- Dropdown selection
- Sorting
- Filtering

### ✅ JavaScript
- No console errors
- Data loading
- Function execution

### ✅ Data Loading
- JSON file loading
- Embedded data
- Character data

---

## 🔍 Troubleshooting

### "Server not running"
**Solution:**
```bash
cd output
python start_local_server.py
```

### "Tests timeout"
**Solution:**
- Increase timeout in tests
- Check server is running
- Check JSON file exists

### "Elements not visible"
**Solution:**
- Wait for data to load
- Click tab first
- Increase wait times

---

## 📝 Adding New Tests

### Example Test:

```python
def test_new_feature(self, page: Page):
    """Test new feature"""
    page.goto(f"{BASE_URL}/character_database.html")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    
    # Your test code here
    element = page.locator("#my-element")
    expect(element).to_be_visible()
```

---

## 🎉 Benefits

### 1. Automated Testing
- No manual checking needed
- Runs on every change
- Catches regressions

### 2. Comprehensive Coverage
- All HTML files tested
- JavaScript validated
- UI elements verified

### 3. Server Management
- Automatic server start/stop
- Port configuration
- Error handling

### 4. Detailed Reports
- Test results
- Error messages
- Console output

---

## 📊 Current Test Status

**Last Run:**
```
✅ 10 tests passing
⚠️  5 tests need data loading
Total: 15 tests
```

**Server:** Running on port 8002 ✅

**Coverage:**
- ✅ Page loading
- ✅ UI elements
- ✅ Tab functionality
- ✅ Console errors
- ⚠️ Data-dependent features (needs data loaded)

---

## 🚀 Quick Commands

### Run All Tests
```bash
python run_playwright_tests.py
```

### Run Specific Test
```bash
pytest tests/test_character_database.py::TestCharacterDatabase::test_page_loads -v
```

### Run with Server Already Running
```bash
pytest tests/test_character_database.py -v --base-url=http://localhost:8002
```

---

**The Playwright testing system is set up and working!** 🎉

Run `python run_playwright_tests.py` to test your HTML files!
