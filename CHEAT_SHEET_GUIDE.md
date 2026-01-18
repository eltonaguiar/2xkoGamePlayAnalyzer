# Cheat Sheet Documentation

This project now includes comprehensive cheat sheets for character moves, frame data, and strategic recommendations.

## Available Cheat Sheet Resources

### 1. **MOVE_CHEAT_SHEET.md** - Complete Reference Guide
**Location**: `MOVE_CHEAT_SHEET.md`

The master reference document containing:
- Complete move list with frame data
- Recovery times for each move
- On-block frame advantage
- Guard types (low/high/air/unblockable)
- Strategic usage notes
- Risk levels for each move
- When to use assists
- Punish opportunities
- Common mistakes to avoid
- Combo framework
- Notation guide

**Best for**: Study, in-depth learning, reference when not in a match

---

### 2. **QUICK_REFERENCE.md** - Quick Reference Card
**Location**: `QUICK_REFERENCE.md`

A condensed one-page reference containing:
- Most important moves (2S1, 5S1, 2S2)
- Frame advantage quick guide
- Punish guide by situation
- When to use assists
- Gameplan summary
- Common mistakes
- Strengths vs weaknesses

**Best for**: Quick lookup during matches, printing out, second monitor reference

---

### 3. **Generated Cheat Sheets** - Programmatic Access
**Location**: `output/Blitzcrank_cheat_sheet.txt` and `output/Blitzcrank_cheat_sheet.json`

Auto-generated from character data:
- Text version: Human-readable formatted output
- JSON version: Machine-readable for integration with other tools
- Includes recovery analysis
- Strategic recommendations
- Punish opportunities by situation

**Generation**: Run `python generate_cheat_sheet.py [CharacterName]`

**Best for**: Integration with the analyzer, programmatic access, ensuring data consistency

---

### 4. **Enhanced Character Data** - In-Code Reference
**Location**: `character_data.py`

The source of truth with enhanced `MoveData` class including:
- `requires_assist`: Boolean flag for moves needing assist cover
- `requires_setup`: Boolean flag for moves needing opponent mistakes
- `usage_notes`: Strategic recommendations
- `risk_level`: "low", "medium", or "high"

**New Methods**:
- `get_move_recommendations()`: Get strategic recommendations by situation
- `get_recovery_analysis()`: Get detailed recovery time analysis

**Best for**: Developers, analyzer integration, adding new characters

---

## Key Information Summary

### Blitzcrank Move Safety Guide

#### ✅ SAFE MOVES (Use Freely)
1. **2S1 (Air Purifier)** - +44 on block (SAFEST MOVE!)
   - Recovery: 119 frames
   - Total frames: 153
   - Perfect anti-air
   - NEVER needs assist

2. **5S1 (Rocket Grab)** - Safe at range
   - Controls space
   - Forces opponent to approach
   - Enhanced version adds shock

#### ⚠️ UNSAFE MOVES (Use with Caution)
1. **5L (Light Punch)** - -2 on block
   - Recovery: 12 frames
   - Total frames: 25
   - Can be made safe with cancels or spacing

#### 🔴 HIGH RISK MOVES (Only with Assist/Setup)
1. **2S2 (Garbage Collection)** - UNBLOCKABLE Command Grab
   - **REQUIRES ASSIST** or opponent mistake
   - Very punishable on whiff
   - Enhanced version has armor
   - Only use when:
     - Opponent whiffs big move
     - You have assist covering
     - After heavy conditioning

---

## Recovery Time Breakdown

| Move | Recovery | Total Frames | On Block | Safety |
|------|----------|--------------|----------|--------|
| 5L   | 12       | 25           | -2       | Slightly Unsafe |
| 2S1  | 119      | 153          | +44      | VERY SAFE |
| 2S2  | Unknown  | Unknown      | N/A      | High Risk (Grab) |

---

## When to Use Assists

### ALWAYS Use Assist For:
- **2S2 (Garbage Collection)** - Command grab mixup needs cover
- **Whiffed heavy normals** - Cover your recovery
- **Unsafe block situations** - When minus on block

### OPTIONAL Assist For:
- **5L** - Can be made safe with spacing/cancels
- **5S1** - Already decent at range
- **Combo extensions** - For bigger damage

### NEVER Need Assist For:
- **2S1 (Air Purifier)** - Already +44 on block!

---

## Punish Opportunities

