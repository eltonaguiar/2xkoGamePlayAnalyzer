"""
Web scraper to fetch character data from 2XKO wiki.
Pulls frame data, strategies, and move information.
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional
import json

BASE_URL = "https://wiki.play2xko.com/en-us"

# All 2XKO characters
ALL_CHARACTERS = [
    "Ahri", "Braum", "Darius", "Ekko", "Illaoi", 
    "Yasuo", "Jinx", "Vi", "Blitzcrank", "Teemo", "Warwick"
]


def parse_frame_data_table(table) -> Optional[Dict]:
    """Parse a frame data table from the wiki"""
    if not table:
        return None
    
    rows = table.find_all('tr')
    if len(rows) < 2:
        return None
    
    # Get headers
    headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
    
    # Get data row (usually second row)
    data_row = rows[1] if len(rows) > 1 else None
    if not data_row:
        return None
    
    data_cells = [td.get_text(strip=True) for td in data_row.find_all(['td', 'th'])]
    
    frame_data = {}
    
    # Map common headers to our fields
    header_mapping = {
        'damage': ['Damage', 'damage'],
        'startup': ['Startup', 'startup'],
        'active': ['Active', 'active'],
        'recovery': ['Recovery', 'recovery'],
        'on_block': ['On-Block', 'On Block', 'on-block', 'on_block'],
        'guard': ['Guard', 'guard'],
        'cancel': ['Cancel', 'cancel']
    }
    
    for i, header in enumerate(headers):
        header_lower = header.lower()
        if i < len(data_cells):
            value = data_cells[i]
            
            # Parse damage
            if any(h in header_lower for h in ['damage']):
                # Extract number
                damage_match = re.search(r'(\d+)', value)
                if damage_match:
                    frame_data['damage'] = int(damage_match.group(1))
            
            # Parse startup
            elif any(h in header_lower for h in ['startup']):
                startup_match = re.search(r'(\d+)', value)
                if startup_match:
                    frame_data['startup'] = int(startup_match.group(1))
            
            # Parse recovery
            elif any(h in header_lower for h in ['recovery']):
                recovery_match = re.search(r'(\d+)', value)
                if recovery_match:
                    frame_data['recovery'] = int(recovery_match.group(1))
            
            # Parse on-block
            elif any(h in header_lower for h in ['on-block', 'on block']):
                # Handle +4, -2, etc.
                on_block_match = re.search(r'([+-]?\d+)', value)
                if on_block_match:
                    frame_data['on_block'] = int(on_block_match.group(1))
            
            # Parse guard
            elif any(h in header_lower for h in ['guard']):
                frame_data['guard'] = value
    
    return frame_data if frame_data else None


def scrape_character_page(character_name: str) -> Dict:
    """Scrape a character's wiki page for data"""
    url = f"{BASE_URL}/{character_name}"
    
    print(f"[INFO] Scraping {character_name} from {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        character_data = {
            'name': character_name,
            'moves': {},
            'info': {},
            'strategies': []
        }
        
        # Get basic info from overview section
        overview = soup.find('div', {'id': 'Overview'}) or soup.find('h2', string=re.compile('Overview', re.I))
        if overview:
            # Try to find health, archetype, etc.
            info_section = overview.find_next()
            if info_section:
                text = info_section.get_text()
                # Extract health
                health_match = re.search(r'Health[:\s]+(\d+)', text, re.I)
                if health_match:
                    character_data['info']['health'] = int(health_match.group(1))
                
                # Extract archetype
                archetype_match = re.search(r'Archetype[:\s]+(\w+)', text, re.I)
                if archetype_match:
                    character_data['info']['archetype'] = archetype_match.group(1)
        
        # Find all move sections
        move_sections = soup.find_all(['h3', 'h4'], string=re.compile(r'^(5L|5M|5H|2L|2M|2H|j\.|Special|Super)', re.I))
        
        for move_header in move_sections:
            move_name = move_header.get_text(strip=True)
            
            # Find the frame data table after this header
            next_table = move_header.find_next('table')
            if next_table:
                frame_data = parse_frame_data_table(next_table)
                if frame_data:
                    # Extract move input from header
                    move_input = move_name.split()[0] if move_name.split() else move_name
                    character_data['moves'][move_input] = frame_data
        
        # Find strategy sections
        strategy_headers = soup.find_all(['h2', 'h3'], string=re.compile(r'Strategy|Guide|Tips', re.I))
        for header in strategy_headers:
            strategy_section = header.find_next(['div', 'section', 'ul'])
            if strategy_section:
                strategies = []
                for item in strategy_section.find_all(['li', 'p']):
                    text = item.get_text(strip=True)
                    if text and len(text) > 20:  # Filter out very short items
                        strategies.append(text)
                
                if strategies:
                    character_data['strategies'].extend(strategies[:5])  # Limit to 5
        
        print(f"[OK] Scraped {len(character_data['moves'])} moves for {character_name}")
        return character_data
        
    except requests.RequestException as e:
        print(f"[ERROR] Failed to scrape {character_name}: {e}")
        return {'name': character_name, 'moves': {}, 'info': {}, 'strategies': []}
    except Exception as e:
        print(f"[ERROR] Error parsing {character_name}: {e}")
        return {'name': character_name, 'moves': {}, 'info': {}, 'strategies': []}


def scrape_all_characters() -> Dict[str, Dict]:
    """Scrape all characters from the wiki"""
    all_data = {}
    
    for char_name in ALL_CHARACTERS:
        char_data = scrape_character_page(char_name)
        all_data[char_name] = char_data
        # Small delay to be respectful
        import time
        time.sleep(1)
    
    return all_data


def save_scraped_data(data: Dict, filename: str = "output/scraped_wiki_data.json"):
    """Save scraped data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved scraped data to {filename}")


if __name__ == "__main__":
    print("Scraping 2XKO Wiki for character data...")
    print("="*70)
    
    # Scrape all characters
    scraped_data = scrape_all_characters()
    
    # Save to file
    save_scraped_data(scraped_data)
    
    print("\n" + "="*70)
    print("[OK] Scraping complete!")
    print(f"Scraped data for {len(scraped_data)} characters")
