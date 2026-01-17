"""
Configuration file for 2XKO Gameplay Analyzer
"""

# Analysis settings
ANALYSIS_SETTINGS = {
    "frame_sample_rate": 2,  # Analyze every Nth frame (1 = all frames)
    "min_frames_between_events": 30,  # Minimum frames between detected events
    "activity_threshold": 1.2,  # Ratio threshold for determining active player
    "bright_pixel_threshold": 1000,  # Threshold for hit/block detection
}

# Character-specific analysis settings
BLITZCRANK_ANALYSIS = {
    "unsafe_move_threshold": -5,  # Moves with on_block < this are considered unsafe
    "punish_window_threshold": 5,  # Minimum frames for punish opportunity
    "steam_detection_threshold": 0.1,  # 10% of region must have steam VFX
}

# Report settings
REPORT_SETTINGS = {
    "include_timestamps": True,
    "include_frame_numbers": True,
    "include_suggestions": True,
    "detailed_analysis": True,
}

# Matchup types
MATCHUP_TYPES = {
    "mirror": {
        "description": "Same character vs same character",
        "supported": True
    },
    "different": {
        "description": "Different characters",
        "supported": False  # Coming soon
    }
}
