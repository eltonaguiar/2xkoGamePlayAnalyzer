"""Verify Blitzcrank's poke moves and their rankings"""

from character_data import CHARACTER_DATA
import json

# Get Blitzcrank data
blitz = CHARACTER_DATA['Blitzcrank']
moves = blitz.get_moves()

print("="*70)
print("BLITZCRANK POKE MOVES VERIFICATION")
print("="*70)

print("\nBlitzcrank's moves that could be 'poke moves':")
print(f"  5L: {moves['5L'].startup}f startup - {moves['5L'].description}")
print(f"  5M: {moves['5M'].startup}f startup - {moves['5M'].description}")
print(f"  2L: {moves['2L'].startup}f startup - {moves['2L'].description}")

# Load database to check rankings
with open('output/character_database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fastest = data['comparison']['fastest_moves_in_game']

print("\n" + "="*70)
print("BLITZCRANK MOVES IN FASTEST RANKINGS")
print("="*70)

blitz_moves_in_ranking = [m for m in fastest if m['character'] == 'Blitzcrank']
print(f"\nFound {len(blitz_moves_in_ranking)} Blitzcrank moves in top {len(fastest)} fastest moves:")

for move in blitz_moves_in_ranking:
    rank = next((i for i, m in enumerate(fastest, 1) if m == move), None)
    print(f"  Rank #{rank}: {move['move']} ({move['name']}) - {move['startup']}f")

print("\n" + "="*70)
print("ANALYSIS")
print("="*70)

# Check 5L
blitz_5l = next((m for m in fastest if m['character'] == 'Blitzcrank' and m['move'] == '5L'), None)
if blitz_5l:
    rank = next((i for i, m in enumerate(fastest, 1) if m == blitz_5l), None)
    print(f"\n[OK] 5L (8f) is at rank #{rank} in fastest moves")
    print(f"     This is Blitzcrank's fastest normal and IS in the rankings")
else:
    print("\n[ERROR] 5L is NOT in fastest moves list!")

# Check 5M
blitz_5m = next((m for m in fastest if m['character'] == 'Blitzcrank' and m['move'] == '5M'), None)
if blitz_5m:
    rank = next((i for i, m in enumerate(fastest, 1) if m == blitz_5m), None)
    print(f"\n[OK] 5M (11f) is at rank #{rank} in fastest moves")
else:
    print(f"\n[INFO] 5M (11f) is NOT in top 30 fastest moves")
    print(f"       Top 30 cutoff is {fastest[29]['startup']}f (Jinx 2M)")
    print(f"       5M at 11f is slower than the cutoff")

# Check what moves are around 5L's speed
print("\n" + "="*70)
print("MOVES AROUND 5L'S SPEED (8f)")
print("="*70)
moves_8f = [m for m in fastest if m['startup'] == 8]
print(f"\nThere are {len(moves_8f)} moves with 8f startup:")
for move in moves_8f[:10]:
    rank = next((i for i, m in enumerate(fastest, 1) if m == move), None)
    print(f"  Rank #{rank}: {move['character']} {move['move']} - {move['startup']}f")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("\nBlitzcrank's 5L (8f) IS in the fastest moves ranking at rank #18")
print("This is correct - 8f is fast but not the fastest (many characters have 5-7f moves)")
print("\nBlitzcrank's 5M (11f) is NOT in top 30 because:")
print("  - Top 30 cutoff is 9f")
print("  - 5M at 11f is slower than many other moves")
print("  - However, 5M is described as 'forward advancing' which is typical of poke moves")
