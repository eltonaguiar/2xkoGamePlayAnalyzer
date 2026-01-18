# Cheat Sheet Updates - Beginner Friendly Edition

## ✅ What Was Improved

The cheat sheets have been updated to be much more accessible for people less technical in the fighting game community. Here's what changed:

---

## 🎯 Major Improvements

### 1. **Clear English Explanations for Every Move**

**Before**: `2S1 - Air Purifier`  
**Now**: 
```
2S1 - Air Purifier (Down + Special 1)
**In Plain English**: Shoot your fist diagonally up to grab jumpers
**How to Do It**: Hold Down + press Special 1 button
```

Every move now includes:
- ✅ English name explanation
- ✅ Plain language description of what it does
- ✅ How to actually perform it (not just notation)
- ✅ When and why to use it

---

### 2. **Beginner-Friendly Notation Guide**

Added a complete "How to Read This Guide" section at the start of MOVE_CHEAT_SHEET.md:

```
## 📖 How to Read This Guide (For Beginners)

### Understanding Move Notation

Fighting games use **numpad notation** for directions:

7  8  9     [Back-Up]  [Up]      [Forward-Up]
4  5  6     [Back]     [Neutral] [Forward]
1  2  3     [Back-Down][Down]    [Forward-Down]

### Examples:
- 5L = Standing Light Punch (just press Light while standing)
- 2M = Crouching Medium Kick (hold Down + press Medium)
- j.H = Jumping Heavy Attack (press Heavy while in the air)
- 5S1 = Standing Special 1 (Blitzcrank's Rocket Grab)
```

**Key Features**:
- Visual numpad diagram
- Clear direction mappings
- Real examples from Blitzcrank's moveset
- Frame data explained simply

---

### 3. **Move Categories Explained**

Each category now has a header explaining what it means:

**Standing Normals**:
```
**What are "Standing Normals"?** 
These are your basic attacks while standing still or moving. 
Think of them as your jab, punch, and heavy punch.
```

**Special Moves**:
```
**What are "Special Moves"?** 
These are Blitzcrank's unique signature moves that define his character. 
They're usually stronger than normal attacks and have special properties.
```

**Universal Moves**:
```
**What are "Universal Moves"?** 
These work the same for every character in the game. Everyone has these!
```

---

### 4. **Detailed Move Breakdowns**

Each move now has comprehensive beginner-friendly information:

#### Example: 5L - Standing Light Punch

**Before**:
```
- Input: 5L (Neutral Light)
- Damage: 45
- Startup: 8 frames
- Recovery: 12 frames
- On Block: -2 frames
```

**After**:
```
#### 5L - Standing Light Punch
**In Plain English**: Your quick standing jab

- **How to Do It**: Just press Light button while standing
- **Input Notation**: 5L (5 = standing, L = Light)
- **Damage**: 45
- **Speed**: 8 frames startup (fairly quick)
- **Active**: 5 frames (how long it can hit)
- **Recovery**: 12 frames (how long you're stuck after)
- **On Block**: -2 frames ⚠️ (slightly unsafe - opponent recovers 2 frames before you)
- **What Can Block It**: Everything (Low blocks, High blocks, Air blocks all work)
- **When to Use**: 
  - Quick poke to check opponent
  - Start combos
  - After landing Rocket Grab or Air Purifier
```

---

### 5. **Command Grab Deep Explanation**

Added extensive beginner-friendly explanation for 2S2 (Command Grab):

```
#### 2S2 - Garbage Collection 🔒 COMMAND GRAB
**In Plain English**: Blitzcrank grabs the opponent - they CANNOT block this!

**What It Does**: Unlike normal attacks, **blocking does NOT stop this!** 
They must jump or backdash away to avoid it.

**⚠️ WARNING - HIGH RISK MOVE**: 
- If you miss this (they jump or backdash), you're VERY punishable
- **DO NOT SPAM THIS!** Experienced players will jump and punish you hard

**When to Use** (ONLY these situations):
- ✅ After calling your assist - Assist protects you if you miss
- ✅ When opponent whiffs a big slow move - They're stuck recovering, free grab!
- ✅ After conditioning - You've made them scared to press buttons
- ❌ NEVER raw - Don't just throw it out randomly!

**This is Your Win Condition**: 
Once you're close, opponent must guess: Block (loses to this grab) or 
Jump (loses to your attacks). This "guess" situation is how Blitzcrank wins.
```

---

### 6. **Updated QUICK_REFERENCE.md**

Added beginner guide at the top:

```
## 📖 Reading This Guide (Beginner Friendly!)

**What do the numbers and letters mean?**
- 5 = Standing (not moving)
- 2 = Crouching (holding down)
- j. = Jumping (in the air)
- L/M/H = Light/Medium/Heavy attack buttons
- S1/S2 = Special move buttons

**Example**: 2S1 means "Hold Down + press Special 1"
```

