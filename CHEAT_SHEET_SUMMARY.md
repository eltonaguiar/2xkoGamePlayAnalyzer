# Cheat Sheet Summary

## ✅ Successfully Created

Your 2XKO Gameplay Analyzer now has comprehensive cheat sheets covering:

### 📚 Main Documentation Files

1. **MOVE_CHEAT_SHEET.md** (12,943 bytes)
   - Complete move reference with full frame data
   - Recovery times for each move
   - Strategic recommendations
   - Combo framework
   - Notation guide
   - Detailed usage notes

2. **QUICK_REFERENCE.md** (2,684 bytes)
   - One-page quick reference
   - Most important moves
   - Frame advantage guide
   - Punish opportunities
   - When to use assists
   - Perfect for during matches

3. **PRINTABLE_CHEAT_SHEET.txt** (4,991 bytes)
   - Formatted for printing
   - ASCII table layout
   - All key info on one page
   - Easy to read at a glance

4. **CHEAT_SHEET_GUIDE.md** (8,328 bytes)
   - How to use all cheat sheet resources
   - Integration guide for analyzer
   - Future enhancements list
   - Data sources

### 🔧 Generated Files

5. **output/Blitzcrank_cheat_sheet.txt**
   - Auto-generated from character_data.py
   - Organized by risk level
   - Strategic recommendations
   - Punish opportunities

6. **output/Blitzcrank_cheat_sheet.json** (10,367 bytes)
   - Machine-readable format
   - Complete move database
   - Recovery analysis
   - Programmatic access

### 💻 Code Enhancements

7. **character_data.py** (Enhanced)
   - Added `requires_assist` flag
   - Added `requires_setup` flag
   - Added `usage_notes` field
   - Added `risk_level` field
   - New method: `get_move_recommendations()`
   - New method: `get_recovery_analysis()`

8. **generate_cheat_sheet.py** (9,258 bytes)
   - Generates text and JSON cheat sheets
   - Organizes moves by risk level
   - Includes strategic recommendations
   - Usage: `python generate_cheat_sheet.py [CharacterName]`

---

## 📋 Key Information Covered

### ✅ Character Names
- **Blitzcrank** - The Great Steam Golem
- Archetype: Grappler
- Health: 1050

### ✅ Move Recovery Times

| Move | Recovery | Total Frames | On Block | Notes |
|------|----------|--------------|----------|-------|
| **5L** | 12f | 25f | -2 | Slightly unsafe, cancel or space it |
| **2S1** | 119f | 153f | **+44** | SAFEST MOVE! |
| **2S2** | Unknown | Unknown | N/A | High risk grab |

### ✅ Moves Requiring Assists

**ALWAYS Need Assist:**
- **2S2 (Garbage Collection)** - Command grab mixup too risky alone

**OPTIONAL Assist:**
- **5L** - Can be made safe with cancels/spacing
- **Whiffed heavies** - Cover recovery

**NEVER Need Assist:**
- **2S1 (Air Purifier)** - Already +44 on block!

### ✅ Moves for Punishing Opponent Mistakes

**When Opponent Whiffs Big Move (Long Recovery):**
- ✅ **2S2 (Garbage Collection)** - FREE COMMAND GRAB!
- ✅ **5S1 (Rocket Grab)** → Combo
- ✅ Jump-in → Full combo

**When Opponent Jumps:**
- ✅ **2S1 (Air Purifier)** - +44 even on block!
- ✅ **j.S1 (Air Rocket Grab)** - Air-to-air

**When Opponent Blocks Too Much:**
- ✅ **2S2 + Assist** - Command grab beats block
- ✅ **Regular Throw** - Quick and easy

**When Opponent is Very Minus (Blocked Unsafe Move):**
- ✅ **Fastest normal → Combo** - Guaranteed punish
- ✅ **2S2 if close** - Big damage
- ✅ **Super if meter** - Maximum damage

---

## 🎯 Strategic Recommendations

### Safe to Use Freely
1. **2S1 (Air Purifier)** - +44 on block, safest move
2. **5S1 (Rocket Grab)** - Safe at range, controls space

