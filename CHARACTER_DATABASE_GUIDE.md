# Character Database & Comparison System

## 🎯 Overview

The 2XKO Character Database is a comprehensive system for comparing characters, moves, frame data, and combos across all characters. It provides:

- **Character Stats Comparison** (Health, Archetype, Playstyle)
- **Move Database** with sortable/filterable tables
- **BnB Combo Library** with damage estimates
- **Fastest Moves Rankings** (by startup frames)
- **Safest Moves Rankings** (by frame advantage)
- **Move Efficiency Rankings** (speed + safety + damage formula)
- **Assist-Dependent Moves** identification

---

## 📁 Files Created

### Core System Files:

1. **character_comparison.py** (10 KB)
   - Python module for comparing characters
   - Methods for fastest/safest/most efficient moves
   - Combo comparison across characters
   - JSON export functionality

2. **generate_database.py** (4 KB)
   - Script to generate complete JSON database
   - Includes statistics and comparisons
   - Run this after updating character data

3. **output/character_database.html** (17 KB)
   - Interactive web interface
   - Browse all characters, moves, and combos
   - Sort and filter functionality
   - Responsive design

4. **output/character_database.json** (Generated)
   - Complete character data in JSON format
   - Used by HTML interface
   - Includes all moves, combos, and comparisons

---

## 🎮 How to Use

### Generating the Database:

```bash
python generate_database.py
```

This creates `output/character_database.json` with all character data.

### Opening the Interface:

1. Navigate to: `output/character_database.html`
2. Open in any modern web browser
3. The interface will load data from `character_database.json`

---

## 📊 Interface Features

### 1. **Character Overview Tab**

**What it shows:**
- All characters in grid layout
- Health, Archetype, Playstyle for each
- Sortable by Name/Health/Archetype

**Use it for:**
- Quick character stats lookup
- Comparing health pools
- Finding characters by archetype

---

### 2. **Move Comparison Tab**

**What it shows:**
- Complete move database for all characters
- Sortable by: Startup Speed, Safety, Damage, Recovery
- Filterable by: All/Safe/Unsafe/Requires Assist

**Columns:**
- **Character**: Which character has this move
- **Move**: Notation (5L, 2S1, etc.)
- **Name**: English name (Light Punch, Air Purifier, etc.)
- **Startup**: Frames until move hits (lower = faster)
- **Recovery**: Frames stuck after move (lower = better)
- **On Block**: Frame advantage when blocked
  - **Green +**: Safe (you recover first)
  - **Yellow ±0**: Neutral
  - **Red -**: Unsafe (they recover first)
- **Damage**: Raw damage value
- **Risk**: LOW/MEDIUM/HIGH
- **Notes**: Badges for "Needs Assist" etc.

**Sort Options:**
- **Startup Speed**: Fastest moves first
- **Safety**: Safest moves first (+44, +10, etc.)
- **Damage**: Highest damage first
- **Recovery Time**: Quickest recovery first

**Example Use Cases:**
- Find fastest move in the game: Sort by Startup
- Find safest moves: Sort by Safety
- Find high-risk moves: Filter "Unsafe"
- Find moves needing assists: Filter "Requires Assist"

---

### 3. **BnB Combos Tab**

**What it shows:**
- All Bread and Butter combos for selected character
- Combo notation, damage, difficulty, hit count
- Filterable by difficulty level

**Information per Combo:**
- **Name**: Combo name (Light Chain, Jump-In, etc.)
- **Notation**: FGC notation (5L > 5L > 5S1)
- **Hits**: Number of hits in combo
- **Damage**: Low/Medium/High/Maximum
- **Difficulty**: ⭐ to ⭐⭐⭐⭐
- **Meter Use**: Does it require meter?
- **Situation**: When to use it

**Example:**
```
Combo: Jump-In Combo
Notation: j.M > 5L > 5M > 5H > 5S1
Hits: 5
Damage: Medium
Difficulty: ⭐⭐ (Easy)
Situation: After landing jump-in attack
```

---

### 4. **Fastest Moves Tab**

**What it shows:**
- Fastest move for each character
- Ranked by startup frames (lowest first)

**Why it matters:**
- Shows who has fastest buttons
- Important for frame traps and counter-pokes
- Fastest moves usually win in close situations

