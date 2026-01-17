# Video Player Feature Guide

## Overview

The video player feature creates an interactive HTML5 player that allows you to review gameplay mistakes with annotations, character identification, and filtering options.

## Features

### ✨ Key Features

1. **Annotated Video Clips**: Each mistake is extracted as a short clip (5 seconds) with on-screen annotations
2. **Player Identification**: 
   - Character images extracted from gameplay
   - Dominant color detection for visual identification
   - Username extraction from HUD (when available)
3. **Filtering System**: 
   - View all mistakes
   - Filter by Player 1 mistakes only
   - Filter by Player 2 mistakes only
4. **Proper Timestamps**: MM:SS format for videos under 1 hour, HH:MM:SS for longer videos
5. **Interactive Interface**: Click any mistake clip to play it with annotations

## Usage

### Quick Start

```bash
python run_video_player.py
```

This will automatically process the default Blitzcrank video and generate the player.

### Custom Video

```bash
python generate_video_player.py "C:\Users\zerou\Desktop\your_video.mp4"
```

### Command Line Options

```bash
python generate_video_player.py <video_path>
```

## Output Structure

After running the generator, you'll get:

```
output/
├── video_player.html          # Main HTML5 player (open this in browser)
├── metadata.json              # Complete analysis metadata
├── clips/                     # Individual mistake clips
│   ├── mistake_player1_0.mp4
│   ├── mistake_player1_1.mp4
│   └── ...
└── character_images/          # Character identification images
    ├── player1_character.png
    └── player2_character.png
```

## How It Works

### Step 1: Gameplay Analysis
- Analyzes the video for mistakes and key events
- Identifies unsafe moves, missed opportunities, etc.
- Creates timestamped mistake list

### Step 2: Character Identification
- Extracts character images from gameplay frames
- Detects dominant colors for visual identification
- Attempts to extract usernames from HUD using OCR

### Step 3: Clip Generation
- Extracts 5-second clips around each mistake
- Adds on-screen annotations (player, mistake type, description)
- Saves clips in MP4 format

### Step 4: HTML Player Generation
- Creates interactive HTML5 video player
- Includes filtering system
- Displays character info and usernames
- Shows clickable mistake list

## Player Interface

### Header Section
- **Player Cards**: Shows character images, usernames, and color indicators
- **Visual Identification**: Color-coded indicators help distinguish players

### Filter Buttons
- **All Mistakes**: Shows all mistakes from both players
- **Player 1 Mistakes**: Filters to show only Player 1 mistakes
- **Player 2 Mistakes**: Filters to show only Player 2 mistakes

### Video Player
- Standard HTML5 video controls
- Annotations appear as overlay during playback
- Shows mistake type, description, and suggestions

### Clips List
- Clickable list of all mistake clips
- Shows timestamp, mistake type, description, and suggestions
- Color-coded by player (green for P1, red for P2)

## Timestamp Format

- **Short videos (< 1 hour)**: `MM:SS` format (e.g., `02:35`)
- **Long videos (≥ 1 hour)**: `HH:MM:SS` format (e.g., `01:23:45`)

## Character Identification

### Image Extraction
- Samples multiple frames throughout the video
- Extracts character regions (middle-bottom area)
- Saves representative character images

### Color Detection
- Uses K-means clustering to find dominant colors
- Identifies primary and secondary colors
- Displays color indicators in player cards

### Username Extraction
- Attempts OCR on HUD regions (top corners)
- Samples multiple frames for accuracy
- Falls back to "Player 1" / "Player 2" if extraction fails

## Requirements

- **pytesseract**: For username extraction (optional, will work without it)
- **scikit-learn**: For color detection
- **OpenCV**: For video processing

Install missing dependencies:
```bash
pip install scikit-learn pytesseract
```

Note: pytesseract requires Tesseract OCR to be installed on your system.

## Troubleshooting

### Clips Not Playing
- Ensure clips are in the `output/clips/` directory
- Check browser console for path errors
- Verify video codec compatibility (MP4/H.264)

### Character Images Not Showing
- Check `output/character_images/` directory
- Verify image files were created
- Check browser console for path errors

### Usernames Not Extracted
- OCR may fail if HUD text is unclear
- Install Tesseract OCR for better results
- Falls back to "Player 1" / "Player 2" if extraction fails

### No Mistakes Found
- The tool will create clips from key events if no mistakes are detected
- Check the analysis report for detected events

## Browser Compatibility

- **Chrome/Edge**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Mobile browsers**: Responsive design, may have autoplay restrictions

## Future Enhancements

- Combo detection and annotation
- Neutral game analysis clips
- Defense evaluation clips
- Side-by-side comparison view
- Export clips individually
- Custom annotation styles
