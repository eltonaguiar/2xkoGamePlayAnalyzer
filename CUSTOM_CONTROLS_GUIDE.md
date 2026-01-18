# Custom Control Mapping System - Complete Guide

## 🎮 Overview

This system allows you to customize your keyboard controls and automatically see **all moves, combos, and strategies** displayed with **YOUR custom keyboard mappings**.

---

## 📁 Files Created

### 1. **control_mapper.py** (Python Module)
Backend system for control mapping:
- Convert FGC notation to keyboard instructions
- Support multiple control schemes (presets)
- Generate custom move lists
- Save/load custom configurations

### 2. **output/custom_controls.html** (Interactive Web Interface) ⭐
**MAIN INTERFACE** - Beautiful, interactive control mapper:
- Visual control editor with input boxes
- 4 built-in presets (Default, WASD+UIOP, Arrow Keys, Hitbox)
- Real-time move list updates as you change controls
- Shows all moves with YOUR custom keys
- Save controls to browser
- Export controls to JSON

### 3. **output/Blitzcrank_custom_controls.md** (Generated Move List)
Complete move list with custom controls in Markdown format

---

## 🎯 Features

### ✅ Full 2XKO Control Mapping

**Movement (4 keys):**
- Up/Jump
- Down/Crouch
- Left/Back
- Right/Forward

**Attacks (4 keys):**
- Light
- Medium
- Heavy
- Special

**Actions (4 keys):**
- Grab/Throw
- Parry
- Break
- Tag/Assist

**Total: 12 customizable controls**

---

## 🖥️ How to Use

### Option 1: Interactive Web Interface (RECOMMENDED)

**File:** `output/custom_controls.html`

**Steps:**
1. Open `custom_controls.html` in any web browser
2. Choose a preset OR customize each key manually
3. See ALL moves update in real-time with your custom controls!
4. Click "💾 Save" to save to browser storage
5. Click "📄 Export" to download JSON config file

**Features:**
- ✅ 4 built-in presets
- ✅ Real-time preview
- ✅ Visual keyboard layout display
- ✅ All moves shown with YOUR keys
- ✅ Combo sequences converted
- ✅ Save/load functionality

---

### Option 2: Python Command Line

**Generate move list with default controls:**
```bash
python control_mapper.py
```
Output: `output/Blitzcrank_custom_controls.md`

**Generate move lists for ALL presets:**
```bash
python control_mapper.py --all
```
Generates:
- `Blitzcrank_controls_default.md`
- `Blitzcrank_controls_wasd_uiop.md`
- `Blitzcrank_controls_arrows.md`
- `Blitzcrank_controls_hitbox.md`

---

## 📋 Built-in Presets

### 1. Default 2XKO (Standard)
```
Movement: WASD
Attacks: JKLM
Actions: I, U, O, T

W = Jump        J = Light
S = Crouch      K = Medium
A = Back        L = Heavy
D = Forward     M = Special
                I = Grab
                U = Parry
                O = Break
                T = Tag
```

### 2. WASD + UIOP
```
Movement: WASD
Attacks: UIOP
Actions: [, ], \, Enter

W = Jump        U = Light
S = Crouch      I = Medium
A = Back        O = Heavy
D = Forward     P = Special
```

### 3. Arrow Keys
```
Movement: Arrow Keys
Attacks: ZXCV
Actions: ASDF

↑ = Jump        Z = Light
↓ = Crouch      X = Medium
← = Back        C = Heavy
→ = Forward     V = Special
```

### 4. Hitbox Style (FGC Standard)
```
Movement: Space + DVF
Attacks: UIOP
Actions: JKL;

Space = Jump    U = Light
V = Crouch      I = Medium
D = Back        O = Heavy
F = Forward     P = Special
```

---

## 🔄 How It Works

### Notation Translation System

**FGC Notation → Your Custom Keys**

**Direction Mapping (Numpad Notation):**
```
7  8  9       (Your Up+Left)  (Your Up)  (Your Up+Right)
4  5  6   =   (Your Left)     Neutral    (Your Right)
1  2  3       (Your Down+Left) (Your Down) (Your Down+Right)
```

**Button Mapping:**
```
L  = Your Light key
M  = Your Medium key
H  = Your Heavy key
S  = Your Special key
S1 = Your Special key
S2 = Your Special key
```

**Examples:**

| Notation | Default Keys | Arrow Keys Preset | Hitbox Preset |
|----------|--------------|-------------------|---------------|
| **5L** | Press J | Press Z | Press U |
| **2S1** | Hold S + Press M | Hold ↓ + Press V | Hold V + Press P |
| **j.H** | Press W, then Press L | Press ↑, then Press C | Press Space, then Press O |
| **6M** | Hold D + Press K | Hold → + Press X | Hold F + Press I |