**FGC Terms:**
- **Startup Frames**: Time before move becomes active
- **Frame Trap**: Using fast move to catch opponent pressing buttons
- **Counter-Poke**: Fast move to beat opponent's attack

---

### 5. **Safest Moves Tab**

**What it shows:**
- Safest move for each character
- Ranked by frame advantage on block (highest first)

**Why it matters:**
- Shows most oppressive pressure tools
- Positive frames = Your turn to attack again
- Blitzcrank's 2S1 at +44 is extremely safe!

**FGC Terms:**
- **Plus on Block (+)**: You recover before opponent (safe!)
- **Minus on Block (-)**: Opponent recovers first (unsafe!)
- **Frame Advantage**: Who gets to move first after block

**Safety Categories:**
- **+10 or more**: HUGE advantage - free mixup
- **+1 to +9**: Safe - your turn
- **0 to -2**: Slightly unsafe
- **-3 to -5**: Unsafe - can be punished
- **-6 or worse**: VERY UNSAFE - full punish

---

### 6. **Move Efficiency Tab**

**What it shows:**
- Moves ranked by efficiency score
- Formula: Speed + Safety + Damage

**How Efficiency is Calculated:**
```
Efficiency Score = Startup Score + Safety Score + Damage Score

Where:
- Startup Score = max(0, 30 - startup_frames)
  (Faster = Better)
  
- Safety Score = on_block + 10
  (More plus = Better)
  
- Damage Score = damage / 10
  (Higher damage = Better)
```

**Example:**
```
Blitzcrank 5L:
- Startup: 8f  → Score: 22 (30-8)
- On Block: -2 → Score: 8  (-2+10)
- Damage: 45   → Score: 4.5 (45/10)
- Total Efficiency: 34.5
```

**Use it for:**
- Finding "best bang for buck" moves
- Moves that are fast, safe, AND damaging
- Optimal move selection

---

## 🔍 FGC Terminology Explained

### Frame Data Terms:

**Startup**: Frames until move hits
- 8f = Fast (jabs, light attacks)
- 15f = Medium (medium attacks)
- 23f+ = Slow (heavy attacks, specials)

**Active**: Frames move can hit
- More active frames = easier to hit with
- Covers more space/time

**Recovery**: Frames stuck after move
- Lower = Better
- Can't do anything during recovery

**On Block**: Frame advantage when blocked
- **+44**: You recover 44 frames BEFORE them
- **+5**: You recover 5 frames before them
- **0**: Both recover at same time
- **-2**: They recover 2 frames before you
- **-15**: They recover 15 frames before you (very bad!)

### Move Types:

**Normal**: Basic attacks (5L, 2M, j.H, etc.)
**Special**: Unique character moves (5S1, 2S2, etc.)
**Command Grab**: Unblockable grab (must jump/backdash)
**Overhead**: Must block standing
**Low**: Must block crouching

### Safety Terms:

**Safe**: Can't be punished on block
**Unsafe**: Can be punished on block
**Plus on Block**: You move first (good!)
**Minus on Block**: They move first (bad!)

### Combo Terms:

**BnB (Bread and Butter)**: Reliable go-to combos
**Hit Confirm**: Making sure move hits before continuing
**Cancel**: Interrupting move recovery with another move
**Meter**: Resource used for supers/enhanced moves
**Restand**: Keeps opponent standing for pressure

---

## 📈 Rankings Explained

### Fastest Moves (Startup Frames)

**What it means:**
- Lower startup = Faster move
- Fastest moves win close trades
- Important for frame traps

**Rankings:**
1. **5-8f**: Lightning fast (jabs)
2. **9-12f**: Fast (light attacks)
3. **13-20f**: Medium speed
4. **21-30f**: Slow (heavies)
5. **30f+**: Very slow (big specials)

**Example:**
```
Blitzcrank 5L: 8f (Fast jab)
Blitzcrank 2S1: 23f (Slow but +44!)
```

---

### Safest Moves (Frame Advantage)

**What it means:**
- Higher on block = Safer
- Positive (+) = You attack first
- Negative (-) = They attack first

**Rankings:**
1. **+20 or more**: Extremely safe
2. **+10 to +19**: Very safe
3. **+1 to +9**: Safe
4. **0**: Neutral
5. **-1 to -5**: Slightly unsafe
6. **-6 or worse**: Very unsafe

