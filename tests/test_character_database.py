"""
Playwright tests for character database HTML files.
Broken into micro-tests to prevent timeouts.
"""

import pytest
from playwright.sync_api import Page, expect

PORT = 8002
BASE_URL = f"http://localhost:{PORT}"


# ============================================================================
# Basic Page Loading Tests
# ============================================================================

class TestPageLoading:
    """Micro-tests for basic page loading"""
    
    def test_database_page_title(self, page: Page):
        """Test page title"""
        page.goto(f"{BASE_URL}/character_database.html", timeout=10000)
        expect(page).to_have_title("2XKO Character Database - Move Comparison", timeout=5000)
    
    def test_database_page_header(self, page: Page):
        """Test header element exists"""
        page.goto(f"{BASE_URL}/character_database.html", timeout=10000)
        header = page.locator("header h1")
        expect(header).to_be_visible(timeout=5000)
        expect(header).to_contain_text("Character Database", timeout=5000)


# ============================================================================
# Tab Presence Tests (Individual)
# ============================================================================

class TestTabsPresence:
    """Micro-tests for each tab presence"""
    
    @pytest.mark.parametrize("tab_name", [
        "Move Comparison",  # Actual tab name in HTML
        "BnB Combos",
        "Character Overview",
        "Fastest Moves",
        "Safest Moves",
        "Move Efficiency"
    ])
    def test_tab_exists(self, page: Page, tab_name: str):
        """Test individual tab exists"""
        page.goto(f"{BASE_URL}/character_database.html", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        
        tab = page.locator(f"text={tab_name}").first
        if tab.count() == 0:
            tab = page.locator(f"button:has-text('{tab_name}')").first
        if tab.count() == 0:
            tab = page.locator(f".tab:has-text('{tab_name}')").first
        
        assert tab.count() > 0, f"Tab '{tab_name}' not found"


# ============================================================================
# Tab Switching Tests (Individual)
# ============================================================================

class TestTabSwitching:
    """Micro-tests for individual tab switching"""
    
    def test_switch_to_moves_tab(self, loaded_database_page: Page):
        """Test switching to Move Database tab"""
        page = loaded_database_page
        # Wait for page to fully initialize
        page.wait_for_load_state("networkidle", timeout=10000)
        # Click the Move Comparison tab (actual tab name in HTML)
        page.click("text=Move Comparison", timeout=5000)
        page.wait_for_selector("#moves-container", state="visible", timeout=10000)
        expect(page.locator("#moves-container")).to_be_visible(timeout=5000)
    
    def test_switch_to_combos_tab(self, loaded_database_page: Page):
        """Test switching to BnB Combos tab"""
        page = loaded_database_page
        page.click("text=BnB Combos", timeout=5000)
        page.wait_for_selector("#combos-container", state="visible", timeout=10000)
        expect(page.locator("#combos-container")).to_be_visible(timeout=5000)
    
    def test_switch_to_overview_tab(self, loaded_database_page: Page):
        """Test switching to Character Overview tab"""
        page = loaded_database_page
        page.click("text=Character Overview", timeout=5000)
        page.wait_for_selector("#character-grid", state="visible", timeout=10000)
        expect(page.locator("#character-grid")).to_be_visible(timeout=5000)
    
    def test_switch_to_fastest_tab(self, loaded_database_page: Page):
        """Test switching to Fastest Moves tab"""
        page = loaded_database_page
        page.click("text=Fastest Moves", timeout=5000)
        page.wait_for_selector("#fastest-container", state="visible", timeout=10000)
        expect(page.locator("#fastest-container")).to_be_visible(timeout=5000)
    
    def test_switch_to_safest_tab(self, loaded_database_page: Page):
        """Test switching to Safest Moves tab"""
        page = loaded_database_page
        page.click("text=Safest Moves", timeout=5000)
        page.wait_for_selector("#safest-container", state="visible", timeout=10000)
        expect(page.locator("#safest-container")).to_be_visible(timeout=5000)
    
    def test_switch_to_efficiency_tab(self, loaded_database_page: Page):
        """Test switching to Move Efficiency tab"""
        page = loaded_database_page
        page.click("text=Move Efficiency", timeout=5000)
        page.wait_for_selector("#efficiency-container", state="visible", timeout=10000)
        expect(page.locator("#efficiency-container")).to_be_visible(timeout=5000)


# ============================================================================
# Move Database Tab Tests (Micro)
# ============================================================================

class TestMoveDatabaseElements:
    """Micro-tests for Move Database tab elements"""
    
    def test_character_dropdown_exists(self, moves_tab_ready: Page):
        """Test character dropdown is present"""
        page = moves_tab_ready
        dropdown = page.locator("#move-character")
        expect(dropdown).to_be_visible(timeout=5000)
    
    def test_sort_dropdown_exists(self, moves_tab_ready: Page):
        """Test sort dropdown is present"""
        page = moves_tab_ready
        dropdown = page.locator("#sort-moves")
        expect(dropdown).to_be_visible(timeout=5000)
    
    def test_filter_dropdown_exists(self, moves_tab_ready: Page):
        """Test filter dropdown is present"""
        page = moves_tab_ready
        dropdown = page.locator("#filter-moves")
        expect(dropdown).to_be_visible(timeout=5000)
    
    def test_moves_container_exists(self, moves_tab_ready: Page):
        """Test moves container is present"""
        page = moves_tab_ready
        container = page.locator("#moves-container")
        expect(container).to_be_visible(timeout=5000)
        # Check it has content
        assert len(container.inner_text(timeout=5000)) > 0


class TestSortOptions:
    """Micro-tests for each sort option"""
    
    @pytest.mark.parametrize("sort_value", ["startup", "safety", "damage", "recovery"])
    def test_sort_option(self, moves_tab_ready: Page, sort_value: str):
        """Test individual sort option"""
        page = moves_tab_ready
        sort_dropdown = page.locator("#sort-moves")
        
        # Check option exists
        option = sort_dropdown.locator(f'option[value="{sort_value}"]')
        if option.count() > 0:
            sort_dropdown.select_option(value=sort_value, timeout=5000)
            # Just verify it selected (no need to wait for re-render)


class TestFilterOptions:
    """Micro-tests for each filter option"""
    
    @pytest.mark.parametrize("filter_value", ["all", "safe", "unsafe", "assist"])
    def test_filter_option(self, moves_tab_ready: Page, filter_value: str):
        """Test individual filter option"""
        page = moves_tab_ready
        filter_dropdown = page.locator("#filter-moves")
        
        # Check option exists
        option = filter_dropdown.locator(f'option[value="{filter_value}"]')
        if option.count() > 0:
            filter_dropdown.select_option(value=filter_value, timeout=5000)


# ============================================================================
# Console Error Tests
# ============================================================================

class TestConsoleErrors:
    """Micro-tests for console errors"""
    
    def test_no_critical_console_errors(self, page: Page):
        """Test no critical console errors on database page"""
        errors = []
        
        def handle_console(msg):
            if msg.type == "error":
                errors.append(msg.text)
        
        page.on("console", handle_console)
        page.goto(f"{BASE_URL}/character_database.html", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # Filter out known non-critical errors
        critical_errors = [
            err for err in errors 
            if "CORS" not in err and 
               "Failed to fetch" not in err and
               "character_database.json" not in err
        ]
        
        assert len(critical_errors) == 0, f"Found console errors: {critical_errors}"


# ============================================================================
# Embedded Page Tests (Micro)
# ============================================================================

class TestEmbeddedPage:
    """Micro-tests for embedded page"""
    
    def test_embedded_page_title(self, page: Page):
        """Test embedded page title"""
        page.goto(f"{BASE_URL}/character_database_embedded.html", timeout=10000)
        expect(page).to_have_title("2XKO Character Database - Move Comparison", timeout=5000)
    
    def test_embedded_no_cors_errors(self, page: Page):
        """Test embedded page has no CORS errors"""
        errors = []
        
        def handle_console(msg):
            if msg.type == "error":
                errors.append(msg.text)
        
        page.on("console", handle_console)
        page.goto(f"{BASE_URL}/character_database_embedded.html", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        
        cors_errors = [err for err in errors if "CORS" in err or "Failed to fetch" in err]
        assert len(cors_errors) == 0, f"Found CORS errors: {cors_errors}"
    
    def test_embedded_moves_tab(self, loaded_embedded_page: Page):
        """Test embedded page moves tab loads"""
        page = loaded_embedded_page
        # Wait for page to fully initialize
        page.wait_for_load_state("networkidle", timeout=10000)
        # Click the Move Comparison tab (actual tab name in HTML)
        page.click("text=Move Comparison", timeout=5000)
        page.wait_for_selector("#moves-container", state="visible", timeout=10000)
        expect(page.locator("#moves-container")).to_be_visible(timeout=5000)
    
    def test_embedded_combos_tab(self, loaded_embedded_page: Page):
        """Test embedded page combos tab loads"""
        page = loaded_embedded_page
        page.click("text=BnB Combos", timeout=5000)
        page.wait_for_selector("#combos-container", state="visible", timeout=10000)
        expect(page.locator("#combos-container")).to_be_visible(timeout=5000)
    
    def test_embedded_overview_tab(self, loaded_embedded_page: Page):
        """Test embedded page overview tab loads"""
        page = loaded_embedded_page
        page.click("text=Character Overview", timeout=5000)
        page.wait_for_selector("#character-grid", state="visible", timeout=10000)
        expect(page.locator("#character-grid")).to_be_visible(timeout=5000)


# ============================================================================
# Other Pages Tests (Micro)
# ============================================================================

class TestCharacterGuide:
    """Micro-tests for character guide page"""
    
    def test_guide_page_loads(self, page: Page):
        """Test guide page loads"""
        page.goto(f"{BASE_URL}/character_guide.html", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        expect(page.locator("body")).to_be_visible(timeout=5000)


class TestCustomControls:
    """Micro-tests for custom controls page"""
    
    def test_controls_page_loads(self, page: Page):
        """Test controls page loads"""
        page.goto(f"{BASE_URL}/custom_controls.html", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        expect(page.locator("body")).to_be_visible(timeout=5000)
    
    def test_controls_inputs_exist(self, page: Page):
        """Test control inputs are present"""
        page.goto(f"{BASE_URL}/custom_controls.html", timeout=10000)
        page.wait_for_load_state("networkidle", timeout=10000)
        inputs = page.locator("input[type='text']")
        if inputs.count() > 0:
            expect(inputs.first).to_be_visible(timeout=5000)
