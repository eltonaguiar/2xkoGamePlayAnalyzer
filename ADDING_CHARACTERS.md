# Adding More Characters to the Database

## ✅ Current Status

**Blitzcrank is fully implemented with:**
- ✅ All 9 moves (5L, 5M, 5H, 2L, 2M, 2H, 5S1, 2S1, 2S2)
- ✅ Complete frame data
- ✅ 8 BnB combos
- ✅ Strategies and matchups

## 🎯 To Add More Characters

### Step 1: Add Character Class to `character_data.py`

Create a new class following the BlitzcrankData pattern:

```python
class NewCharacterData:
    """New Character data from 2XKO wiki"""
    
    @staticmethod
    def get_character_info() -> Dict:
        return {
            "name": "CharacterName",
            "archetype": "Rushdown",  # or "Zoner", "Grappler", etc.
            "health": 1000,
            "playstyle": "Description of how they play",
            "strengths": ["Strength 1", "Strength 2"],
            "weaknesses": ["Weakness 1", "Weakness 2"],
            "dash_speed": "Fast",  # or "Medium", "Slow"
            "defense_rating": "Good"  # or "Excellent", "Average", "Poor"
        }
    
    @staticmethod
    def get_moves() -> Dict[str, MoveData]:
        moves = {}
        
        # Add all moves
        moves["5L"] = MoveData(
            name="5L",
            input="5L",
            damage=50,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=6,  # Frame data
            active=3,
            recovery=10,
            on_block=-1,  # Frame advantage
            cancel_options=["N", "SP"],
            description="Quick jab",
            is_safe=False,
            risk_level="low",
            move_category="normal",
            move_type="ground",
            range="close"
        )
        
        # Add more moves: 5M, 5H, 2L, 2M, 2H, j.L, j.M, j.H, specials, etc.
        
        # Calculate safety
        for move in moves.values():
            if move.on_block >= 0:
                move.is_safe = True
        
        return moves
    
    @staticmethod
    def get_bnb_combos() -> Dict[str, Dict]:
        return {
            "combo_1": {
                "name": "Basic BnB",
                "notation": "5L > 5M > 5H",
                "english": "Light, medium, heavy",
                "inputs": "Press J > Press K > Press L",
                "hits": 3,
                "difficulty": 1,
                "damage_estimate": "~150",
                "meter_use": 0,
                "starter": "5L",
                "ender": "5H",
                "situation": "Close range hit confirm",
                "notes": "Easy combo to learn"
            }
            # Add more combos...
        }
    
    @staticmethod
    def get_top_strategies() -> List[Dict]:
        return [
            {
                "name": "Strategy 1: ...",
                "priority": 1,
                "description": "...",
                "key_moves": ["5L", "5M"],
                "execution": ["Step 1", "Step 2"],
                "success_rate": "High",
                "difficulty": "Easy"
            }
            # Add 2 more strategies...
        ]
    
    @staticmethod
    def get_most_used_moves() -> Dict:
        return {
            "neutral_game": [...],
            "pressure_game": [...],
            "variety_options": [...]
        }
    
    @staticmethod
    def get_matchup_guide() -> Dict:
        return {
            "tough_matchups": [...],
            "favorable_matchups": [...],
            "universal_tips": [...]
        }
    
    @staticmethod
    def get_move_recommendations() -> Dict:
        return {...}
    
    @staticmethod
    def get_recovery_analysis() -> Dict:
        return {...}
    
    @staticmethod
    def get_combo_goals() -> Dict:
        return {...}
```

### Step 2: Register Character

At the bottom of `character_data.py`, add to `CHARACTER_DATA`:

```python
CHARACTER_DATA = {
    "Blitzcrank": BlitzcrankData,
    "NewCharacter": NewCharacterData  # Add here
}
```

### Step 3: Regenerate Database

```bash
python generate_database.py
```

### Step 4: Refresh Browser

Open `output/character_database.html` - new character will appear!

## 📊 Data Sources

Get frame data from:
- **Official Wiki**: https://wiki.play2xko.com
- **In-game Training Mode**: Frame data display
- **Community Resources**: Discord, Reddit, etc.

## 🎯 Minimum Required Data

**To get a character working in the database:**

1. ✅ `get_character_info()` - Basic stats
2. ✅ `get_moves()` - At least a few moves with frame data
3. ✅ `get_bnb_combos()` - At least 1 combo (can be placeholder)

**Optional (for full features):**
- `get_top_strategies()` - 3 strategies
- `get_most_used_moves()` - Usage frequency
- `get_matchup_guide()` - Matchup info

## 💡 Quick Template

Copy `BlitzcrankData` class and modify:
- Change class name
- Update character info
- Replace moves with new character's moves
- Update combos
- Register in `CHARACTER_DATA`

## 🚀 Example: Adding a Simple Character

```python
class SimpleCharacterData:
    @staticmethod
    def get_character_info():
        return {
            "name": "SimpleCharacter",
            "archetype": "Rushdown",
            "health": 1000,
            "playstyle": "Fast pressure character",
            "strengths": ["Fast moves", "Good pressure"],
            "weaknesses": ["Low health"],
            "dash_speed": "Fast",
            "defense_rating": "Average"
        }
    
    @staticmethod
    def get_moves():
        moves = {}
        moves["5L"] = MoveData(
            name="5L", input="5L", damage=40,
            guard=[GuardType.LOW, GuardType.HIGH, GuardType.AIR],
            startup=6, active=3, recovery=8, on_block=-1,
            cancel_options=["N", "SP"],
            description="Fast light",
            is_safe=False, risk_level="low",
            move_category="normal", move_type="ground", range="close"
        )
        # Add more moves...
        return moves
    
    @staticmethod
    def get_bnb_combos():
        return {
            "basic": {
                "name": "Basic Combo",
                "notation": "5L > 5M",
                "english": "Light into medium",
                "inputs": "Press J > Press K",
                "hits": 2, "difficulty": 1,
                "damage_estimate": "~100",
                "meter_use": 0,
                "starter": "5L", "ender": "5M",
                "situation": "Basic hit confirm",
                "notes": "Simple combo"
            }
        }
    
    # Add other methods returning empty dicts if not ready yet
    @staticmethod
    def get_top_strategies(): return []
    @staticmethod
    def get_most_used_moves(): return {}
    @staticmethod
    def get_matchup_guide(): return {}
    @staticmethod
    def get_move_recommendations(): return {}
    @staticmethod
    def get_recovery_analysis(): return {}
    @staticmethod
    def get_combo_goals(): return {}

# Register
CHARACTER_DATA["SimpleCharacter"] = SimpleCharacterData
```

## ✅ Verification

After adding a character:

1. Run `python generate_database.py`
2. Check output shows: `Total characters: 2` (or more)
3. Open `output/character_database.html`
4. New character should appear in:
   - Character Overview tab
   - Move Database dropdown
   - All comparison tabs

## 🎮 Current Known 2XKO Characters

Based on game announcements, these characters may be in the roster:
- Blitzcrank ✅ (Fully implemented)
- Ahri (Rumored)
- Yasuo (Rumored)
- Jinx (Rumored)
- Ekko (Rumored)
- Darius (Rumored)
- Illaoi (Rumored)

**Note:** Frame data needs to be gathered from official sources or in-game testing.

---

**Once you add character data, the database will automatically include them in all comparisons!** 🎉