**Example:**
```
Blitzcrank 2S1: +44 (SUPER SAFE!)
Blitzcrank 5L: -2 (Slightly unsafe)
Blocked 5S2: -15 (VERY UNSAFE!)
```

---

### Assist-Dependent Moves

**What it means:**
- Moves too risky to use alone
- Need assist to cover if opponent avoids
- Usually high reward but high risk

**When Move Needs Assist:**
- Command grabs (they can jump)
- Slow, punishable specials
- Risky mix-up moves
- Anything with "requires_assist: true"

**Example:**
```
Blitzcrank 2S2 (Command Grab):
- CANNOT BE BLOCKED
- But can be jumped
- Use WITH assist to cover the jump
- If they jump: Assist hits them
- If they block: Grab hits them
= They have to guess!
```

---

### Move Efficiency Rankings

**What it means:**
- Best overall value moves
- Considers speed + safety + damage together
- Higher score = Better move

**High Efficiency Moves:**
- Fast startup (quick)
- Plus on block (safe)
- Good damage (rewarding)

**Low Efficiency Moves:**
- Slow startup (telegraphed)
- Minus on block (punishable)
- Low damage (not worth it)

---

## 💾 Data Structure

### Character Entry Example:

```json
{
  "name": "Blitzcrank",
  "health": 1050,
  "archetype": "Grappler",
  "moves": [
    {
      "move": "5L",
      "name": "Light Punch",
      "startup": 8,
      "recovery": 12,
      "on_block": -2,
      "damage": 45,
      "is_safe": false,
      "requires_assist": false,
      "risk_level": "low"
    },
    {
      "move": "2S1",
      "name": "Air Purifier",
      "startup": 23,
      "recovery": 119,
      "on_block": 44,
      "damage": 1,
      "is_safe": true,
      "requires_assist": false,
      "risk_level": "low"
    }
  ],
  "bnb_combos": [
    {
      "name": "Light Chain",
      "notation": "5L > 5L > 5S1",
      "hits": 3,
      "damage": "Low",
      "difficulty": 1
    }
  ]
}
```

---

## 🔧 Adding New Characters

### Step 1: Add Character Data

Edit `character_data.py`:

```python
class NewCharacterData:
    @staticmethod
    def get_character_info() -> Dict:
        return {
            "name": "NewCharacter",
            "archetype": "Rushdown",
            "health": 1000,
            # ... etc
        }
    
    @staticmethod
    def get_moves() -> Dict[str, MoveData]:
        moves = {}
        moves["5L"] = MoveData(...)
        # ... add all moves
        return moves
    
    @staticmethod
    def get_bnb_combos() -> Dict[str, Dict]:
        return {
            "combo_1": {...},
            # ... add combos
        }

# Register character
CHARACTER_DATA["NewCharacter"] = NewCharacterData
```

### Step 2: Regenerate Database

```bash
python generate_database.py
```

### Step 3: Refresh Browser

The HTML interface will automatically load the new character!

---

## 📚 Use Cases

### For Players:

1. **Learning a new character**
   - Check fastest move for poking
   - Find safest moves for pressure
   - Learn BnB combos by difficulty

2. **Matchup preparation**
   - Compare your character vs opponent
   - Find their fastest punish options
   - Learn which moves they need assist for

3. **Optimization**
   - Find most efficient moves
   - Identify unsafe moves to punish
   - Build better combos

### For Analysts:

1. **Character balance**
   - Compare health across characters
   - Find outlier moves (too fast/safe)
   - Identify assist dependencies

2. **Meta analysis**
   - Track which moves are used most
   - Correlate with combo tracking data
   - Find underutilized efficient moves

---

## 🎯 Quick Reference

### Opening the Database:
```
1. Run: python generate_database.py
2. Open: output/character_database.html
3. Browse and compare!
```

### Finding Specific Info:
- **Fastest move?** → Fastest Moves tab
- **Safest move?** → Safest Moves tab
- **Best overall move?** → Efficiency tab
- **Easy combos?** → BnB Combos → Filter: Beginner
- **Moves needing assist?** → Moves tab → Filter: Requires Assist

### Understanding Frame Data:
- **8f startup** = Fast jab
- **+44 on block** = SUPER SAFE!
- **-15 on block** = VERY UNSAFE!
- **Requires Assist** = High risk without help

---

**Data Source**: https://wiki.play2xko.com  
**Last Updated**: 2026-01-17
