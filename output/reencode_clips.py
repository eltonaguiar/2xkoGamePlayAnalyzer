"""
Re-encode video clips to H.264 for browser compatibility.
This fixes videos that were encoded with mp4v codec.
"""
import os
import subprocess
import sys

def reencode_video(input_path, output_path):
    """Re-encode a video to H.264 using ffmpeg"""
    try:
        # Use ffmpeg to re-encode to H.264
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264',  # H.264 video codec
            '-c:a', 'aac',      # AAC audio codec
            '-preset', 'medium', # Encoding speed/quality balance
            '-crf', '23',       # Quality (18-28, lower is better quality)
            '-movflags', '+faststart',  # Enable web streaming
            '-y',               # Overwrite output file
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Re-encoded: {os.path.basename(input_path)}")
            return True
        else:
            print(f"✗ Failed to re-encode {os.path.basename(input_path)}: {result.stderr}")
            return False
    except FileNotFoundError:
        print("ERROR: ffmpeg not found!")
        print("Please install ffmpeg:")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        print("  Or use: winget install ffmpeg")
        print("  Or use: choco install ffmpeg")
        return False
    except Exception as e:
        print(f"✗ Error re-encoding {os.path.basename(input_path)}: {e}")
        return False

def main():
    clips_dir = os.path.join(os.path.dirname(__file__), 'clips')
    
    if not os.path.exists(clips_dir):
        print(f"Error: Clips directory not found: {clips_dir}")
        return
    
    video_files = [f for f in os.listdir(clips_dir) if f.endswith('.mp4')]
    
    if not video_files:
        print("No video files found in clips directory")
        return
    
    print(f"Found {len(video_files)} video file(s) to re-encode")
    print("This will create browser-compatible H.264 versions...")
    print()
    
    # Create backup directory
    backup_dir = os.path.join(clips_dir, 'backup_original')
    os.makedirs(backup_dir, exist_ok=True)
    
    success_count = 0
    for video_file in video_files:
        input_path = os.path.join(clips_dir, video_file)
        backup_path = os.path.join(backup_dir, video_file)
        output_path = os.path.join(clips_dir, video_file.replace('.mp4', '_fixed.mp4'))
        
        # Backup original
        if not os.path.exists(backup_path):
            import shutil
            shutil.copy2(input_path, backup_path)
            print(f"Backed up: {video_file}")
        
        # Re-encode
        if reencode_video(input_path, output_path):
            # Replace original with fixed version
            import shutil
            shutil.move(output_path, input_path)
            success_count += 1
    
    print()
    print(f"Re-encoded {success_count}/{len(video_files)} video(s)")
    if success_count == len(video_files):
        print("✓ All videos re-encoded successfully!")
        print("Original files backed up to: clips/backup_original/")
    else:
        print("⚠ Some videos failed to re-encode. Check errors above.")

if __name__ == '__main__':
    main()
