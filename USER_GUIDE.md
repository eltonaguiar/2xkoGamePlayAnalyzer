# 2XKO Character Database System - User Guide

## 📚 Complete System Overview

This system provides a comprehensive way to analyze, compare, and learn fighting game characters with focus on:
- ✅ Frame data (startup, recovery, safety)
- ✅ Move organization (basics first, then advanced)
- ✅ Strategic guides (top 3 strategies)
- ✅ Matchup information (who's tough and how to beat them)
- ✅ BnB combos (organized by difficulty)
- ✅ Usage frequency (most-used moves)

---

## 🎮 How to Access the Guides

### Method 1: Interactive Web Interface (RECOMMENDED)

**File**: `output/character_guide.html`

**How to Use:**
1. Open `character_guide.html` in any web browser
2. Select character from dropdown menu
3. Browse all sections in one page:
   - Character Overview
   - Top 3 Strategies
   - Most Used Moves
   - Basic Moves (sorted tables)
   - Special Moves
   - BnB Combos
   - Matchup Guide

**Features:**
- Beautiful, color-coded interface
- Sortable move tables (by speed, safety, recovery, damage)
- Combo cards with difficulty ratings
- Strategy execution guides
- Matchup counter-strategies

---

### Method 2: Markdown Guide (For Reading/Printing)

**File**: `output/Blitzcrank_COMPLETE_GUIDE.md`

**Generate:**
```bash
python generate_character_page.py Blitzcrank
```

**Features:**
- Complete text guide (80+ pages)
- All sections included
- Easy to read in any text editor
- Can be converted to PDF for printing

---

### Method 3: Character Comparison Database

**File**: `output/character_database.html`

**Generate:**
```bash
python generate_database.py
```

**Features:**
- Compare ALL characters side-by-side
- Rankings (fastest moves, safest moves)
- Multi-tab interface
- Character grid view

---

## 📊 What Each Section Shows

### 1️⃣ Character Overview

**Answers:**
- How much health does this character have?
- What archetype are they? (Grappler, Rushdown, Zoner)
- How fast do they move?
- How good is their defense?
- What's their playstyle?

**Example (Blitzcrank):**
```
Health: 1050 HP
Archetype: Grappler
Dash Speed: Slow
Defense: Poor
Playstyle: Get close, then hit or grab
Strengths: Rocket Grab, Command Grab, Air Purifier +44
Weaknesses: Risky neutral, slow speed, bad defense
```

---

### 2️⃣ Top 3 Strategies

**Answers:**
- What are the best ways to win with this character?
- How do I execute each strategy?
- What moves do I need?
- How difficult is it?
- What's the success rate?

**Format for Each Strategy:**
```
Strategy Name: Zone Control
Difficulty: Easy
Success Rate: High in neutral game
Description: Use Rocket Grab from mid-range to control space

Key Moves: 5S1 (Rocket Grab), 2S1 (Air Purifier)

How to Execute:
1. Stay at mid-range
2. Throw out Rocket Grab repeatedly
3. If opponent jumps, use Air Purifier
4. Once it hits, dash forward and combo
5. Force them to come to you
```

**Blitzcrank's 3 Strategies:**
1. **Zone Control** - Use Rocket Grab to force approach (Easy)
2. **Anti-Air Dominance** - Dominate air with +44 Air Purifier (Medium)
3. **50-50 Mix-up** - Command grab vs attack guessing game (Hard)

---

### 3️⃣ Most Frequently Used Moves

**Answers:**
- What moves will I use most often?
- When should I use them?
- What's their purpose?

**Organized by Situation:**

**In Neutral Game (Mid-Long Range):**
```
5S1 (Rocket Grab)
- Frequency: Very High
- Purpose: Zone control, force approach
- When: Mid-long range, in neutral

2S1 (Air Purifier)
- Frequency: High
- Purpose: Anti-air, +44 frame advantage
- When: When opponent jumps

5L (Light Punch)
- Frequency: High
- Purpose: Quick poke, combo starter
- When: Close range, after plus frames
```

**In Pressure Game (Close Range):**
```
2S2 (Command Grab) - Medium-High frequency
2L (Low Poke) - Medium frequency
Assist Call - Very High frequency
```

**Variety/Mix-up Options:**
```
j.M (Jump Medium) - Medium
Throw - Medium
5M > 5H frame trap - Low-Medium
```

---

### 4️⃣ Basic Moves (START HERE!)

**Answers:**
- How fast is each move (startup)?
- How long is the recovery?
- Is it safe on block?
- How much damage?
- What's the range?
- Does it need assist?

**Organized by Type:**
1. **Standing Normals** (5L, 5M, 5H)
2. **Crouching Normals** (2L, 2M, 2H)
3. **Jumping Normals** (j.L, j.M, j.H)

**Table Format:**
```
Move | Startup | Recovery | On Block | Damage | Safety  | Range | Properties
-----|---------|----------|----------|--------|---------|-------|------------
5L   | 8f      | 12f      | -2f      | 45     | NEUTRAL | Close | Pressure
2S1  | 23f     | 119f     | +44f     | 1      | SAFE    | Mid   | Anti-Air
```

**Color Coding:**
- 🟢 Green = SAFE (positive frames)
- 🟡 Yellow = NEUTRAL (±2 frames)
- 🔴 Red = UNSAFE (-5 or worse)

**Sortable by:**
- Startup (fastest first)
- Safety (safest first)
- Recovery (quickest first)
- Damage (highest first)

---

### 5️⃣ Special Moves

**Answers:**
- What are the special moves?
- How do they work?
- When should I use them?
- Are they safe?
- Do they need assist?

**Detailed Breakdown for Each:**

**Example: 2S1 (Air Purifier)**
```
Frame Data:
- Startup: 23f
- Recovery: 119f
- On Block: +44f
- Damage: 1

Properties:
- Range: Mid
- Risk Level: LOW
- Safe on Block: YES (very!)
- Requires Assist: NO
- Anti-Air: YES
- Pressure Tool: YES

Usage:
Best anti-air in the game. Despite 119f recovery, the +44 
frame advantage makes it extremely safe. Use liberally against 
jumpers. Even on block, you get massive advantage to start 
your mixup.
```

---

### 6️⃣ BnB Combos (Bread and Butter)

**Answers:**
- What combos should I learn?
- In what order should I learn them?
- How much damage do they do?
- How many hits?
- How hard are they?
- When should I use them?

**Organized by Difficulty:**
```
⭐ (Difficulty 1)
⭐⭐ (Difficulty 2)
⭐⭐⭐ (Difficulty 3)
⭐⭐⭐⭐ (Difficulty 4)
⭐⭐⭐⭐⭐ (Difficulty 5)
```

**Format for Each Combo:**
```
Basic BnB (⭐ Difficulty 1/5)

Notation: 5L > 5L > 5S1
Plain English: Jab, jab, Rocket Grab

Stats:
- Hits: 3
- Damage: ~150
- Meter: No
- Starter: Light punch

When to Use: Close range, after plus frames
Notes: Most reliable combo. Easy execution. Always works.
```

**Learn in Order:**
1. Start with ⭐ combos (easiest)
2. Practice until consistent
3. Move to ⭐⭐ combos
4. Progress gradually
5. Save ⭐⭐⭐⭐ for advanced play

---

### 7️⃣ Matchup Guide

**Answers:**
- Who are the toughest opponents?
- Why are they difficult?
- How do I counter them?
- What moves should I use/avoid?

**Format for Each Matchup:**

**vs Zoners (Long-Range Characters) - HARD**
```
Why Difficult:
Can keep Blitzcrank out, avoid Rocket Grab, control space better

Counter-Strategy:
Patient approach, use Air Purifier liberally, don't chase

Key Points:
- Walk forward slowly (don't dash, too committal)
- Block projectiles and gain ground
- Use Air Purifier to stuff their pokes
- Once you land one Rocket Grab, they're in your range
- Use assist to cover your approach

Moves to Use:
- 2S1 (Air Purifier) frequently
- Careful forward movement
- Assists for coverage

Moves to Avoid:
- Random Rocket Grab from far (gets punished)
- Jumping predictably (easy anti-air for them)
```

**Blitzcrank's Tough Matchups:**
1. **vs Zoners** (Hard) - Keep you out, avoid your tools
2. **vs Rushdown** (Med-Hard) - Pressure your bad defense
3. **vs Good Backdash** (Medium) - Escape command grab

**Universal Tips:**
- Always have assist ready before command grab
- If they jump a lot, spam Air Purifier (+44!)
- In corner, they can't escape your mixup
- Never challenge when you're minus
- One Rocket Grab often leads to 50% health gone

---

## 🎯 Common Questions Answered

### "How long is the recovery on this move?"

**Look at:** Recovery column in move tables

**Example:**
```
5L: 12f recovery (fast!)
2S1: 119f recovery (slow, but +44 makes it safe)
5S1: Unknown (projectile)
```

---

### "Is this move safe on block?"

**Look at:** On Block column + Safety rating

**Understanding Frame Advantage:**
- **+44** (like 2S1) = SUPER SAFE! You recover 44 frames before opponent
- **-2** (like 5L) = NEUTRAL, slightly unsafe but usually OK
- **-15** = VERY UNSAFE, opponent can punish with full combo

**Rule of Thumb:**
- Positive (+) = SAFE
- 0 to -4 = NEUTRAL (usually OK)
- -5 or worse = UNSAFE (can be punished)

---

### "Is it good for closing distance (gap closer)?"

**Look at:** Properties column for "Gap Closer" tag

**Blitzcrank's Gap Closers:**
- ✅ 5S1 (Rocket Grab) - Pulls them to you!
- ❌ Normal attacks - No (use jump-ins or dash instead)

---

### "What are the top 3 strategies for winning?"

**Look at:** Top 3 Strategies section

**Blitzcrank:**
1. **Zone Control** - Spam Rocket Grab from mid-range
2. **Anti-Air Dominance** - Abuse +44 Air Purifier
3. **50-50 Mix-up** - Command grab or attack guessing game

---

### "What moves do I use most often?"

**Look at:** Most Frequently Used Moves section

**Blitzcrank (Neutral):**
- 5S1 (Very High) - Rocket Grab spam
- 2S1 (High) - Anti-air
- 5L (High) - Quick poke

**Blitzcrank (Pressure):**
- Assist Call (Very High) - Make mixups safe
- 2S2 (Medium-High) - Command grab win condition
- 2L (Medium) - Low mixup

---

### "Who are the toughest matchups?"

**Look at:** Matchup Guide section

**Blitzcrank's Hardest:**
1. **Zoners** (Hard) - Counter: Patient approach, Air Purifier
2. **Rushdown** (Med-Hard) - Counter: Keep them out, reset neutral
3. **Good Backdash** (Medium) - Counter: Corner them, use assists

---

## 💡 Learning Path

### Beginner (Week 1):
1. Read Character Overview
2. Learn Top 3 Strategies (start with Strategy 1)
3. Study Basic Moves section
4. Practice ⭐ combos only
5. Focus on most-used moves (5S1, 2S1, 5L)

### Intermediate (Week 2-3):
1. Master all basic normals
2. Learn special move properties
3. Practice ⭐⭐ and ⭐⭐⭐ combos
4. Study matchup guide (start with tough ones)
5. Implement Strategy 2 and 3

### Advanced (Week 4+):
1. Master ⭐⭐⭐⭐ combos
2. Study frame data deeply
3. Practice matchup-specific counters
4. Mix all 3 strategies
5. Learn advanced pressure sequences

---

## 🛠️ Technical Reference

### FGC Notation Used:
- **5L/M/H** - Standing Light/Medium/Heavy (no direction)
- **2L/M/H** - Crouching Light/Medium/Heavy (hold down)
- **j.L/M/H** - Jumping Light/Medium/Heavy
- **5S1/2S1** - Special moves
- **>** - Cancel into (5L > 5M = cancel light into medium)

### Frame Data Terms:
- **Startup** - How fast move comes out
- **Recovery** - How long until you can act again
- **On Block** - Frame advantage/disadvantage when blocked
  - Positive (+) = You recover first (safe!)
  - Negative (-) = Opponent recovers first (unsafe!)
- **Active** - How long the hitbox is out

### Safety Terms:
- **SAFE** - Can't be punished (positive frames)
- **NEUTRAL** - Barely safe (±2 frames)
- **UNSAFE** - Can be punished (-5 or worse)

### Risk Levels:
- **LOW** - Use freely, hard to punish
- **MEDIUM** - Use with caution
- **HIGH** - Only use with assist or setup

---

## 🎨 Web Interface Features

### Character Guide Interface:
- Dropdown character selector
- Color-coded safety indicators
- Sortable move tables
- Difficulty-rated combo cards
- Matchup counter-strategies
- Strategy execution guides

### Sorting Options:
- **By Startup** - See fastest moves first
- **By Safety** - See safest moves first
- **By Recovery** - See quickest recovery
- **By Damage** - See highest damage

### Visual Indicators:
- 🟢 Green borders = Safe moves
- 🔴 Red borders = Unsafe moves
- 🟡 Yellow badges = Medium difficulty
- 🟢 Green badges = Low risk
- 🔴 Red badges = High risk

---

## 📝 Summary

**You now have:**
- ✅ Complete character overview
- ✅ Top 3 winning strategies
- ✅ Most frequently used moves
- ✅ Basic moves organized and sortable
- ✅ Special moves with full details
- ✅ BnB combos sorted by difficulty
- ✅ Matchup guides with counters
- ✅ Multiple interfaces (Web + Markdown)

**Start Here:**
1. Open `output/character_guide.html`
2. Select "Blitzcrank"
3. Read Top 3 Strategies
4. Study Most Used Moves
5. Learn Basic Moves (5L, 2S1, 5S1)
6. Practice ⭐ combos
7. Study matchup guide

**Key Files:**
- `character_guide.html` - Interactive web guide
- `Blitzcrank_COMPLETE_GUIDE.md` - Text guide
- `Blitzcrank_page_data.json` - JSON data
- `character_database.html` - Multi-character comparison

---

**Created**: 2026-01-17  
**Data Source**: https://wiki.play2xko.com  
**System Version**: 2.0