### Opponent Whiffs Big Move (Long Recovery)
✅ 2S2 (Garbage Collection) - FREE GRAB!
✅ 5S1 (Rocket Grab) → Combo
✅ Jump-in → Full Combo
✅ Heaviest combo starter

### Opponent Jumps
✅ 2S1 (Air Purifier) - +44 even if blocked!
✅ j.S1 (Air Rocket Grab) - Air-to-air
✅ Anti-air normals

### Opponent Blocks Too Much
✅ 2S2 (Garbage Collection) + Assist
✅ Regular Throw
⚠️ Call assist first for safety

### Opponent Very Minus (Blocked Unsafe Move)
✅ Fastest normal → Combo
✅ 2S2 if close
✅ Super if meter available

---

## Frame Advantage Guide

| Frame Advantage | Meaning | Action |
|----------------|---------|--------|
| +10 or more    | HUGE advantage | FREE mixup/pressure |
| +1 to +9       | Good advantage | Your turn to attack |
| 0 to -2        | Slightly unsafe | Contest or retreat |
| -3 to -5       | Unsafe | Opponent can attack |
| -6 or worse    | VERY UNSAFE | Full punish available |

### Blitzcrank's Frame Situations:
- **2S1 on block (+44)**: YOU GET FREE MIXUP! 🎉
- **5L on block (-2)**: Slightly unsafe, space or cancel

---

## How to Use These Resources

### Before a Match:
1. Review **MOVE_CHEAT_SHEET.md** for detailed strategy
2. Print out **QUICK_REFERENCE.md** for quick access
3. Practice key moves: 2S1, 5S1, 2S2

### During a Match:
1. Keep **QUICK_REFERENCE.md** nearby
2. Reference punish guide for opponent mistakes
3. Check frame advantage when unsure

### After a Match:
1. Run the analyzer on your gameplay video
2. Check generated JSON for specific move usage
3. Review **MOVE_CHEAT_SHEET.md** for mistakes made

### When Learning New Character:
1. Read character info section
2. Learn safe moves first (2S1, 5S1)
3. Practice high-risk moves with assist (2S2)
4. Study punish opportunities
5. Understand strengths and weaknesses

---

## Generating Updated Cheat Sheets

When character data is updated, regenerate the cheat sheets:

```bash
python generate_cheat_sheet.py Blitzcrank
```

This creates:
- `output/Blitzcrank_cheat_sheet.txt` - Human-readable text
- `output/Blitzcrank_cheat_sheet.json` - Machine-readable JSON

---

## Integration with Analyzer

The analyzer can now use the enhanced character data to provide:
- Better mistake detection (checking `requires_assist` and `requires_setup`)
- Strategic recommendations based on `usage_notes`
- Risk assessment using `risk_level`
- Contextual advice based on opponent's situation

Example usage in analyzer:
```python
from character_data import BlitzcrankData

# Get move recommendations
recommendations = BlitzcrankData.get_move_recommendations()

# Check if move requires assist
move_data = BlitzcrankData.get_moves()["2S2"]
if move_data.requires_assist:
    print("WARNING: This move should be used with assist!")

# Get recovery analysis
recovery = BlitzcrankData.get_recovery_analysis()
print(recovery["2S1"]["usage_recommendation"])
```

---

## Future Enhancements

Potential additions to the cheat sheet system:
- [ ] More complete frame data for all normals
- [ ] Jump attacks frame data
- [ ] Super moves frame data
- [ ] Combo notation and damage values
- [ ] Matchup-specific notes
- [ ] Additional characters (Ahri, Darius, Ekko, Illaoi, Yasuo)
- [ ] Interactive web-based cheat sheet
- [ ] Video examples linked to each move
- [ ] Training mode drill suggestions

---

## Data Sources

All frame data sourced from: https://wiki.play2xko.com

**Note**: Frame data may change with game patches. Always verify against the latest wiki data and test in training mode.

---

## Quick Tips Summary

1. **2S1 is your safest move** - Use it vs jumpers, +44 on block!
2. **Don't spam command grab** - Setup first with assists or conditioning
3. **Rocket Grab controls space** - Use it to force them into grab range
4. **Your defense is weak** - Don't let them start pressure
5. **Assists are essential** - Cover your risky moves
6. **50-50 is your win condition** - Mix strikes and grabs once close

---

**Remember**: Practice makes perfect. Use these cheat sheets as reference, but develop muscle memory through training mode and real matches!
