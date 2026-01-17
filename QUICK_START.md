# Quick Start Guide - 2XKO Gameplay Analyzer

## How to Run the Tool

### Method 1: Quick Run (Pre-configured)
The easiest way is to use the pre-configured script:

```bash
python run_analysis.py
```

This will automatically analyze the Blitzcrank vs Blitzcrank video at:
`C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4`

### Method 2: Command Line with Options
For more control, use the main analyzer:

```bash
python analyzer.py --video "C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4" --matchup mirror --character Blitzcrank
```

**With custom output file:**
```bash
python analyzer.py --video "C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4" --matchup mirror --character Blitzcrank --output my_report.json
```

### Command Line Arguments

- `--video` / `-v`: **Required** - Path to your MP4 video file
- `--matchup` / `-m`: Matchup type (default: "mirror")
- `--character` / `-c`: Character name (default: "Blitzcrank")
- `--output` / `-o`: Optional - Custom output JSON file path (default: "analysis_report.json")

## What Happens When You Run It

1. **Video Loading**: The tool loads your video and extracts metadata (duration, FPS, resolution)
2. **Frame Extraction**: Extracts frames from the video (samples every 2nd frame for performance)
3. **Analysis**: 
   - Detects hit/block interactions
   - Identifies unsafe moves
   - Tracks player patterns
   - Analyzes mistakes and opportunities
4. **Report Generation**: 
   - Prints detailed analysis to console
   - Saves JSON report to file

## Output

You'll see:
- **Console Output**: Formatted report with timestamps, mistakes, and recommendations
- **JSON File**: Detailed data saved to `analysis_report.json` (or your custom path)

## Example Output

```
================================================================================
2XKO GAMEPLAY ANALYSIS REPORT
================================================================================

Video: C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4
Duration: 156.90s
Matchup: Blitzcrank vs Blitzcrank (mirror)

--------------------------------------------------------------------------------
PLAYER 1 ANALYSIS
--------------------------------------------------------------------------------

Mistakes:
  [00:39.200] player1 used Rocket Grab (5S1) which can be easily punished on whiff
         Suggestion: Rocket Grab is risky in neutral. Consider using it after conditioning opponent or with assist cover.
...
```

## Troubleshooting

**Error: "Video file not found"**
- Check that the video path is correct
- Use full absolute path if relative path doesn't work

**Error: "ModuleNotFoundError"**
- Install dependencies: `pip install -r requirements.txt`

**Video takes too long to process**
- The tool samples every 2nd frame by default
- For faster processing, you can modify `sample_rate` in the code
