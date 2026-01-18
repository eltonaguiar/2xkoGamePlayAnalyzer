# QA Final Report - Frame Data Validation & Safety Analysis

## ✅ QA Results Summary

### Frame Data Validation
- ✅ **0 Errors** across all 11 characters
- ✅ **0 Warnings** - All data is consistent
- ✅ **All frame values valid** (startup >= 0, recovery >= 0, active >= 0, damage >= 0)

### Characters Validated
1. ✅ Blitzcrank (9 moves)
2. ✅ Ahri (8 moves)
3. ✅ Braum (8 moves)
4. ✅ Darius (8 moves)
5. ✅ Ekko (8 moves)
6. ✅ Illaoi (8 moves)
7. ✅ Yasuo (8 moves)
8. ✅ Jinx (8 moves)
9. ✅ Vi (8 moves)
10. ✅ Teemo (8 moves)
11. ✅ Warwick (8 moves)

**Total: 88 moves validated**

---

## 📊 Safest Moves Analysis

### Definition
**Safest moves** = Moves with best frame advantage on block (highest on_block value)

### Top Safest Moves Per Character

| Character | Safest Move | On Block | Notes |
|-----------|-------------|----------|-------|
| **Blitzcrank** | **2S1 (Air Purifier)** | **+5** | ✅ **SAFEST MOVE IN GAME** |
| **Blitzcrank** | **5S1 (Rocket Grab)** | **+4** | ✅ **Very safe** |
| Ahri | 5L | -1 | Relatively safe |
| Braum | 5L | -1 | Relatively safe |
| Darius | 2L | -2 | Relatively safe |
| Ekko | 2L | -1 | Relatively safe |
| Illaoi | 2L | -2 | Relatively safe |
| Yasuo | 2L | -1 | Relatively safe |
| Jinx | 5L | -2 | Relatively safe |
| Vi | 2L | -1 | Relatively safe |
| Teemo | 5L | -1 | Relatively safe |
| Warwick | 2L | -1 | Relatively safe |

### Key Finding
**Only Blitzcrank has truly safe moves** (on_block >= 0). All other characters' "safest" moves are still slightly unsafe (-1 to -3), meaning they can be punished but are relatively manageable.

---

## ⚠️ Dangerous Moves Analysis

### Definition
**Dangerous moves** = Moves that are:
- Very unsafe on block (< -8)
- OR require assist cover
- OR have very long recovery (> 30f)
- OR have high risk level

### Danger Score Calculation
- **On Block < -10**: +3 points
- **On Block < -8**: +2 points
- **On Block < -5**: +1 point
- **Recovery > 30f**: +2 points
- **Recovery > 20f**: +1 point
- **Requires Assist**: +3 points
- **Risk Level High**: +2 points
- **Risk Level Medium**: +1 point

**Score 6-10/10**: Extremely dangerous, MUST use with assist
**Score 4-5/10**: Very dangerous, should use with assist
**Score 3/10**: Dangerous, use carefully

### Most Dangerous Moves

#### Blitzcrank
1. **2H**: -16 on block, 33f recovery, **Danger Score: 6/10** ⚠️
   - **MOST DANGEROUS MOVE**
   - Only use with assist cover or after conditioning
   
2. **5H**: -10 on block, 31f recovery, **Danger Score: 5/10** ⚠️
   - Very unsafe, needs spacing or assist
   
3. **2S2 (Garbage Collection)**: Command grab, requires assist
   - **HIGH RISK** - Only use with assist cover

#### Other Characters
Most characters have moves with:
- **Danger Score 3-4/10**: Heavy attacks (5H, 2H) with -6 to -8 on block
- These are unsafe but manageable with proper spacing
- None are as dangerous as Blitzcrank's 2H (-16)

---

## 🎯 Safety Categories

### ✅ Truly Safe (on_block >= 0)
- **Blitzcrank 2S1**: +5 on block
- **Blitzcrank 5S1**: +4 on block
- **Usage**: Safe to use in pressure, gives frame advantage

### ⚠️ Relatively Safe (on_block -1 to -3)
- Most characters' light attacks
- **Usage**: Can be made safe with spacing or cancels
- Good for pressure but need to be careful

