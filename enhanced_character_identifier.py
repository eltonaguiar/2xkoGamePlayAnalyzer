"""
Enhanced character identifier with starting position detection.
"""

from character_identifier import CharacterIdentifier
import cv2
import numpy as np
from typing import Dict, Tuple, Optional
from collections import Counter


class EnhancedCharacterIdentifier(CharacterIdentifier):
    """Enhanced character identifier with starting position detection"""
    
    def identify_characters_at_start(self) -> Dict:
        """
        Identify characters at the very start of the round
        
        Returns:
            Dictionary with character info including starting positions
        """
        # Get first few frames
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        character_info = {}
        positions = {"player1": [], "player2": []}
        
        # Sample first 10 frames
        for frame_num in range(0, min(10, int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # Detect character positions
            p1_pos, p2_pos = self._detect_starting_positions(frame)
            if p1_pos:
                positions["player1"].append(p1_pos)
            if p2_pos:
                positions["player2"].append(p2_pos)
        
        # Get most common positions
        if positions["player1"]:
            p1_start = Counter(positions["player1"]).most_common(1)[0][0]
        else:
            p1_start = "left"  # Default
        
        if positions["player2"]:
            p2_start = Counter(positions["player2"]).most_common(1)[0][0]
        else:
            p2_start = "right"  # Default
        
        # Extract character images at start
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 5)  # Use frame 5 for character image
        ret, start_frame = self.cap.read()
        
        if ret:
            # Extract character images
            p1_img = self._extract_character_region(start_frame, "player1")
            p2_img = self._extract_character_region(start_frame, "player2")
            
            # Detect colors
            p1_colors = self.detect_character_colors(p1_img) if p1_img is not None else {}
            p2_colors = self.detect_character_colors(p2_img) if p2_img is not None else {}
            
            character_info = {
                "player1": {
                    "image": p1_img,
                    "colors": p1_colors,
                    "starting_position": p1_start
                },
                "player2": {
                    "image": p2_img,
                    "colors": p2_colors,
                    "starting_position": p2_start
                }
            }
        
        return character_info
    
    def _detect_starting_positions(self, frame: np.ndarray) -> Tuple[Optional[str], Optional[str]]:
        """
        Detect starting positions of characters
        
        Returns:
            Tuple of (player1_position, player2_position) - "left" or "right"
        """
        height, width = frame.shape[:2]
        left_half = frame[:, :width//2]
        right_half = frame[:, width//2:]
        
        # Detect character presence
        left_chars = self._count_character_pixels(left_half)
        right_chars = self._count_character_pixels(right_half)
        
        # Determine positions
        if left_chars > right_chars * 1.2:
            return ("left", "right")
        elif right_chars > left_chars * 1.2:
            return ("right", "left")
        else:
            # Ambiguous - return None
            return (None, None)
    
    def _count_character_pixels(self, region: np.ndarray) -> int:
        """Count character-like pixels in region"""
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        # Character pixels are typically medium brightness
        mask = (gray > 30) & (gray < 220)
        return np.sum(mask)
