# QA Complete - Frame Data Validation & Safety Analysis

## ✅ QA Results

### Frame Data Validation
- ✅ **0 Errors** - All frame data is valid
- ✅ **0 Warnings** - No data inconsistencies found
- ✅ **11/11 Characters** validated

### Validation Checks Performed
- ✅ Startup frames: All >= 0
- ✅ Recovery frames: All >= 0
- ✅ Active frames: All >= 0
- ✅ Damage values: All >= 0
- ✅ Guard types: All specified
- ✅ Safety flags: Consistent with on_block values

---

## 📊 Safest Moves Analysis

### Top Safest Moves Per Character

**Blitzcrank:**
1. **2S1 (Air Purifier)**: +5 on block ✅ **SAFEST**
2. **5S1 (Rocket Grab)**: +4 on block ✅ **SAFE**
3. **5L**: -2 on block (slightly unsafe but manageable)

**Other Characters:**
- Most characters' safest moves are around -1 to -3 on block
- These are "relatively safe" but not truly safe
- Only Blitzcrank has moves that are actually plus on block

---

## ⚠️ Dangerous Moves Analysis

### Moves That Need Assist Cover

**Blitzcrank:**
1. **2H**: -16 on block, 33f recovery, Danger Score: 6/10
   - ⚠️ **Very unsafe** - Only use with assist or after conditioning
2. **5H**: -10 on block, 31f recovery, Danger Score: 5/10
   - ⚠️ **Unsafe** - Needs careful spacing or assist
3. **2S2 (Garbage Collection)**: Command grab, requires assist
   - ⚠️ **HIGH RISK** - Only use with assist cover

**Other Characters:**
- Most characters have moves with -6 to -8 on block
- These are unsafe but manageable with proper spacing
- Heavy attacks (5H, 2H) are typically the most dangerous

---

## 🎯 Safety Categories

### ✅ Truly Safe Moves (on_block >= 0)
- **Blitzcrank 2S1**: +5 on block
- **Blitzcrank 5S1**: +4 on block
- These moves give frame advantage and are safe to use in pressure

### ⚠️ Relatively Safe Moves (on_block -1 to -3)
- Most characters' light attacks
- Can be made safe with spacing or cancels
- Good for pressure but need to be careful

### ❌ Unsafe Moves (on_block -4 to -8)
- Medium attacks, some specials
- Need spacing or assist cover
- Can be punished if blocked at close range

### 🔴 Very Unsafe Moves (on_block < -8)
- Heavy attacks (5H, 2H)
- **Danger Score 4-6/10**
- **Should only use with assist cover or after conditioning**

### 🚨 Extremely Dangerous (on_block < -10 OR requires_assist)
- **Danger Score 6-10/10**
- **MUST use with assist cover**
- Examples: Blitzcrank 2H (-16), command grabs

---

## 📋 Updated UI Features

### Safest Moves Tab
Now includes:
- ✅ **View dropdown**: "Safest Moves", "Dangerous Moves", or "Both"
- ✅ **Safest Moves section**: Shows top 5 safest moves per character
- ✅ **Dangerous Moves section**: Shows moves that need assist
- ✅ **Danger Score**: 0-10 scale indicating how dangerous a move is
- ✅ **Color coding**: Red for dangerous, green for safe
- ✅ **Clear warnings**: Notes about when to use dangerous moves

---

## 🔍 How to Use

### View Safest Moves
1. Open `output/character_database_embedded.html`
2. Click **"Safest Moves"** tab
3. Select **"Safest Moves"** from View dropdown
4. See top 5 safest moves for each character

### View Dangerous Moves
1. Same tab, select **"Dangerous Moves"** from View dropdown
2. See moves that need assist cover
3. Check **Danger Score** - higher = more dangerous
4. Look for **"⚠️ YES"** in "Needs Assist" column

### View Both
1. Select **"Both"** from View dropdown
2. See safest and dangerous moves side-by-side
3. Compare safety across all characters

---

## 📊 Key Findings

### Blitzcrank Safety Analysis
- ✅ **2S1 (Air Purifier)**: +5 on block - **SAFEST MOVE IN GAME**
- ✅ **5S1 (Rocket Grab)**: +4 on block - **Very safe**
- ❌ **2H**: -16 on block - **MOST DANGEROUS** (needs assist)
- ❌ **5H**: -10 on block - **Very unsafe** (needs spacing/assist)

### Other Characters
- Most characters don't have truly safe moves (on_block >= 0)
- Their "safest" moves are still slightly unsafe (-1 to -3)
- Heavy attacks are universally dangerous across all characters

---

## ✅ QA Report Generated

**File:** `output/QA_FRAME_DATA_REPORT.md`

Contains:
- Full validation results
- Safest moves table for all characters
- Dangerous moves table with danger scores
- Recommendations for each character

---

## 🎯 Summary

**Frame Data Status:**
- ✅ All 11 characters validated
- ✅ 0 errors, 0 warnings
- ✅ All frame data is mathematically valid

**Safety Analysis:**
- ✅ Safest moves identified for all characters
- ✅ Dangerous moves identified with danger scores
- ✅ Clear indication of which moves need assist cover
- ✅ UI updated to show both safest and dangerous moves

**The system now clearly shows which moves are safe to use and which need assist cover!** 🚀
