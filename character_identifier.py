"""
Character identification module for extracting player information.
"""

import cv2
import numpy as np
from typing import Dict, Tuple, Optional, List
from collections import Counter
import os


class CharacterIdentifier:
    """Identifies and extracts character information from gameplay"""
    
    def __init__(self, video_path: str):
        """
        Initialize character identifier
        
        Args:
            video_path: Path to video file
        """
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Player regions (left and right sides)
        self.player1_region = (0, 0, self.width // 2, self.height)
        self.player2_region = (self.width // 2, 0, self.width // 2, self.height)
    
    def extract_character_images(self, num_samples: int = 10) -> Dict[str, np.ndarray]:
        """
        Extract character images from video
        
        Args:
            num_samples: Number of frames to sample
        
        Returns:
            Dictionary with player1 and player2 character images
        """
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_indices = np.linspace(total_frames // 4, 3 * total_frames // 4, num_samples, dtype=int)
        
        player1_images = []
        player2_images = []
        
        for frame_idx in sample_indices:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # Extract character regions
            p1_img = self._extract_character_region(frame, "player1")
            p2_img = self._extract_character_region(frame, "player2")
            
            if p1_img is not None:
                player1_images.append(p1_img)
            if p2_img is not None:
                player2_images.append(p2_img)
        
        # Get representative images (middle frame)
        result = {}
        if player1_images:
            result["player1"] = player1_images[len(player1_images) // 2]
        if player2_images:
            result["player2"] = player2_images[len(player2_images) // 2]
        
        return result
    
    def _extract_character_region(self, frame: np.ndarray, player: str) -> Optional[np.ndarray]:
        """Extract character region from frame"""
        if player == "player1":
            x, y, w, h = self.player1_region
        else:
            x, y, w, h = self.player2_region
        
        # Focus on middle-bottom area where characters typically are
        char_y = int(y + h * 0.3)
        char_h = int(h * 0.5)
        char_region = frame[char_y:char_y+char_h, x:x+w]
        
        if char_region.size > 0:
            return char_region
        return None
    
    def detect_character_colors(self, character_image: np.ndarray) -> Dict[str, Tuple[int, int, int]]:
        """
        Detect dominant colors in character image
        
        Args:
            character_image: Character image array
        
        Returns:
            Dictionary with primary and secondary colors
        """
        if character_image is None or character_image.size == 0:
            return {"primary": (0, 0, 0), "secondary": (0, 0, 0)}
        
        # Reshape image to list of pixels
        pixels = character_image.reshape(-1, 3)
        
        # Remove black/dark pixels (background)
        brightness = np.sum(pixels, axis=1)
        bright_pixels = pixels[brightness > 50]
        
        if len(bright_pixels) == 0:
            return {"primary": (0, 0, 0), "secondary": (0, 0, 0)}
        
        # Use K-means to find dominant colors
        try:
            from sklearn.cluster import KMeans
            
            kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
            kmeans.fit(bright_pixels)
            
            colors = kmeans.cluster_centers_.astype(int)
            
            # Sort by frequency
            labels = kmeans.labels_
            label_counts = Counter(labels)
            sorted_colors = sorted(zip(colors, [label_counts[i] for i in range(len(colors))]), 
                                  key=lambda x: x[1], reverse=True)
            
            primary = tuple(sorted_colors[0][0].tolist())
            secondary = tuple(sorted_colors[1][0].tolist()) if len(sorted_colors) > 1 else primary
        except ImportError:
            # Fallback: use simple color averaging
            primary = tuple(np.mean(bright_pixels, axis=0).astype(int).tolist())
            secondary = primary
        
        return {
            "primary": primary,
            "secondary": secondary
        }
    
    def extract_usernames(self, num_samples: int = 5) -> Dict[str, Optional[str]]:
        """
        Extract usernames from HUD
        
        Args:
            num_samples: Number of frames to sample for username detection
        
        Returns:
            Dictionary with player1 and player2 usernames
        """
        # Sample frames from different parts of video
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        sample_indices = np.linspace(0, total_frames - 1, num_samples, dtype=int)
        
        player1_names = []
        player2_names = []
        
        for frame_idx in sample_indices:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # Try to extract usernames from HUD regions
            # Typically usernames are in top corners or above health bars
            p1_name = self._extract_username_from_region(frame, "player1")
            p2_name = self._extract_username_from_region(frame, "player2")
            
            if p1_name:
                player1_names.append(p1_name)
            if p2_name:
                player2_names.append(p2_name)
        
        # Get most common username
        result = {}
        if player1_names:
            result["player1"] = Counter(player1_names).most_common(1)[0][0]
        else:
            result["player1"] = None
        
        if player2_names:
            result["player2"] = Counter(player2_names).most_common(1)[0][0]
        else:
            result["player2"] = None
        
        return result
    
    def _extract_username_from_region(self, frame: np.ndarray, player: str) -> Optional[str]:
        """Extract username from HUD region with improved preprocessing"""
        # Try multiple HUD regions where usernames might appear
        regions_to_try = []
        
        if player == "player1":
            # Top-left regions
            regions_to_try = [
                frame[0:80, 0:self.width//4],  # Top-left corner
                frame[0:120, 0:self.width//3],  # Slightly wider
                frame[50:150, 0:self.width//4],  # Below top
            ]
        else:
            # Top-right regions
            regions_to_try = [
                frame[0:80, 3*self.width//4:self.width],  # Top-right corner
                frame[0:120, 2*self.width//3:self.width],  # Slightly wider
                frame[50:150, 3*self.width//4:self.width],  # Below top
            ]
        
        # Try OCR on each region
        for hud_region in regions_to_try:
            # Preprocess for better OCR
            gray = cv2.cvtColor(hud_region, cv2.COLOR_BGR2GRAY)
            
            # Enhance contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # Threshold to get text
            _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Try OCR (requires pytesseract)
            try:
                import pytesseract
                # Try different PSM modes
                for psm in [7, 8, 6]:
                    text = pytesseract.image_to_string(thresh, config=f'--psm {psm} -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-.')
                    text = text.strip()
                    # Filter out noise and validate
                    if text and len(text) >= 2 and len(text) <= 20:
                        # Remove common OCR errors
                        text = text.replace('|', 'I').replace('0', 'O').replace('1', 'I')
                        # Check if it looks like a username (alphanumeric + common chars)
                        if any(c.isalnum() for c in text):
                            return text
            except ImportError:
                # OCR not available - try fallback method
                pass
            except Exception as e:
                # OCR failed, try next region
                continue
        
        # Fallback: Try to detect text-like patterns without OCR
        # This is a simple heuristic that might catch some usernames
        for hud_region in regions_to_try[:1]:  # Just try first region
            gray = cv2.cvtColor(hud_region, cv2.COLOR_BGR2GRAY)
            # Look for high-contrast horizontal lines (text-like patterns)
            edges = cv2.Canny(gray, 50, 150)
            horizontal_lines = np.sum(edges, axis=1)
            if np.max(horizontal_lines) > 100:  # Has text-like patterns
                # Could extract more info here, but for now return None
                pass
        
        return None
    
    def save_character_images(self, images: Dict[str, np.ndarray], output_dir: str = "character_images"):
        """Save character images to disk"""
        os.makedirs(output_dir, exist_ok=True)
        
        saved_paths = {}
        for player, img in images.items():
            if img is not None:
                path = os.path.join(output_dir, f"{player}_character.png")
                cv2.imwrite(path, img)
                saved_paths[player] = path
        
        return saved_paths
    
    def close(self):
        """Release video capture"""
        if self.cap:
            self.cap.release()