All moves now show both notation AND plain English:

```
### 2S1 - Air Purifier (Down + Special 1) ✅
**In English**: Shoot your fist diagonally up to grab jumpers  
**How to do it**: Hold Down, press Special 1
```

---

### 7. **Frame Advantage Explained**

Added simple explanation of frame advantage:

```
**What is frame advantage?** When both players do a move, who recovers first?
- **Positive (+)** = You recover first = GOOD! You can attack again
- **Negative (-)** = They recover first = BAD! They can hit you
- **Example**: +44 means you recover 44 frames before them = SUPER SAFE!
```

---

### 8. **Punish Guide with Context**

Added context to punish situations:

**Before**: `Opponent Whiffs Big Move`  
**After**: 
```
### Opponent Whiffs Big Move (Misses a slow attack)
**What does "punish" mean?** When opponent makes a mistake, you hit them for it!
```

---

### 9. **PRINTABLE_CHEAT_SHEET.txt Updated**

Added notation guide and English translations:

```
NOTATION GUIDE: Think of a keyboard numpad for directions!
  5 = Standing | 2 = Crouching | j. = Jumping
  Example: 2S1 = Hold Down + press Special 1

2S1 (Air Purifier)
  English: Shoot fist up at jumpers
  How: Hold Down + Special 1

2S2 (Garbage Collection)
  English: Grab - can't be blocked!
  How: Hold Down + Special 2
```

---

## 📋 Files Updated

1. ✅ **MOVE_CHEAT_SHEET.md** - Complete beginner guide added
2. ✅ **QUICK_REFERENCE.md** - Plain English for all moves
3. ✅ **PRINTABLE_CHEAT_SHEET.txt** - Added notation guide and English
4. ✅ **character_data.py** - Enhanced with usage notes (unchanged, already good)
5. ✅ **generate_cheat_sheet.py** - Regenerated outputs

---

## 🎯 Key Changes Summary

| Feature | Before | After |
|---------|--------|-------|
| Move names | Notation only (5L, 2S1) | Notation + English (5L - Standing Light Punch) |
| Instructions | None | "How to Do It" for each move |
| Notation guide | Basic | Detailed with numpad diagram |
| Frame data | Technical terms | Explained in plain language |
| Categories | Just headers | Explained what each category means |
| Command grab | Brief | Extensive beginner warnings & tips |
| Examples | Few | Many throughout |

---

## 🎮 Example Improvements

### Move Name: 2L

**Before (technical)**:
```
2L - Crouching Light
- Input: 2L (Down Light)
- Description: Fast low poke
```

**After (beginner-friendly)**:
```
#### 2L - Crouching Light Kick
**In Plain English**: Your quick low poke while crouching

- **How to Do It**: Hold Down + press Light button
- **Input Notation**: 2L (2 = down/crouching, L = Light)
- **What It Does**: Fast low attack, probably hits opponent's feet/legs
- **When to Use**: Quick low pressure, forces opponent to block low
```

---

### Move Name: 5S1

**Before (technical)**:
```
5S1 - Rocket Grab
- Input: 5S1 (Neutral Special 1)
- Description: Iconic projectile grab that pulls opponent close
```

**After (beginner-friendly)**:
```
#### 5S1 - Rocket Grab ⭐
**In Plain English**: Blitzcrank shoots his fist forward like a rocket to grab opponents from far away

- **How to Do It**: Press Special 1 button while standing
- **Input Notation**: 5S1 (5 = standing, S1 = Special move 1)
- **What It Does**: Blitzcrank's iconic move! He shoots his fist like a rocket projectile. 
  If it hits, it pulls the opponent right up to you.
- **When to Use**: 
  - **THIS IS YOUR MAIN MOVE** - Use it a lot!
  - Stand at mid-long range and throw it out
  - Forces opponent to come close to you (where you're strongest)
```

---

## ✅ Result

Now anyone can pick up these cheat sheets and understand:
- ✅ What each move is called in plain English
- ✅ How to actually perform the move
- ✅ What the move does visually
- ✅ When and why to use it
- ✅ How to read the notation system
- ✅ What frame advantage means
- ✅ Why certain moves are risky

**No prior fighting game knowledge required!**

---

## 🚀 Quick Start for Beginners

1. **Start Here**: Read the "How to Read This Guide" section in MOVE_CHEAT_SHEET.md
2. **Learn Notation**: Understand what 5, 2, j., L, M, H, S1, S2 mean
3. **Practice 3 Moves**: 
   - 5S1 (Rocket Grab) - Your main zoning tool
   - 2S1 (Air Purifier) - Your safest anti-air
   - 2S2 (Command Grab) - Your win condition (use carefully!)
4. **Keep Reference Nearby**: Use QUICK_REFERENCE.md during matches

---

**Data Source**: https://wiki.play2xko.com

**Last Updated**: 2026-01-17
