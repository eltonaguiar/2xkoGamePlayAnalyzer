"""
Comprehensive script to update all characters from 2XKO wiki.
Scrapes wiki pages and updates character_data.py with real frame data.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Optional
import time

BASE_URL = "https://wiki.play2xko.com/en-us"
ALL_CHARACTERS = [
    "Ahri", "Braum", "Darius", "Ekko", "Illaoi", 
    "Yasuo", "Jinx", "Vi", "Blitzcrank", "Teemo", "Warwick"
]


def parse_frame_table(table) -> Optional[Dict]:
    """Parse frame data from wiki table"""
    if not table:
        return None
    
    rows = table.find_all('tr')
    if len(rows) < 2:
        return None
    
    # Get headers
    headers = []
    for th in rows[0].find_all(['th', 'td']):
        header_text = th.get_text(strip=True)
        headers.append(header_text)
    
    # Get data from second row
    data_cells = []
    for td in rows[1].find_all(['td', 'th']):
        cell_text = td.get_text(strip=True)
        data_cells.append(cell_text)
    
    frame_data = {}
    
    # Map headers to values
    for i, header in enumerate(headers):
        if i >= len(data_cells):
            continue
        
        value = data_cells[i]
        header_lower = header.lower()
        
        # Damage
        if 'damage' in header_lower:
            match = re.search(r'(\d+)', value)
            if match:
                frame_data['damage'] = int(match.group(1))
        
        # Startup
        elif 'startup' in header_lower:
            match = re.search(r'(\d+)', value)
            if match:
                frame_data['startup'] = int(match.group(1))
        
        # Active
        elif 'active' in header_lower:
            match = re.search(r'(\d+)', value)
            if match:
                frame_data['active'] = int(match.group(1))
        
        # Recovery
        elif 'recovery' in header_lower:
            match = re.search(r'(\d+)', value)
            if match:
                frame_data['recovery'] = int(match.group(1))
        
        # On-Block
        elif 'on-block' in header_lower or 'on block' in header_lower:
            match = re.search(r'([+-]?\d+)', value)
            if match:
                frame_data['on_block'] = int(match.group(1))
        
        # Guard
        elif 'guard' in header_lower:
            frame_data['guard'] = value
    
    return frame_data if frame_data else None


def scrape_character_moves(character_name: str) -> Dict[str, Dict]:
    """Scrape all moves for a character from wiki"""
    url = f"{BASE_URL}/{character_name}"
    
    print(f"[INFO] Scraping {character_name}...")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        moves = {}
        
        # Find all move sections (h3 or h4 with move names)
        # Look for sections like "5L", "5M", "2L", "Special 1", etc.
        move_pattern = re.compile(r'^(5L|5M|5H|2L|2M|2H|j\.|Special|Super|Ultimate)', re.I)
        
        # Find all headers that might be moves
        headers = soup.find_all(['h3', 'h4', 'h5'])
        
        for header in headers:
            header_text = header.get_text(strip=True)
            
            # Check if this looks like a move header
            if not move_pattern.match(header_text):
                continue
            
            # Extract move input (first part of header)
            move_parts = header_text.split()
            if not move_parts:
                continue
            
            move_input = move_parts[0]
            
            # Find the frame data table after this header
            current = header.next_sibling
            table = None
            
            # Look for table in next few siblings
            for _ in range(10):
                if current is None:
                    break
                if hasattr(current, 'name') and current.name == 'table':
                    table = current
                    break
                if hasattr(current, 'find'):
                    table = current.find('table')
                    if table:
                        break
                current = getattr(current, 'next_sibling', None)
            
            if not table:
                # Try finding in next element
                next_elem = header.find_next('table')
                if next_elem:
                    table = next_elem
            
            if table:
                frame_data = parse_frame_table(table)
                if frame_data:
                    moves[move_input] = frame_data
                    print(f"  [OK] Found {move_input}: {frame_data.get('startup', '?')}f startup")
        
        print(f"[OK] Scraped {len(moves)} moves for {character_name}")
        return moves
        
    except Exception as e:
        print(f"[ERROR] Failed to scrape {character_name}: {e}")
        return {}


def scrape_all_characters() -> Dict[str, Dict[str, Dict]]:
    """Scrape all characters"""
    all_data = {}
    
    for char_name in ALL_CHARACTERS:
        moves = scrape_character_moves(char_name)
        all_data[char_name] = moves
        time.sleep(2)  # Be respectful to the server
    
    return all_data


def save_scraped_data(data: Dict, filename: str = "output/scraped_wiki_data.json"):
    """Save scraped data"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Saved scraped data to {filename}")


if __name__ == "__main__":
    print("Scraping 2XKO Wiki for all character frame data...")
    print("="*70)
    
    scraped_data = scrape_all_characters()
    save_scraped_data(scraped_data)
    
    print("\n" + "="*70)
    print(f"[OK] Scraping complete! Got data for {len(scraped_data)} characters")
    print("\nNext: Use this data to update character_data.py")