### ❌ Unsafe (on_block -4 to -8)
- Medium attacks, some specials
- **Usage**: Need spacing or assist cover
- Can be punished if blocked at close range

### 🔴 Very Unsafe (on_block < -8)
- Heavy attacks (5H, 2H)
- **Danger Score: 4-6/10**
- **Usage**: Should only use with assist cover or after conditioning

### 🚨 Extremely Dangerous (on_block < -10 OR requires_assist)
- **Danger Score: 6-10/10**
- **Usage**: MUST use with assist cover
- Examples: Blitzcrank 2H (-16), command grabs

---

## 📋 UI Updates

### Safest Moves Tab
Now includes:
- ✅ **View dropdown** with 3 options:
  - "Safest Moves" - Shows safest moves only
  - "Dangerous Moves" - Shows dangerous moves that need assist
  - "Both" - Shows both side-by-side

- ✅ **Safest Moves Section** (Green):
  - Top 5 safest moves per character
  - Shows on_block, startup, recovery, damage
  - Clear "Safe" indicator (✅ Yes / ❌ No)

- ✅ **Dangerous Moves Section** (Red):
  - Moves that need assist cover
  - **Danger Score** (0-10 scale)
  - **"Needs Assist"** column (⚠️ YES / No)
  - Color-coded by danger level
  - Warning message about usage

---

## 🔍 How to Use the Safety Analysis

### View Safest Moves
1. Open `output/character_database_embedded.html`
2. Click **"Safest Moves"** tab
3. Select **"Safest Moves"** from View dropdown
4. See top 5 safest moves for each character
5. Look for moves with **+** on block (truly safe)

### View Dangerous Moves
1. Same tab, select **"Dangerous Moves"** from View dropdown
2. See moves that need assist cover
3. Check **Danger Score**:
   - **6-10/10**: Extremely dangerous (red background)
   - **4-5/10**: Very dangerous (yellow background)
   - **3/10**: Dangerous (gray background)
4. Look for **"⚠️ YES"** in "Needs Assist" column

### View Both
1. Select **"Both"** from View dropdown
2. See safest and dangerous moves side-by-side
3. Compare safety across all characters

---

## 📊 Key Findings

### Blitzcrank Safety Profile
- ✅ **2S1 (Air Purifier)**: +5 on block - **SAFEST MOVE IN GAME**
- ✅ **5S1 (Rocket Grab)**: +4 on block - **Very safe**
- ❌ **2H**: -16 on block - **MOST DANGEROUS MOVE** (Danger Score: 6/10)
- ❌ **5H**: -10 on block - **Very unsafe** (Danger Score: 5/10)
- ⚠️ **2S2 (Garbage Collection)**: Command grab, requires assist

### Other Characters
- Most characters don't have truly safe moves (on_block >= 0)
- Their "safest" moves are still slightly unsafe (-1 to -3)
- Heavy attacks are universally dangerous across all characters
- Most dangerous moves have Danger Score 3-4/10 (manageable)

---

## ✅ QA Report Files

1. **`output/QA_FRAME_DATA_REPORT.md`**
   - Full validation results
   - Safest moves table for all characters
   - Dangerous moves table with danger scores

2. **`qa_frame_data.py`**
   - QA script that validates frame data
   - Identifies safest and dangerous moves
   - Can be run anytime to verify data

---

## 🎯 Summary

**Frame Data Status:**
- ✅ All 11 characters validated
- ✅ 0 errors, 0 warnings
- ✅ All frame data is mathematically valid

**Safety Analysis:**
- ✅ Safest moves identified for all characters
- ✅ Dangerous moves identified with danger scores (0-10)
- ✅ Clear indication of which moves need assist cover
- ✅ UI updated to show both safest and dangerous moves
- ✅ Color-coded danger levels for easy identification

**The system now clearly shows:**
- ✅ Which moves are **safest** (best for pressure)
- ✅ Which moves are **dangerous** and need assist cover
- ✅ **Danger Score** (0-10) indicating how risky a move is
- ✅ Clear warnings about when to use dangerous moves

**All frame data is valid and safety analysis is complete!** 🚀