### High Risk (Setup/Assist Only)
1. **2S2 (Garbage Collection)** - Very punishable on whiff
   - Only use with assist cover
   - Only when opponent whiffs big move
   - Only after heavy conditioning

### Anti-Air Options
1. **2S1 (Air Purifier)** - Best option, +44 on block
2. **j.S1 (Air Rocket Grab)** - Air-to-air option

---

## 📊 Frame Advantage Breakdown

| Frame Advantage | Meaning | What to Do |
|----------------|---------|------------|
| **+44** (2S1) | HUGE advantage | FREE MIXUP! |
| **+10 or more** | Massive advantage | Guaranteed pressure |
| **+1 to +9** | Good advantage | Your turn to attack |
| **0 to -2** (5L at -2) | Slightly unsafe | Contest or retreat |
| **-3 to -5** | Unsafe | Opponent can attack |
| **-6 or worse** | VERY UNSAFE | Full punish available |

---

## 🎮 How to Use These Resources

### Before Playing:
1. Read **MOVE_CHEAT_SHEET.md** for full understanding
2. Practice key moves in training mode:
   - 2S1 (Air Purifier)
   - 5S1 (Rocket Grab)
   - 2S2 (Garbage Collection)

### During Matches:
1. Keep **QUICK_REFERENCE.md** or **PRINTABLE_CHEAT_SHEET.txt** nearby
2. Reference punish opportunities when opponent makes mistakes
3. Check when to use assists

### After Matches:
1. Review which moves you used incorrectly
2. Check if you used 2S2 without assist (mistake!)
3. Verify you're anti-airing with 2S1

### For Development:
1. Use **character_data.py** as source of truth
2. Run `generate_cheat_sheet.py` to update after changes
3. Use JSON format for programmatic access

---

## 🔄 Updating Cheat Sheets

When you update `character_data.py`, regenerate the cheat sheets:

```bash
python generate_cheat_sheet.py Blitzcrank
```

This ensures consistency across all formats.

---

## 📁 File Locations

```
2xkoGPAnalyzer/
├── MOVE_CHEAT_SHEET.md          ← Complete reference
├── QUICK_REFERENCE.md           ← Quick lookup
├── PRINTABLE_CHEAT_SHEET.txt    ← Print this!
├── CHEAT_SHEET_GUIDE.md         ← How to use everything
├── character_data.py            ← Source of truth (enhanced)
├── generate_cheat_sheet.py      ← Generator script
└── output/
    ├── Blitzcrank_cheat_sheet.txt   ← Auto-generated text
    └── Blitzcrank_cheat_sheet.json  ← Auto-generated JSON
```

---

## ⚡ Quick Tips

1. **2S1 is your safest move** - Use it vs jumpers, +44 on block!
2. **Don't spam command grab** - Setup first with assists or conditioning
3. **Rocket Grab controls space** - Use it to force them into grab range
4. **Your defense is weak** - Don't let them start pressure
5. **Assists are essential** - Cover your risky moves
6. **50-50 is your win condition** - Mix strikes and grabs once close

---

## 📚 Data Sources

All frame data sourced from: https://wiki.play2xko.com

**Note**: Frame data may change with game patches. Always verify against latest wiki data.

---

## ✅ Mission Complete!

You now have:
- ✅ Character name reference (Blitzcrank)
- ✅ Complete move list with recovery times
- ✅ Moves that require assist usage
- ✅ Moves to only use when opponent makes mistakes
- ✅ Punish opportunities for opponent's long recovery moves
- ✅ Multiple formats (Markdown, Text, JSON)
- ✅ Quick reference cards
- ✅ Printable cheat sheet
- ✅ Programmatic access
- ✅ Integration with analyzer

**Next Steps:**
1. Print out **PRINTABLE_CHEAT_SHEET.txt** for quick reference
2. Study **MOVE_CHEAT_SHEET.md** for detailed strategy
3. Practice key moves in training mode
4. Use the analyzer to review your gameplay
5. Add more characters as needed!
