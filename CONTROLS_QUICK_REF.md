# 🎮 Custom Controls System - Quick Reference

## What Is This?

A system that **automatically converts all moves and combos to YOUR custom keyboard layout**.

No more "What key is 5L again?" - Just see exactly what to press!

---

## 🚀 Quick Start (30 seconds)

1. Open: `output/custom_controls.html`
2. Choose a preset OR type your own keys
3. Done! All moves now show YOUR keys

---

## 📊 What You Can Customize

### 12 Controls Total:

**Movement (4):**
- Up/Jump
- Down/Crouch  
- Left/Back
- Right/Forward

**Attacks (4):**
- Light
- Medium
- Heavy
- Special

**Actions (4):**
- Grab
- Parry
- Break
- Tag

---

## 🎯 Built-in Presets

Click to instantly load:

### 1. Default 2XKO
```
WASD + JKLM + IUO
```

### 2. WASD + UIOP
```
WASD + UIOP + Brackets
```

### 3. Arrow Keys
```
↑↓←→ + ZXCV + ASDF
```

### 4. Hitbox Style
```
Space/DVF + UIOP + JKL;
```

---

## 💡 Example Conversions

### With Default Controls (WASD + JKLM):

| Notation | Your Keys |
|----------|-----------|
| 5L | Press J |
| 2S1 | Hold S + Press M |
| j.H | Press W, then Press L |
| 5L > 5M > 5S1 | Press J → Press K → Press M |

### With Arrow Keys Preset:

| Notation | Your Keys |
|----------|-----------|
| 5L | Press Z |
| 2S1 | Hold ↓ + Press V |
| j.H | Press ↑, then Press C |
| 5L > 5M > 5S1 | Press Z → Press X → Press V |

---

## 🔥 What Gets Converted

✅ **All Basic Moves** (5L, 2M, j.H, etc.)
✅ **All Special Moves** (5S1, 2S1, 2S2, etc.)  
✅ **All BnB Combos** (full sequences)
✅ **All Strategy Instructions**

**Result:** Every single move explained with YOUR exact keys!

---

## 💾 Features

- ✅ Real-time preview as you type
- ✅ Save to browser (auto-load next time)
- ✅ Export to JSON file
- ✅ Visual control legend
- ✅ Combo sequences converted
- ✅ Works on any device

---

## 📁 Files

### Main Interface (Use This!)
**`output/custom_controls.html`**
- Interactive web app
- Visual editor
- Real-time updates

### Python Script
**`control_mapper.py`**
- Generate markdown files
- Command-line tool
- Custom presets

### Generated Output
**`output/Blitzcrank_custom_controls.md`**
- Complete move list
- With your keys
- Printable format

---

## 🎮 Use Cases

### "I remapped my controls"
→ Set your custom keys, see all moves update instantly

### "I use a different keyboard layout"
→ Try the 4 presets or make your own

### "I want to learn without confusion"
→ See moves with the EXACT keys you press

### "I share my PC with someone who uses different controls"
→ Generate separate guides for each person

---

## 📖 How It Works

### Step 1: You Set Your Keys
```
Light = J
Medium = K
Special = M
Down = S
```

### Step 2: System Converts Everything
```
FGC Notation → Your Keys

5L        →  Press J
2S1       →  Hold S + Press M
5L > 5S1  →  Press J → Press M
```

### Step 3: You See Your Custom Guide
```
Air Purifier (2S1)
Your Keys: Hold S + Press M
When: Opponent jumps
```

---

## ⚡ Super Quick Example

### Before Custom Controls:
**Move List Says:**
> "Use 2S1 for anti-air"

**You Think:**
> "What the heck is 2S1? What buttons is that?"

### After Custom Controls:
**Move List Says:**
> "Air Purifier: Hold S + Press M"

**You Think:**
> "Oh! Down + Special. Got it!" ✅

---

## 🏆 Benefits

### ✅ Zero Mental Translation
No more converting notation to keys in your head

### ✅ Learn Faster
See exactly what to press from day one

### ✅ Less Mistakes
No confusion about which key does what

### ✅ Any Layout Works
Keyboard, controller mapping, accessibility setup

### ✅ Always Accurate
Change controls? Everything updates automatically

---

## 📝 What The Output Looks Like

### Your Control Legend
```
🎮 Your Current Controls
──────────────────────────
Movement:
  W = Jump
  S = Crouch
  A = Back
  D = Forward

Attacks:
  J = Light
  K = Medium
  L = Heavy
  M = Special
```

### Your Moves
```
Standing Light (5L)
Your Keys: Press J
→ Quick jab, combo starter

Air Purifier (2S1)
Your Keys: Hold S + Press M
→ Anti-air special, +44 on block!

Rocket Grab (5S1)
Your Keys: Press M
→ Long-range grab, zone control
```

### Your Combos
```
Basic BnB Combo ⭐
Notation: 5L > 5L > 5S1
Your Keys: Press J → Press J → Press M
Damage: ~150
When: Close range, after plus frames
```

---

## 🎯 Start Now

### Option 1: Web Interface (Fastest)
```
1. Open: output/custom_controls.html
2. Click a preset OR type your keys
3. See all moves with YOUR keys!
```

### Option 2: Generate File
```bash
python control_mapper.py
# Creates: output/Blitzcrank_custom_controls.md
```

---

## 💡 Pro Tips

### Tip 1: Try All Presets
Load each preset to see which layout feels best

### Tip 2: Save Often
Click "💾 Save" to keep your custom setup

### Tip 3: Export for Backup
Click "📄 Export" to download your config

### Tip 4: Print Your Guide
Generate markdown file and print for desk reference

### Tip 5: Share with Friends
Generate custom guides for each person's controls

---

## 🆘 Common Questions

### Q: "Can I use any keys?"
**A:** Yes! All 12 controls are fully customizable.

### Q: "Will combos be converted too?"
**A:** Yes! Full combo sequences are translated to your key presses.

### Q: "Can I save multiple layouts?"
**A:** Yes! Export to JSON and save different files.

### Q: "Does this work for other characters?"
**A:** Yes! The system works for any character (Blitzcrank shown as example).

### Q: "I use a controller, not keyboard. Does this help?"
**A:** Yes! Map your controller buttons to see moves in your controller layout.

---

## 📊 Feature Comparison

| Feature | Manual Notation | Custom Controls System |
|---------|----------------|------------------------|
| Shows FGC notation | ✅ | ✅ |
| Shows your keys | ❌ | ✅✅✅ |
| Updates when you remap | ❌ | ✅ Auto |
| Converts combos | ❌ | ✅ Full sequences |
| Multiple presets | ❌ | ✅ 4 built-in |
| Save configuration | ❌ | ✅ Browser + JSON |
| Mental translation | 😰 Required | ✅ None! |

---

## 🎉 Result

**You get a personalized move guide that speaks YOUR keyboard language!**

No notation confusion. No mental translation. Just pure, direct instructions:

> "Press YOUR keys to do YOUR moves!"

---

**Main File:** `output/custom_controls.html`  
**Full Guide:** `CUSTOM_CONTROLS_GUIDE.md`  
**Python Tool:** `control_mapper.py`

**Just open the HTML file and start customizing!** 🚀
