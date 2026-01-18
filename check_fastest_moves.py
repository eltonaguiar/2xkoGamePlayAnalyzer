"""Check if Blitzcrank's poke moves are in the fastest moves ranking"""

import json

# Load database
with open('output/character_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get fastest moves
fastest = data['comparison']['fastest_moves_in_game']

print("="*70)
print("TOP 30 FASTEST MOVES IN GAME")
print("="*70)

blitzcrank_found = False
for i, move in enumerate(fastest[:30], 1):
    marker = " <-- BLITZCRANK" if move['character'] == 'Blitzcrank' else ""
    if move['character'] == 'Blitzcrank':
        blitzcrank_found = True
    print(f"{i:2d}. {move['character']:12s} {move['move']:4s} ({move['name']:20s}): {move['startup']:2d}f{marker}")

print("\n" + "="*70)
print("BLITZCRANK MOVES CHECK")
print("="*70)

# Check Blitzcrank's moves
blitz = data['characters']['Blitzcrank']
moves = blitz['moves']

print("\nBlitzcrank's moves sorted by startup:")
blitz_moves = sorted(moves, key=lambda m: m['startup'])
for move in blitz_moves:
    print(f"  {move['move']:4s} ({move['name']:20s}): {move['startup']:2d}f startup")

# Check if 5L and 5M are in top 30
print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

blitz_5l = next((m for m in fastest if m['character'] == 'Blitzcrank' and m['move'] == '5L'), None)
blitz_5m = next((m for m in fastest if m['character'] == 'Blitzcrank' and m['move'] == '5M'), None)

if blitz_5l:
    rank = next((i for i, m in enumerate(fastest, 1) if m == blitz_5l), None)
    print(f"[OK] Blitzcrank 5L found at rank #{rank} ({blitz_5l['startup']}f)")
else:
    print("[ERROR] Blitzcrank 5L NOT in fastest moves list!")

if blitz_5m:
    rank = next((i for i, m in enumerate(fastest, 1) if m == blitz_5m), None)
    print(f"[OK] Blitzcrank 5M found at rank #{rank} ({blitz_5m['startup']}f)")
else:
    print("[WARN] Blitzcrank 5M NOT in top 30 (11f is slower than top 30 cutoff)")

# Check what the cutoff is
print(f"\nFastest move: {fastest[0]['character']} {fastest[0]['move']} ({fastest[0]['startup']}f)")
print(f"30th fastest: {fastest[29]['character']} {fastest[29]['move']} ({fastest[29]['startup']}f)")
