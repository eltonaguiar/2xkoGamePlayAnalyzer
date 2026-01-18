# 📋 Cheat Sheets - Quick Start

Welcome to the 2XKO Cheat Sheet System! Here's what you need to know to get started quickly.

## 🎯 I Want To...

### → **Study the character in-depth**
**Read:** [MOVE_CHEAT_SHEET.md](MOVE_CHEAT_SHEET.md)
- Complete move list
- Full frame data
- Strategic recommendations
- Combo framework

### → **Have quick reference during matches**
**Read:** [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- One-page reference
- Most important moves
- Punish guide
- Frame advantage

### → **Print a cheat sheet**
**Print:** [PRINTABLE_CHEAT_SHEET.txt](PRINTABLE_CHEAT_SHEET.txt)
- ASCII table layout
- All essential info
- Fits on one page

### → **Understand the cheat sheet system**
**Read:** [CHEAT_SHEET_GUIDE.md](CHEAT_SHEET_GUIDE.md)
- How to use all resources
- Integration with analyzer
- How to update cheat sheets

### → **Get a quick overview**
**Read:** [CHEAT_SHEET_SUMMARY.md](CHEAT_SHEET_SUMMARY.md)
- What's been created
- Key information at a glance
- Quick tips

### → **Add a new character**
**Edit:** `character_data.py`
**Run:** `python generate_cheat_sheet.py [CharacterName]`

---

## ⚡ Most Important Info (Blitzcrank)

### 3 Key Moves:

1. **2S1 (Air Purifier)** - +44 on block!
   - Safest move in the game
   - Perfect anti-air
   - Never needs assist

2. **5S1 (Rocket Grab)** - Safe at range
   - Controls space
   - Forces opponent close
   - Core zoning tool

3. **2S2 (Garbage Collection)** - UNBLOCKABLE
   - Command grab (can't be blocked!)
   - ⚠️ HIGH RISK - only use with assist or setup
   - Your 50-50 win condition

### Frame Situations:
- **2S1 on block: +44** (YOU GET FREE MIXUP!)
- **5L on block: -2** (Slightly unsafe, cancel or space it)

### Gameplan:
1. Zone with Rocket Grab
2. Anti-air with Air Purifier
3. Get close, then mix strikes and grabs
4. Use assists to cover risky moves
5. Don't spam command grab!

---

## 📁 All Files

| File | Size | Purpose |
|------|------|---------|
| **MOVE_CHEAT_SHEET.md** | 13 KB | Complete reference guide |
| **QUICK_REFERENCE.md** | 3 KB | One-page quick reference |
| **PRINTABLE_CHEAT_SHEET.txt** | 5 KB | Printable format |
| **CHEAT_SHEET_GUIDE.md** | 8 KB | Documentation |
| **CHEAT_SHEET_SUMMARY.md** | 7 KB | Overview |
| **generate_cheat_sheet.py** | 9 KB | Generator script |
| **output/Blitzcrank_cheat_sheet.txt** | 5 KB | Auto-generated text |
| **output/Blitzcrank_cheat_sheet.json** | 10 KB | Auto-generated JSON |

---

## 🔄 Quick Commands

```bash
# Generate/update cheat sheets
python generate_cheat_sheet.py Blitzcrank

# Run analyzer with cheat sheet integration
python analyzer.py --video "gameplay.mp4" --matchup mirror --character Blitzcrank
```

---

## 📚 Learning Path

### Beginner:
1. Read **QUICK_REFERENCE.md**
2. Practice the 3 key moves (2S1, 5S1, 2S2)
3. Learn when to use assists

### Intermediate:
1. Read **MOVE_CHEAT_SHEET.md**
2. Study frame advantage situations
3. Learn punish opportunities
4. Practice combo framework

### Advanced:
1. Study detailed frame data
2. Learn all move properties
3. Master risk/reward decisions
4. Use analyzer for gameplay review

---

## 🆘 Common Questions

### Q: What's the safest move?
**A:** 2S1 (Air Purifier) - +44 on block!

### Q: When should I use command grab?
**A:** Only with assist cover OR when opponent whiffs big move OR after heavy conditioning. Never spam it!

### Q: What if opponent keeps jumping?
**A:** Use 2S1 (Air Purifier). It's +44 even if they block, so totally safe!

### Q: How do I punish opponent mistakes?
**A:** See the punish guide in QUICK_REFERENCE.md. Quick answer: if they whiff a big move, you get a free command grab!

### Q: Do I always need assists?
**A:** Not for 2S1 (it's already super safe). But YES for command grab mixups and covering unsafe moves.

---

## 🎯 Pro Tips

1. **Print PRINTABLE_CHEAT_SHEET.txt** and keep it next to your setup
2. **Study one move at a time** in training mode
3. **2S1 is your best friend** - use it liberally vs jumpers
4. **Assists cover 2S2** - never do naked command grab without setup
5. **Frame advantage matters** - learn the +44 situation after 2S1

---

## 📊 Data Quality

| Move | Frame Data | Strategic Notes | Complete? |
|------|------------|-----------------|-----------|
| 5L | ✅ Complete | ✅ Complete | ✅ Yes |
| 2S1 | ✅ Complete | ✅ Complete | ✅ Yes |
| 2S2 | ⚠️ Partial | ✅ Complete | ⚠️ Partial |
| 5S1 | ⚠️ Partial | ✅ Complete | ⚠️ Partial |
| Others | ⚠️ Minimal | ⚠️ Basic | ❌ No |

**Note:** Frame data is being expanded. Check https://wiki.play2xko.com for latest updates.

---

## 🚀 Start Here!

**For immediate use:**
1. Open [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Read the "Most Important Moves" section
3. Practice 2S1, 5S1, and 2S2 in training mode
4. Come back to this guide as you learn!

**Good luck!** 🎮

---

*Last updated: 2026-01-17*  
*Data source: https://wiki.play2xko.com*
