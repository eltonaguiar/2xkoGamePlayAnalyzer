"""
Video clip generator for extracting annotated gameplay clips.
"""

import cv2
import numpy as np
import os
from typing import List, Dict, Tuple, Optional
from datetime import timedelta
import json


class ClipGenerator:
    """Generates video clips from gameplay analysis"""
    
    def __init__(self, video_path: str, output_dir: str = "clips"):
        """
        Initialize clip generator
        
        Args:
            video_path: Path to source video
            output_dir: Directory to save clips
        """
        self.video_path = video_path
        self.output_dir = output_dir
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Clips storage
        self.clips = []
    
    def extract_clip(self, start_time: float, end_time: float, clip_id: str, 
                    annotations: Dict) -> str:
        """
        Extract a clip from the video
        
        Args:
            start_time: Start time in seconds
            end_time: End time in seconds
            clip_id: Unique identifier for clip
            annotations: Dictionary with annotation data
        
        Returns:
            Path to saved clip file
        """
        # Calculate frame numbers
        start_frame = int(start_time * self.fps)
        end_frame = int(end_time * self.fps)
        
        # Set video position
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Video writer
        clip_path = os.path.join(self.output_dir, f"{clip_id}.mp4")
        
        # Use H.264 codec for browser compatibility (mp4v is not supported by browsers)
        # Try different H.264 fourcc codes in order of preference
        fourcc_options = [
            cv2.VideoWriter_fourcc(*'avc1'),  # H.264 (best browser support)
            cv2.VideoWriter_fourcc(*'H264'),  # H.264 alternative
            cv2.VideoWriter_fourcc(*'X264'),  # x264 encoder
            cv2.VideoWriter_fourcc(*'mp4v'),  # Fallback (may not work in browsers)
        ]
        
        out = None
        for fourcc in fourcc_options:
            try:
                out = cv2.VideoWriter(clip_path, fourcc, self.fps, (self.width, self.height))
                if out.isOpened():
                    break
            except:
                continue
        
        if out is None or not out.isOpened():
            # Last resort: use mp4v but warn user
            print(f"Warning: Could not initialize H.264 codec for {clip_id}. Using mp4v (may not work in browsers).")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(clip_path, fourcc, self.fps, (self.width, self.height))
        
        current_frame = start_frame
        while current_frame <= end_frame:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Annotate frame
            annotated_frame = self._annotate_frame(frame, annotations, current_frame, start_frame)
            out.write(annotated_frame)
            current_frame += 1
        
        out.release()
        
        # Store clip info
        clip_info = {
            "id": clip_id,
            "path": clip_path,
            "start_time": start_time,
            "end_time": end_time,
            "duration": end_time - start_time,
            "annotations": annotations
        }
        self.clips.append(clip_info)
        
        return clip_path
    
    def _annotate_frame(self, frame: np.ndarray, annotations: Dict, 
                       current_frame: int, start_frame: int) -> np.ndarray:
        """Annotate a frame with text overlays"""
        annotated = frame.copy()
        
        # Calculate relative time in clip
        relative_time = (current_frame - start_frame) / self.fps
        
        # Draw annotations
        if "player" in annotations:
            player = annotations["player"]
            mistake_type = annotations.get("type", "mistake")
            description = annotations.get("description", "")
            
            # Player label
            label_y = 50
            cv2.putText(annotated, f"Player: {player}", (20, label_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Mistake type
            cv2.putText(annotated, f"Type: {mistake_type}", (20, label_y + 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Description
            if description:
                cv2.putText(annotated, description[:50], (20, label_y + 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Timestamp
        timestamp = self._format_timestamp(annotations.get("timestamp", 0) + relative_time)
        cv2.putText(annotated, timestamp, (self.width - 200, self.height - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        return annotated
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp as MM:SS or HH:MM:SS"""
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def generate_clips_from_mistakes(self, mistakes: List[Dict], 
                                    clip_duration: float = 5.0) -> List[Dict]:
        """
        Generate clips from mistake list
        
        Args:
            mistakes: List of mistake dictionaries with timestamps
            clip_duration: Duration of each clip in seconds
        
        Returns:
            List of clip information dictionaries
        """
        generated_clips = []
        
        for i, mistake in enumerate(mistakes):
            timestamp = mistake.get("timestamp", 0)
            start_time = max(0, timestamp - 1.0)  # 1 second before mistake
            end_time = timestamp + clip_duration
            
            clip_id = f"mistake_{mistake.get('player', 'unknown')}_{i}"
            clip_path = self.extract_clip(start_time, end_time, clip_id, mistake)
            
            generated_clips.append({
                "id": clip_id,
                "path": clip_path,
                "start_time": start_time,
                "end_time": end_time,
                "player": mistake.get("player", "unknown"),
                "mistake_type": mistake.get("type", "unknown"),
                "description": mistake.get("description", ""),
                "suggestion": mistake.get("suggestion", "")
            })
        
        return generated_clips
    
    def close(self):
        """Release video capture"""
        if self.cap:
            self.cap.release()
    
    def save_clips_manifest(self, filename: str = "clips_manifest.json"):
        """Save manifest of all generated clips"""
        manifest_path = os.path.join(self.output_dir, filename)
        with open(manifest_path, 'w') as f:
            json.dump(self.clips, f, indent=2)
        return manifest_path