---

## 💥 Combo Translation

**Combo notation is automatically converted to YOUR key sequences!**

**Example Combo:** `5L > 5M > 5S1`

**Default Controls:**
```
Press J > Press K > Press M
```

**Arrow Keys Preset:**
```
Press Z > Press X > Press V
```

**Hitbox Preset:**
```
Press U > Press I > Press P
```

**Complex Combo:** `2L > 2M > j.H > 5S1`

**Default Controls:**
```
Hold S+Press J → Hold S+Press K → Press W, then Press L → Press M
```

---

## 📊 What Gets Converted

### ✅ Basic Moves
Every normal attack with your custom keys:
```
5L (Standing Light) = Press [Your Light]
2M (Crouching Medium) = Hold [Your Down] + Press [Your Medium]
j.H (Jump Heavy) = Press [Your Up], then Press [Your Heavy]
```

### ✅ Special Moves
All special moves with your custom keys:
```
5S1 (Rocket Grab) = Press [Your Special]
2S1 (Air Purifier) = Hold [Your Down] + Press [Your Special]
2S2 (Command Grab) = Hold [Your Down] + Press [Your Special]
```

### ✅ BnB Combos
Complete combo sequences:
```
Light Chain = [Your Light] > [Your Light] > [Your Special]
Anti-Air Combo = Hold [Your Down]+Press [Your Special] > [Your Light] > [Your Heavy]
Jump Combo = Press [Your Up], then [Your Heavy] > [Your Light] > [Your Medium]
```

### ✅ Strategies
Strategic move instructions updated with your keys:
```
Strategy 1: Zone Control
- Throw out Rocket Grab (Press [Your Special]) repeatedly
- If opponent jumps, use Air Purifier (Hold [Your Down] + Press [Your Special])
```

---

## 💾 Save & Export

### Save to Browser
Click "💾 Save" in the web interface:
- Saves to browser localStorage
- Persists between sessions
- Auto-loads when you return

### Export to JSON
Click "📄 Export" to download:
```json
{
  "up": "W",
  "down": "S",
  "left": "A",
  "right": "D",
  "light": "J",
  "medium": "K",
  "heavy": "L",
  "special": "M",
  "grab": "I",
  "parry": "U",
  "break": "O",
  "tag": "T"
}
```

**Use exported JSON:**
- Share with friends
- Backup your config
- Import to other tools

---

## 🎨 Web Interface Features

### Visual Control Editor
- Input boxes for each control
- Click and type to customize
- Real-time validation
- Clear labels for each action

### Control Legend Display
Shows your current mapping visually:
```
🎮 Your Current Controls
┌─────────────────────────────┐
│ W        J        I         │
│ Up/Jump  Light    Grab      │
│                             │
│ S        K        U         │
│ Crouch   Medium   Parry     │
└─────────────────────────────┘
```

### Move Cards
Each move displayed as a card:
```
┌──────────────────────────────┐
│ Standing Light               │
│ Notation: 5L                 │
│ Your Keys: Press J           │
│ ────────────────────────     │
│ Quick jab, combo starter     │
└──────────────────────────────┘
```

### Combo Cards
Combos with difficulty ratings:
```
┌──────────────────────────────┐
│ Basic BnB Combo              │
│ ⭐ Difficulty 1/5            │
│                              │
│ Notation: 5L > 5L > 5S1      │
│ Your Keys:                   │
│ Press J → Press J → Press M  │
│                              │
│ Damage: ~150                 │
└──────────────────────────────┘
```

---

## 🔧 Advanced Usage

### Create Custom Preset (Python)
```python
from control_mapper import ControlScheme, ControlMapper

# Define your custom scheme
my_scheme = ControlScheme(
    name="My Custom Layout",
    up="Space", down="C", left="Z", right="X",
    light="Q", medium="W", heavy="E", special="R",
    grab="A", parry="S", break_action="D", tag="F"
)

# Create mapper
mapper = ControlMapper(my_scheme)

# Convert notation
print(mapper.notation_to_keys("5L"))  # Press Q
print(mapper.notation_to_keys("2S1"))  # Hold C + Press R
print(mapper.combo_to_keys("5L > 5M > 5S1"))  # Press Q > Press W > Press R

# Generate move list
from character_data import BlitzcrankData
content = generate_custom_move_list(BlitzcrankData, mapper)

# Save to file
with open("output/my_custom_controls.md", 'w') as f:
    f.write(content)
```

### Load Saved Scheme
```python
from control_mapper import ControlMapper

# Load from JSON
mapper = ControlMapper.load_scheme("my_controls.json")

# Use loaded scheme
print(mapper.notation_to_keys("5L"))
```

---

## 📖 Use Cases

