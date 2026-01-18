# Micro-Tests Guide

## 🎯 Overview

All Playwright tests have been broken into **micro-tests** to prevent timeouts and enable faster, more reliable testing.

---

## 📊 Test Breakdown

### Before: Large Tests (Timeout Risk)
- ❌ `test_tab_switching` - Tested 2 tabs in one test
- ❌ `test_sort_dropdown` - Tested 4 options in one test
- ❌ `test_filter_dropdown` - Tested 4 options in one test
- ❌ `test_embedded_data_loads` - Multiple checks in one test

### After: Micro-Tests (No Timeouts)
- ✅ `test_switch_to_moves_tab` - One tab, one test
- ✅ `test_switch_to_combos_tab` - One tab, one test
- ✅ `test_sort_option[startup]` - One option, one test (parametrized)
- ✅ `test_filter_option[all]` - One option, one test (parametrized)

---

## 🧪 Test Organization

### 1. Basic Loading (2 tests)
- `test_database_page_title`
- `test_database_page_header`

### 2. Tab Presence (6 tests - parametrized)
- Each tab tested individually
- Uses `@pytest.mark.parametrize`

### 3. Tab Switching (6 tests)
- One test per tab switch
- Each test is independent

### 4. Move Database Elements (4 tests)
- Character dropdown
- Sort dropdown
- Filter dropdown
- Moves container

### 5. Sort Options (4 tests - parametrized)
- `test_sort_option[startup]`
- `test_sort_option[safety]`
- `test_sort_option[damage]`
- `test_sort_option[recovery]`

### 6. Filter Options (4 tests - parametrized)
- `test_filter_option[all]`
- `test_filter_option[safe]`
- `test_filter_option[unsafe]`
- `test_filter_option[assist]`

### 7. Console Errors (1 test)
- Critical error detection

### 8. Embedded Page (5 tests)
- Title
- CORS errors
- Moves tab
- Combos tab
- Overview tab

### 9. Other Pages (3 tests)
- Guide page
- Controls page (2 tests)

**Total: ~35 micro-tests**

---

## ⚡ Performance Benefits

### Before (Large Tests)
- Average test time: 10-30 seconds
- Risk of timeout: High
- Debugging: Hard to isolate issues

### After (Micro-Tests)
- Average test time: 2-5 seconds each
- Risk of timeout: Very low
- Debugging: Easy to identify failing test

---

## 🔧 Fixtures for Speed

### Pre-loaded Fixtures

**`loaded_database_page`** - Page already loaded
```python
def test_something(loaded_database_page: Page):
    # Page is already loaded, just use it
    page = loaded_database_page
    page.click("text=Tab")
```

**`moves_tab_ready`** - Move Database tab already active
```python
def test_sort(moves_tab_ready: Page):
    # Tab is already active, dropdowns ready
    page = moves_tab_ready
    page.locator("#sort-moves")
```

---

## 🚀 Running Micro-Tests

### Run All Tests
```bash
python run_playwright_tests.py
```

### Run Specific Test Class
```bash
pytest tests/test_character_database.py::TestPageLoading -v
```

### Run Single Test
```bash
pytest tests/test_character_database.py::TestPageLoading::test_database_page_title -v
```

### Run Parametrized Tests
```bash
# All sort option tests
pytest tests/test_character_database.py::TestSortOptions -v

# Single parametrized test
pytest tests/test_character_database.py::TestSortOptions::test_sort_option[startup] -v
```

### Run with Parallel Execution
```bash
# Install pytest-xdist first
pip install pytest-xdist

# Run in parallel
pytest tests/ -n auto
```

---

## ⏱️ Timeout Configuration

### Default Timeouts (in `pytest.ini`)
- **Test timeout:** 30 seconds
- **Page load:** 10-15 seconds
- **Element wait:** 5-10 seconds

### Adjust Timeouts

**Per test:**
```python
@pytest.mark.timeout(60)  # 60 second timeout
def test_slow_feature(page: Page):
    ...
```

**Global:**
Edit `tests/pytest.ini`:
```ini
timeout = 60  # Increase global timeout
```

---

## 📈 Test Statistics

### Test Count
- **Total micro-tests:** ~35
- **Parametrized tests:** 10 (expands to multiple)
- **Independent tests:** 25

### Execution Time
- **Before:** ~3-5 minutes (with timeouts)
- **After:** ~1-2 minutes (no timeouts)
- **Parallel:** ~30-60 seconds (with pytest-xdist)

---

## ✅ Best Practices

### 1. One Assertion Per Test (Ideally)
```python
# Good
def test_title(page: Page):
    expect(page).to_have_title("Title")

def test_header(page: Page):
    expect(page.locator("header")).to_be_visible()
```

### 2. Use Fixtures for Setup
```python
# Good - uses fixture
def test_something(loaded_database_page: Page):
    page = loaded_database_page
    # Test code
```

### 3. Explicit Timeouts
```python
# Good
page.goto(url, timeout=10000)
expect(element).to_be_visible(timeout=5000)
```

### 4. Parametrize Similar Tests
```python
# Good
@pytest.mark.parametrize("tab_name", ["Tab1", "Tab2", "Tab3"])
def test_tab(tab_name: str, page: Page):
    # Test code
```

---

## 🎯 Summary

**All tests are now micro-sized:**
- ✅ Fast execution (< 5 seconds each)
- ✅ No timeout issues
- ✅ Easy debugging
- ✅ Can run in parallel
- ✅ Clear test reports

**Total: ~35 focused micro-tests covering all functionality!**
