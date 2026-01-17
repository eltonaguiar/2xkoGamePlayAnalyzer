"""
Quick script to generate video player for the default Blitzcrank video.
"""

import sys
from generate_video_player import main as generate_main

if __name__ == "__main__":
    # Default video path
    video_path = r"C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4"
    
    # Override with command line argument if provided
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    
    # Set as command line argument for generate_video_player
    sys.argv = [sys.argv[0], video_path]
    
    generate_main()