### 1. **Learning with Your Actual Keys**
You remapped your controls to match your arcade stick:
- Open web interface
- Set your custom mapping
- See ALL moves with YOUR keys
- Print/save for reference while playing

### 2. **Testing Different Layouts**
Trying to find the best control scheme:
- Try each preset (Default, Arrow Keys, Hitbox)
- See how combos feel with each layout
- Compare which is most comfortable
- Export your favorite

### 3. **Sharing with Friends**
Your friend uses different controls:
- Generate move list with their controls
- Share the custom move list
- They can learn without confusion
- Everyone sees moves in their own layout

### 4. **Multi-Platform Gaming**
Different controls on different devices:
- PC controls (keyboard)
- Controller mapping
- Arcade stick layout
- Generate separate guides for each

---

## 🎯 Benefits

### ✅ No Mental Translation
**Before:** "5L means... what key is that again?"
**After:** "Press J" (exactly what you need to press!)

### ✅ Learn Faster
See moves in YOUR keyboard layout from day one
- No confusion
- No mistakes
- Faster muscle memory

### ✅ Portable
Works with ANY control setup:
- Keyboard layouts
- Remapped controls
- Custom bindings
- Accessibility setups

### ✅ Always Up-to-Date
Change your controls? Update instantly:
- All moves automatically converted
- All combos updated
- All strategies reflect new keys

---

## 🚀 Quick Start

### Fastest Way to Get Started:

1. **Open** `output/custom_controls.html`
2. **Select** a preset or customize
3. **See** all moves with your keys!
4. **Save** your configuration
5. **Play** with your custom guide!

### For Default 2XKO Controls:
Just open the web interface - it's already set to default!

### For Custom Setup:
1. Click on each input box
2. Type your key
3. Watch moves update in real-time
4. Click "💾 Save" when done

---

## 📝 Example Output

### Your Move List Header:
```
# Blitzcrank - Custom Control Move List
Control Scheme: [Your Scheme Name]

🎮 Your Custom Controls
Movement:
- Up/Jump: [Your Key]
- Down/Crouch: [Your Key]
- Left/Back: [Your Key]
- Right/Forward: [Your Key]

Attacks:
- Light: [Your Key]
- Medium: [Your Key]
- Heavy: [Your Key]
- Special: [Your Key]
```

### Example Move Entry:
```
### Air Purifier (Your Safest Move!)
- Notation: 2S1
- Your Keys: Hold [Your Down Key] + Press [Your Special Key]
- What it does: Anti-air special, +44 on block!
- When to use: When opponent jumps at you
```

### Example Combo Entry:
```
### Jump-in BnB Combo
- Notation: j.M > 5L > 5M > 5S1
- Your Keys: Press [Up], then [Medium] → Press [Light] → Press [Medium] → Press [Special]
- Difficulty: ⭐⭐
- Damage: ~200
- Situation: After successful jump-in
```

---

## 🎮 Complete Feature List

### Web Interface:
- ✅ Visual control editor (12 customizable inputs)
- ✅ 4 built-in presets
- ✅ Real-time move list updates
- ✅ Control legend display
- ✅ Move cards with custom keys
- ✅ Combo cards with key sequences
- ✅ Save to browser storage
- ✅ Export to JSON
- ✅ Responsive design (mobile-friendly)
- ✅ Beautiful gradient UI

### Python Module:
- ✅ Convert notation to keys (`notation_to_keys`)
- ✅ Convert combos to key sequences (`combo_to_keys`)
- ✅ Generate complete move lists
- ✅ Save/load control schemes
- ✅ Multiple character support
- ✅ Extensible preset system

### Generated Move Lists:
- ✅ Control legend
- ✅ All basic moves with custom keys
- ✅ All special moves with custom keys
- ✅ All combos with key sequences
- ✅ Markdown format (easy to read/print)
- ✅ JSON export for other tools

---

## 🏆 Summary

You now have a **complete custom control mapping system** that:

1. **Maps ANY keyboard layout** (12 customizable controls)
2. **Shows all moves with YOUR keys** (no mental translation)
3. **Converts all combos to YOUR sequences** (step-by-step)
4. **Updates in real-time** (as you customize)
5. **Works with multiple presets** (or create your own)
6. **Saves your configuration** (browser + JSON export)
7. **Beautiful web interface** (easy to use)
8. **Command-line tools** (for advanced users)

**Result:** You see every move, combo, and strategy explained with the EXACT keys YOU press on YOUR keyboard!

---

**Files to Use:**
- 🌟 **Main Interface:** `output/custom_controls.html`
- 📜 **Python Module:** `control_mapper.py`
- 📄 **Generated Lists:** `output/Blitzcrank_custom_controls.md`

**Start here:** Open `output/custom_controls.html` and customize your controls!
