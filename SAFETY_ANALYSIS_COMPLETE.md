# Safety Analysis Complete - Safest vs Dangerous Moves

## ✅ QA Complete

### Frame Data Validation
- ✅ **0 Errors** - All frame data is valid
- ✅ **0 Warnings** - No inconsistencies
- ✅ **11/11 Characters** validated
- ✅ **88 moves** checked

---

## 📊 Safest Moves (Best for Pressure)

### Definition
Moves with **best frame advantage on block** - safe to use in pressure strings.

### Top Safest Moves

#### Blitzcrank (Only character with truly safe moves)
1. **2S1 (Air Purifier)**: **+5 on block** ✅ **SAFEST MOVE IN GAME**
   - Startup: 20f, Recovery: 43f
   - Perfect for anti-air and pressure
   
2. **5S1 (Rocket Grab)**: **+4 on block** ✅ **VERY SAFE**
   - Startup: 25f, Recovery: 30f
   - Safe to use in neutral and pressure

#### Other Characters (Relatively Safe)
- **Ahri**: 5L (-1 on block)
- **Braum**: 5L (-1 on block)
- **Darius**: 2L (-2 on block)
- **Ekko**: 2L (-1 on block)
- **Illaoi**: 2L (-2 on block)
- **Yasuo**: 2L (-1 on block)
- **Jinx**: 5L (-2 on block)
- **Vi**: 2L (-1 on block)
- **Teemo**: 5L (-1 on block)
- **Warwick**: 2L (-1 on block)

**Note**: Other characters' "safest" moves are still slightly unsafe (-1 to -3), meaning they can be punished but are relatively manageable.

---

## ⚠️ Dangerous Moves (Need Assist Cover)

### Definition
Moves that are:
- **Very unsafe on block** (< -8)
- **OR require assist cover**
- **OR have very long recovery** (> 30f)
- **OR have high risk level**

### Danger Score (0-10)
- **6-10/10**: Extremely dangerous - **MUST use with assist**
- **4-5/10**: Very dangerous - **Should use with assist**
- **3/10**: Dangerous - Use carefully

### Most Dangerous Moves

#### Blitzcrank
1. **2H**: -16 on block, 33f recovery
   - **Danger Score: 6/10** 🔴
   - **MOST DANGEROUS MOVE**
   - ⚠️ **Only use with assist cover or after conditioning**
   
2. **5H**: -10 on block, 31f recovery
   - **Danger Score: 5/10** 🔴
   - ⚠️ **Very unsafe - needs spacing or assist**
   
3. **2S2 (Garbage Collection)**: Command grab, requires assist
   - ⚠️ **HIGH RISK** - Only use with assist cover

#### Other Characters
Most characters have moves with:
- **Danger Score 3-4/10**: Heavy attacks (5H, 2H) with -6 to -8 on block
- These are unsafe but manageable with proper spacing
- None are as dangerous as Blitzcrank's 2H (-16)

---

## 🎯 How to Use in UI

### View Safest Moves
1. Open `output/character_database_embedded.html`
2. Click **"Safest Moves"** tab
3. Select **"Safest Moves"** from View dropdown
4. See top 5 safest moves per character
5. Look for **green sections** with ✅ indicators

### View Dangerous Moves
1. Same tab, select **"Dangerous Moves"** from View dropdown
2. See moves that need assist cover
3. Check **Danger Score**:
   - **Red background** (6-10/10): Extremely dangerous
   - **Yellow background** (4-5/10): Very dangerous
   - **Gray background** (3/10): Dangerous
4. Look for **"⚠️ YES"** in "Needs Assist" column

### View Both
1. Select **"Both"** from View dropdown
2. See safest (green) and dangerous (red) moves side-by-side
3. Compare safety across all characters

---

## 📋 Safety Categories

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

## ✅ Files Generated

1. **`qa_frame_data.py`**
   - QA script that validates all frame data
   - Identifies safest and dangerous moves
   - Calculates danger scores

2. **`output/QA_FRAME_DATA_REPORT.md`**
   - Full validation results
   - Safest moves table for all characters
   - Dangerous moves table with danger scores

3. **Updated HTML**
   - Safest Moves tab now shows:
     - Safest moves (green section)
     - Dangerous moves (red section)
     - View dropdown to switch between views
     - Danger scores and assist requirements

---

## 🎯 Summary

**Frame Data Status:**
- ✅ All 11 characters validated
- ✅ 0 errors, 0 warnings
- ✅ All frame data is mathematically valid

**Safety Analysis:**
- ✅ **Safest moves** clearly identified for all characters
- ✅ **Dangerous moves** identified with danger scores (0-10)
- ✅ Clear indication of which moves **need assist cover**
- ✅ UI updated to show both safest and dangerous moves
- ✅ Color-coded danger levels for easy identification

**The system now clearly shows:**
- ✅ Which moves are **safest** (best for pressure)
- ✅ Which moves are **dangerous** and need assist cover
- ✅ **Danger Score** (0-10) indicating how risky a move is
- ✅ Clear warnings about when to use dangerous moves

**All frame data is valid and safety analysis is complete!** 🚀
