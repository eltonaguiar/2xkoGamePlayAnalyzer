# Playwright Test Suite

## 🎯 Overview

Micro-test suite for comprehensive testing of all HTML pages without timeouts.

---

## 📁 Test Structure

### Test Files

- **`test_character_database.py`** - All database page tests (broken into micro-tests)
- **`conftest.py`** - Shared fixtures and configuration

---

## 🧪 Test Organization

### Test Classes (Micro-Tests)

1. **`TestPageLoading`** - Basic page loading
   - Page title
   - Header presence

2. **`TestTabsPresence`** - Tab existence (parametrized)
   - Each tab tested individually

3. **`TestTabSwitching`** - Tab functionality
   - Each tab switch tested individually

4. **`TestMoveDatabaseElements`** - Move Database tab elements
   - Dropdowns
   - Containers

5. **`TestSortOptions`** - Sort functionality (parametrized)
   - Each sort option tested individually

6. **`TestFilterOptions`** - Filter functionality (parametrized)
   - Each filter option tested individually

7. **`TestConsoleErrors`** - Console error detection

8. **`TestEmbeddedPage`** - Embedded page tests
   - Individual tab tests

9. **`TestCharacterGuide`** - Guide page tests

10. **`TestCustomControls`** - Controls page tests

---

## 🚀 Running Tests

### Run All Tests
```bash
python run_playwright_tests.py
```

### Run Specific Test Class
```bash
pytest tests/test_character_database.py::TestPageLoading -v
```

### Run Specific Test
```bash
pytest tests/test_character_database.py::TestPageLoading::test_database_page_title -v
```

### Run with Parallel Execution (if pytest-xdist installed)
```bash
pytest tests/ -n auto
```

### Run with Timeout
```bash
pytest tests/ --timeout=60
```

---

## ⚙️ Configuration

### Timeouts

- **Default test timeout:** 30 seconds (in `pytest.ini`)
- **Page load timeout:** 10-15 seconds
- **Element wait timeout:** 5-10 seconds

### Fixtures

- **`browser`** - Session-scoped browser instance
- **`page`** - Function-scoped page instance
- **`loaded_database_page`** - Pre-loaded database page
- **`loaded_embedded_page`** - Pre-loaded embedded page
- **`moves_tab_ready`** - Move Database tab ready to use

---

## 📊 Test Count

**Total Micro-Tests:** ~40+ individual tests

- Page Loading: 2 tests
- Tab Presence: 6 tests (parametrized)
- Tab Switching: 6 tests
- Move Database Elements: 4 tests
- Sort Options: 4 tests (parametrized)
- Filter Options: 4 tests (parametrized)
- Console Errors: 1 test
- Embedded Page: 5 tests
- Other Pages: 3 tests

---

## ✅ Benefits of Micro-Tests

1. **No Timeouts** - Each test is fast and focused
2. **Better Debugging** - Know exactly which test failed
3. **Parallel Execution** - Can run tests in parallel
4. **Selective Testing** - Run only what you need
5. **Clearer Reports** - See exactly what passed/failed

---

## 🔧 Troubleshooting

### Test Timeout
- Increase timeout in `pytest.ini`
- Check server is running on port 8002
- Verify network connectivity

### Element Not Found
- Check selector is correct
- Increase wait timeout
- Verify page loaded completely

### Server Not Running
```bash
cd output
python start_local_server.py
```

---

## 📝 Adding New Tests

### Example Micro-Test

```python
def test_new_feature(self, page: Page):
    """Test new feature"""
    page.goto(f"{BASE_URL}/page.html", timeout=10000)
    element = page.locator("#element")
    expect(element).to_be_visible(timeout=5000)
```

**Key Points:**
- One assertion per test (ideally)
- Use fixtures for common setup
- Set explicit timeouts
- Keep tests fast (< 5 seconds)

---

**All tests are micro-sized for fast, reliable execution!** 🎉
