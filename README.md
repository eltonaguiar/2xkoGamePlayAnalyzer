# 2XKO Gameplay Analyzer

⚠️ **WARNING: This is a broken draft proof of concept. Do not use in production.**

This project is an experimental, incomplete prototype for analyzing 2XKO fighting game gameplay videos. Many features are non-functional, video playback has known issues, and the codebase contains bugs and incomplete implementations.

## ⚠️ Current Status: BROKEN DRAFT

- **Video playback**: Multiple player methods fail, codec compatibility issues
- **Analysis accuracy**: Untested and likely inaccurate
- **Error handling**: Incomplete, may crash unexpectedly
- **Code quality**: Proof of concept code, not production-ready
- **Documentation**: Incomplete and may be outdated

## What This Project Attempts To Do

A tool for analyzing 2XKO fighting game gameplay videos with:
- Mirror matchup analysis with character-specific frame data
- Mistake detection (unsafe moves, missed opportunities)
- Timestamp reports for key events
- Player analysis and playstyle evaluation
- Move suggestions based on frame data

## Known Issues

- Video codec incompatibility (mp4v codec not supported by browsers)
- JavaScript errors in video player
- Incomplete error handling
- Untested analysis accuracy
- Missing features and incomplete implementations

## Installation

```bash
pip install -r requirements.txt
```

## Usage (At Your Own Risk)

```bash
python analyzer.py --video "path/to/video.mp4" --matchup mirror --character Blitzcrank
```

**Note**: This may not work as expected. See known issues above.

## Project Structure

- `analyzer.py` - Main analysis script (incomplete)
- `video_processor.py` - Video processing (may have bugs)
- `clip_generator.py` - Video clip extraction (codec issues)
- `output/video_player.html` - Video player (multiple playback failures)
- `output/video_player_backup.html` - Alternative player (experimental)

## Contributing

**This is a draft proof of concept.** Contributions welcome, but be aware this is experimental code.

## License

See LICENSE file (if present).

---

**Again: This is a broken draft proof of concept. Use at your own risk.**
