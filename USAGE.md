# 2XKO Gameplay Analyzer - Usage Guide

## Quick Start

### Basic Usage

```bash
python run_analysis.py
```

This will analyze the default video file (Blitzcrank vs Blitzcrank).

### Custom Video Analysis

```bash
python analyzer.py --video "C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4" --matchup mirror --character Blitzcrank
```

**With custom output file:**
```bash
python analyzer.py --video "C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4" --matchup mirror --character Blitzcrank --output my_report.json
```

### Command Line Options

- `--video` / `-v`: Path to MP4 video file (required)
- `--matchup` / `-m`: Matchup type (currently only "mirror" supported)
- `--character` / `-c`: Character name (default: "Blitzcrank")
- `--output` / `-o`: Output JSON file path (optional)

## Output

The analyzer generates:

1. **Console Report**: Detailed analysis printed to console with:
   - Player 1 & 2 analysis (playstyle, pros, cons)
   - Mistakes with timestamps
   - Key events timeline
   - Recommendations

2. **JSON Report**: Saved to `analysis_report.json` (or custom path) containing:
   - Video metadata
   - Matchup information
   - Detailed player statistics
   - All detected events with timestamps
   - Frame-by-frame analysis data

## Understanding the Analysis

### Playstyle Analysis
The tool evaluates each player's approach:
- **Aggressive**: Uses many unsafe moves
- **Defensive**: Misses punish opportunities
- **Balanced**: Good mix of offense and defense

### Mistake Detection
Currently detects:
- Unsafe moves used without proper setup
- Risky specials in neutral
- Missed punish opportunities

### Key Events
Tracks important moments:
- Hit/block interactions
- Unsafe moves
- Good move usage
- Special move usage

## Current Limitations

1. **Move Detection**: Currently uses frame difference analysis and simulated detection. Full computer vision-based move recognition requires:
   - Character pose detection models
   - VFX pattern recognition
   - Motion flow analysis
   - ML models trained on move animations

2. **Character Support**: Currently only Blitzcrank is fully implemented. To add more characters:
   - Add character data to `character_data.py`
   - Implement character-specific move detection in `move_detector.py`

3. **Matchup Types**: Only mirror matchups are currently supported. Different character matchups require additional frame data and matchup-specific analysis.

## Future Enhancements

- Real-time move detection using computer vision
- Combo detection and optimization
- Neutral game analysis
- Defense evaluation
- Assist call analysis
- Steam Steam resource management tracking
- Frame-perfect timing analysis

## Technical Details

- **Video Processing**: Uses OpenCV for frame extraction
- **Frame Analysis**: Analyzes every 2nd frame by default (configurable)
- **Detection Thresholds**: Configurable in `config.py`
- **Character Data**: Sourced from 2XKO wiki frame data
