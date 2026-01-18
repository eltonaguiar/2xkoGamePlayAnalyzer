"""
Generate character_database.html with embedded JSON data.
This avoids CORS issues when opening HTML files directly from the file system.
"""

import json
import subprocess
import sys
from generate_database import generate_character_database


def validate_before_generating():
    """Run JavaScript validation before generating"""
    try:
        result = subprocess.run(
            [sys.executable, 'validate_javascript.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            print("\n[WARNING] JavaScript validation found issues:")
            print(result.stdout)
            print("\nContinuing with generation anyway...")
    except Exception as e:
        print(f"[INFO] Could not run validation: {e}")
        print("Continuing with generation...")


def generate_embedded_html():
    """Generate HTML with JSON data embedded"""
    
    # Validate JavaScript first
    print("Validating JavaScript...")
    validate_before_generating()
    
    # Generate the database
    print("\nGenerating character database...")
    database = generate_character_database()
    
    # Read the base HTML template
    with open('output/character_database.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Convert database to JSON string (minified for embedding)
    json_data = json.dumps(database, separators=(',', ':'))
    
    # Find the loadDatabase function and replace the fetch call
    # Look for the async function loadDatabase pattern
    start_marker = 'async function loadDatabase() {'
    
    # Find the function
    start_idx = html_content.find(start_marker)
    if start_idx == -1:
        print("[ERROR] Could not find loadDatabase function")
        return None
    
    # Find the matching closing brace (find the one that closes the async function)
    # Count braces to find the right one
    brace_count = 0
    in_function = False
    end_idx = start_idx
    
    for i in range(start_idx, len(html_content)):
        if html_content[i] == '{':
            brace_count += 1
            in_function = True
        elif html_content[i] == '}':
            brace_count -= 1
            if in_function and brace_count == 0:
                end_idx = i + 1
                break
    
    # Create the new function with embedded data
    new_function = f'''        async function loadDatabase() {{
            try {{
                // Use embedded data instead of fetching (avoids CORS issues)
                databaseData = {json_data};
                
                // Convert database format to characterData format for compatibility
                if (databaseData && databaseData.characters) {{
                    Object.keys(databaseData.characters).forEach(charName => {{
                        const char = databaseData.characters[charName];
                        if (char && char.info) {{
                            characterData[charName] = {{
                                health: char.info.health || 0,
                                archetype: char.info.archetype || '',
                                playstyle: char.info.playstyle || '',
                                moves: char.moves || [],  // Already in array format
                                combos: Object.values(char.bnb_combos || {{}})
                            }};
                        }}
                    }});
                }}
                
                // Initialize UI after data loads
                if (typeof initializeUI === 'function') {{
                    initializeUI();
                }} else {{
                    console.error('initializeUI function not found');
                }}
            }} catch (error) {{
                console.error('Error loading database:', error);
                const body = document.body;
                if (body) {{
                    body.innerHTML = `
                        <div style="padding: 50px; text-align: center;">
                            <h1>Error Loading Database</h1>
                            <p>Error: ${{error.message}}</p>
                            <p>Check browser console for details</p>
                        </div>
                    `;
                }}
            }}
        }}'''
    
    # Replace the function
    new_html = html_content[:start_idx] + new_function + html_content[end_idx:]
    
    # Save the embedded version
    output_file = 'output/character_database_embedded.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"[OK] Embedded HTML generated: {output_file}")
    print(f"[OK] This file works when opened directly from file system (no server needed)")
    print(f"[OK] Total characters: {len(database['characters'])}")
    for char_name, char_data in database['characters'].items():
        moves_count = len(char_data['moves'])
        combos_count = len(char_data['bnb_combos'])
        print(f"  - {char_name}: {moves_count} moves, {combos_count} combos")
    
    # Validate the generated file
    print("\nValidating generated file...")
    try:
        result = subprocess.run(
            [sys.executable, 'validate_javascript.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("[OK] Generated file passed validation!")
        else:
            print("[WARNING] Generated file has some issues:")
            print(result.stdout)
    except Exception as e:
        print(f"[INFO] Could not validate generated file: {e}")
    
    return output_file


if __name__ == "__main__":
    print("Generating embedded HTML (works without server)...")
    print()
    generate_embedded_html()
    print()
    print("="*60)
    print("[OK] EMBEDDED HTML GENERATED!")
    print("="*60)
    print("\nOpen: output/character_database_embedded.html")
    print("This file works when opened directly (no CORS errors)!")
