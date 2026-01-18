"""
Improved wiki scraper that properly extracts frame data from 2XKO wiki pages.
Uses the actual wiki HTML structure to parse frame data tables.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Optional
import time

BASE_URL = "https://wiki.play2xko.com/en-us"


def extract_number_from_text(text: str) -> Optional[int]:
    """Extract first number from text"""
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else None


def extract_signed_number(text: str) -> Optional[int]:
    """Extract signed number like +4, -2, etc."""
    match = re.search(r'([+-]?\d+)', text)
    return int(match.group(1)) if match else None


def parse_frame_data_table(table) -> Optional[Dict]:
    """Parse frame data table from wiki - improved version"""
    if not table or not hasattr(table, 'find_all'):
        return None
    
    rows = table.find_all('tr')
    if len(rows) < 2:
        return None
    
    # Get headers from first row
    headers = []
    for cell in rows[0].find_all(['th', 'td']):
        header_text = cell.get_text(strip=True)
        if header_text:
            headers.append(header_text.lower())
    
    # Get data from second row (usually the main data row)
    data_row = rows[1]
    data_cells = []
    for cell in data_row.find_all(['td', 'th']):
        cell_text = cell.get_text(strip=True)
        data_cells.append(cell_text)
    
    frame_data = {}
    
    # Map headers to values
    for i, header in enumerate(headers):
        if i >= len(data_cells):
            continue
        
        value = data_cells[i]
        
        # Damage
        if 'damage' in header:
            num = extract_number_from_text(value)
            if num is not None:
                frame_data['damage'] = num
        
        # Startup
        elif 'startup' in header:
            num = extract_number_from_text(value)
            if num is not None:
                frame_data['startup'] = num
        
        # Active
        elif 'active' in header:
            num = extract_number_from_text(value)
            if num is not None:
                frame_data['active'] = num
        
        # Recovery
        elif 'recovery' in header:
            num = extract_number_from_text(value)
            if num is not None:
                frame_data['recovery'] = num
        
        # On-Block
        elif 'on-block' in header or 'on block' in header:
            num = extract_signed_number(value)
            if num is not None:
                frame_data['on_block'] = num
        
        # Guard
        elif 'guard' in header:
            frame_data['guard'] = value
    
    return frame_data if frame_data else None


def find_move_sections(soup: BeautifulSoup) -> Dict[str, Dict]:
    """Find all move sections and their frame data"""
    moves = {}
    
    # Find all headers that might contain move names
    # Look for h2, h3, h4 with move patterns
    move_headers = soup.find_all(['h2', 'h3', 'h4', 'h5'], string=re.compile(
        r'^(5L|5M|5H|2L|2M|2H|j\.L|j\.M|j\.H|j\.2H|Special|Super|Ultimate|Rocket|Garbage|Air|Steam)', 
        re.I
    ))
    
    for header in move_headers:
        header_text = header.get_text(strip=True)
        
        # Extract move identifier
        move_match = re.match(r'^(\d+[LMH]|j\.\d*[LMH]|Special\s*\d+|Super\s*\d+|Ultimate|Rocket|Garbage|Air|Steam)', header_text, re.I)
        if not move_match:
            continue
        
        move_id = move_match.group(1)
        
        # Normalize move ID
        move_id = move_id.replace(' ', '').upper()
        if move_id.startswith('SPECIAL'):
            move_id = move_id.replace('SPECIAL', 'S')
        elif move_id.startswith('SUPER'):
            move_id = move_id.replace('SUPER', 'SU')
        
        # Find table after this header
        current = header
        table = None
        
        # Look in next siblings
        for _ in range(20):
            if not hasattr(current, 'next_sibling'):
                break
            current = current.next_sibling
            if current is None:
                break
            
            if hasattr(current, 'name'):
                if current.name == 'table':
                    table = current
                    break
                elif hasattr(current, 'find'):
                    found_table = current.find('table')
                    if found_table:
                        table = found_table
                        break
        
        # Also try find_next
        if not table:
            table = header.find_next('table')
        
        if table:
            frame_data = parse_frame_data_table(table)
            if frame_data:
                moves[move_id] = frame_data
                print(f"  [OK] {move_id}: {frame_data.get('startup', '?')}f startup, {frame_data.get('on_block', '?')} on block")
    
    return moves


def scrape_character(character_name: str) -> Dict:
    """Scrape a single character's wiki page"""
    url = f"{BASE_URL}/{character_name}"
    
    print(f"\n[INFO] Scraping {character_name}...")
    print(f"  URL: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find move sections
        moves = find_move_sections(soup)
        
        # Get character info
        info = {}
        
        # Try to find health and archetype
        overview_section = soup.find('div', id='Overview') or soup.find('h2', string=re.compile('Overview', re.I))
        if overview_section:
            text = overview_section.get_text()
            health_match = re.search(r'Health[:\s]+(\d+)', text, re.I)
            if health_match:
                info['health'] = int(health_match.group(1))
            
            archetype_match = re.search(r'Archetype[:\s]+(\w+)', text, re.I)
            if archetype_match:
                info['archetype'] = archetype_match.group(1)
        
        print(f"[OK] Scraped {len(moves)} moves for {character_name}")
        
        return {
            'name': character_name,
            'info': info,
            'moves': moves
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to scrape {character_name}: {e}")
        import traceback
        traceback.print_exc()
        return {
            'name': character_name,
            'info': {},
            'moves': {}
        }


def scrape_all_characters(characters: List[str]) -> Dict[str, Dict]:
    """Scrape all characters"""
    all_data = {}
    
    for char_name in characters:
        char_data = scrape_character(char_name)
        all_data[char_name] = char_data
        time.sleep(2)  # Be respectful
    
    return all_data


if __name__ == "__main__":
    characters = ["Blitzcrank", "Ahri", "Braum", "Darius", "Ekko", 
                  "Illaoi", "Yasuo", "Jinx", "Vi", "Teemo", "Warwick"]
    
    print("="*70)
    print("Scraping 2XKO Wiki for Character Frame Data")
    print("="*70)
    
    scraped_data = scrape_all_characters(characters)
    
    # Save to file
    output_file = "output/scraped_wiki_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print(f"[OK] Scraping complete!")
    print(f"[OK] Saved to: {output_file}")
    print(f"[OK] Scraped {len(scraped_data)} characters")
    
    # Summary
    for char_name, data in scraped_data.items():
        move_count = len(data.get('moves', {}))
        print(f"  - {char_name}: {move_count} moves")
