# How to Use the Character Database

## 🚨 CORS Error Fix

**Problem:** "Failed to fetch" error when opening HTML directly  
**Cause:** Browsers block loading JSON files when opening HTML from file system (file:// protocol)

## ✅ Solution 1: Use Embedded HTML (Easiest)

**Generate embedded version:**
```bash
python generate_embedded_html.py
```

**Then open:**
```
output/character_database_embedded.html
```

**This file works when opened directly - no server needed!**

---

## ✅ Solution 2: Use Local Server

**Start local server:**
```bash
cd output
python start_local_server.py
```

**Or double-click:**
```
output/start_local_server.bat
```

**Then open in browser:**
```
http://localhost:8000/character_database.html
```

---

## 📊 About Characters

### Current Status

**Only Blitzcrank has complete data:**
- ✅ 9 moves (all normals + specials)
- ✅ 8 BnB combos
- ✅ Complete frame data
- ✅ Strategies and matchups

### To Add More Characters

**See:** `ADDING_CHARACTERS.md` for full guide

**Quick steps:**
1. Add character class to `character_data.py`
2. Register in `CHARACTER_DATA` dict
3. Run `python generate_database.py`
4. Run `python generate_embedded_html.py` (if using embedded version)
5. Refresh browser - new character appears!

---

## 🎯 Quick Start

### Option 1: Embedded (No Server)
```bash
# Generate embedded HTML
python generate_embedded_html.py

# Open the file
output/character_database_embedded.html
```

### Option 2: Local Server
```bash
# Start server
cd output
python start_local_server.py

# Browser opens automatically at:
# http://localhost:8000/character_database.html
```

---

## 🔍 Verification

**After generating:**
- ✅ All 9 Blitzcrank moves visible
- ✅ All 8 BnB combos visible
- ✅ No CORS errors
- ✅ All tabs working

**If you see errors:**
1. Make sure `character_database.json` exists (run `python generate_database.py`)
2. Use embedded version OR local server
3. Check browser console for specific errors

---

## 📝 Files

- `character_database.html` - Original (needs server or embedded data)
- `character_database_embedded.html` - **Use this one!** (works directly)
- `character_database.json` - Data file (used by HTML)
- `start_local_server.py` - Local server script

---

**Recommended:** Use `character_database_embedded.html` - it works without any setup! 🎉
