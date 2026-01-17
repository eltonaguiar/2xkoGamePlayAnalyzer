"""
HTML5 video player generator with annotations and filters.
"""

import json
import os
from typing import List, Dict
from datetime import timedelta


class VideoPlayerGenerator:
    """Generates HTML5 video player with annotations"""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize player generator
        
        Args:
            output_dir: Output directory for HTML files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_player_html(self, clips: List[Dict], character_info: Dict, 
                           usernames: Dict, output_file: str = "video_player.html"):
        """
        Generate HTML5 video player
        
        Args:
            clips: List of clip information dictionaries
            character_info: Character images and colors
            usernames: Player usernames
            output_file: Output HTML filename
        """
        html_content = self._generate_html_template(clips, character_info, usernames)
        
        output_path = os.path.join(self.output_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _generate_html_template(self, clips: List[Dict], character_info: Dict, 
                                usernames: Dict) -> str:
        """Generate HTML template with video player"""
        
        # Organize clips by player
        player1_clips = [c for c in clips if c.get("player") == "player1"]
        player2_clips = [c for c in clips if c.get("player") == "player2"]
        
        # Get character images
        p1_image = character_info.get("player1", {}).get("image_path", "")
        p2_image = character_info.get("player2", {}).get("image_path", "")
        p1_colors = character_info.get("player1", {}).get("colors", {})
        p2_colors = character_info.get("player2", {}).get("colors", {})
        
        # Get usernames
        p1_username = usernames.get("player1", "Player 1")
        p2_username = usernames.get("player2", "Player 2")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2XKO Gameplay Analysis - Video Player</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .player-info {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        
        .player-card {{
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            min-width: 200px;
            margin: 10px;
        }}
        
        .player-card img {{
            width: 120px;
            height: 120px;
            border-radius: 10px;
            object-fit: cover;
            border: 3px solid white;
            margin-bottom: 10px;
        }}
        
        .player-card h3 {{
            font-size: 1.3em;
            margin-bottom: 5px;
        }}
        
        .color-indicator {{
            display: inline-block;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 2px solid white;
            margin: 5px;
        }}
        
        .controls {{
            padding: 20px;
            background: #f5f5f5;
            border-bottom: 2px solid #ddd;
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 12px 24px;
            font-size: 1em;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }}
        
        .filter-btn.active {{
            background: #667eea;
            color: white;
            transform: scale(1.05);
        }}
        
        .filter-btn:not(.active) {{
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }}
        
        .filter-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .video-section {{
            padding: 30px;
        }}
        
        .video-container {{
            position: relative;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            background: #000;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }}
        
        video {{
            width: 100%;
            display: block;
        }}
        
        .annotation-overlay {{
            position: absolute;
            bottom: 80px;
            left: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }}
        
        .annotation-overlay.active {{
            display: block;
        }}
        
        .annotation-title {{
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 8px;
            color: #ffd700;
        }}
        
        .annotation-text {{
            font-size: 1em;
            line-height: 1.5;
        }}
        
        .clips-list {{
            padding: 20px;
            background: #f9f9f9;
        }}
        
        .clips-list h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        
        .clip-item {{
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .clip-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}
        
        .clip-item.player1 {{
            border-left-color: #4CAF50;
        }}
        
        .clip-item.player2 {{
            border-left-color: #f44336;
        }}
        
        .clip-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        
        .clip-time {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .clip-type {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
        }}
        
        .clip-description {{
            color: #666;
            margin-top: 5px;
        }}
        
        .no-clips {{
            text-align: center;
            padding: 40px;
            color: #999;
        }}
        
        @media (max-width: 768px) {{
            .player-info {{
                flex-direction: column;
            }}
            
            .filter-buttons {{
                flex-direction: column;
            }}
            
            .filter-btn {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 2XKO Gameplay Analysis</h1>
            <p>Review mistakes and improve your gameplay</p>
            
            <div class="player-info">
                <div class="player-card">
                    <img src="{p1_image if p1_image else 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgZmlsbD0iIzRjYWY1MCIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+UDwvdGV4dD48L3N2Zz4='}" alt="Player 1">
                    <h3>{p1_username}</h3>
                    <div>
                        <span class="color-indicator" style="background: rgb({p1_colors.get('primary', (76, 175, 80))[0]}, {p1_colors.get('primary', (76, 175, 80))[1]}, {p1_colors.get('primary', (76, 175, 80))[2]})"></span>
                    </div>
                </div>
                
                <div class="player-card">
                    <img src="{p2_image if p2_image else 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgZmlsbD0iI2Y0NDM2NiIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+UDwvdGV4dD48L3N2Zz4='}" alt="Player 2">
                    <h3>{p2_username}</h3>
                    <div>
                        <span class="color-indicator" style="background: rgb({p2_colors.get('primary', (244, 67, 54))[0]}, {p2_colors.get('primary', (244, 67, 54))[1]}, {p2_colors.get('primary', (244, 67, 54))[2]})"></span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterClips('all')">All Mistakes</button>
                <button class="filter-btn" onclick="filterClips('player1')">Player 1 Mistakes</button>
                <button class="filter-btn" onclick="filterClips('player2')">Player 2 Mistakes</button>
            </div>
        </div>
        
        <div class="video-section">
            <div class="video-container">
                <video id="videoPlayer" controls>
                    <source id="videoSource" src="" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <div class="annotation-overlay" id="annotationOverlay">
                    <div class="annotation-title" id="annotationTitle"></div>
                    <div class="annotation-text" id="annotationText"></div>
                </div>
            </div>
        </div>
        
        <div class="clips-list">
            <h2>Mistake Clips</h2>
            <div id="clipsContainer">
                {self._generate_clips_html(clips)}
            </div>
        </div>
    </div>
    
    <script>
        const clips = {json.dumps(clips)};
        let currentFilter = 'all';
        let currentClipIndex = -1;
        
        function formatTimestamp(seconds) {{
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hours > 0) {{
                return `${{hours.toString().padStart(2, '0')}}:${{minutes.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }} else {{
                return `${{minutes.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }}
        }}
        
        function filterClips(filter) {{
            currentFilter = filter;
            
            // Update button states
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Filter clips
            const filteredClips = filter === 'all' 
                ? clips 
                : clips.filter(c => c.player === filter);
            
            // Update clips list
            const container = document.getElementById('clipsContainer');
            if (filteredClips.length === 0) {{
                container.innerHTML = '<div class="no-clips">No clips found for this filter.</div>';
            }} else {{
                container.innerHTML = filteredClips.map((clip, index) => {{
                    const timestamp = formatTimestamp(clip.start_time);
                    return `
                        <div class="clip-item ${{clip.player}}" onclick="playClip(${{index}}, '${{filter}}')">
                            <div class="clip-header">
                                <span class="clip-time">${{timestamp}}</span>
                                <span class="clip-type">${{clip.mistake_type}}</span>
                            </div>
                            <div class="clip-description">${{clip.description}}</div>
                            ${{clip.suggestion ? `<div class="clip-description" style="margin-top: 5px; font-style: italic;">💡 ${{clip.suggestion}}</div>` : ''}}
                        </div>
                    `;
                }}).join('');
            }}
        }}
        
        function playClip(index, filter) {{
            const filteredClips = filter === 'all' 
                ? clips 
                : clips.filter(c => c.player === filter);
            
            if (index < 0 || index >= filteredClips.length) return;
            
            const clip = filteredClips[index];
            const video = document.getElementById('videoPlayer');
            const source = document.getElementById('videoSource');
            const overlay = document.getElementById('annotationOverlay');
            const title = document.getElementById('annotationTitle');
            const text = document.getElementById('annotationText');
            
            // Set video source (use relative path)
            const videoPath = clip.path.startsWith('http') ? clip.path : 
                             (clip.path.startsWith('/') ? clip.path : 'clips/' + clip.path.split('/').pop());
            source.src = videoPath;
            video.load();
            
            // Try to play, handle autoplay restrictions
            video.play().catch(e => {{
                console.log('Autoplay prevented:', e);
            }});
            
            // Show annotation
            const playerName = clip.player === 'player1' ? '{p1_username}' : '{p2_username}';
            title.textContent = `${{playerName}} - ${{clip.mistake_type}}`;
            text.innerHTML = `
                <strong>Description:</strong> ${{clip.description}}<br>
                ${{clip.suggestion ? `<strong>Suggestion:</strong> ${{clip.suggestion}}` : ''}}
            `;
            overlay.classList.add('active');
            
            // Hide annotation after 5 seconds
            setTimeout(() => {{
                overlay.classList.remove('active');
            }}, 5000);
            
            currentClipIndex = index;
        }}
        
        // Initialize with all clips
        filterClips('all');
    </script>
</body>
</html>
"""
        return html
    
    def _generate_clips_html(self, clips: List[Dict]) -> str:
        """Generate HTML for clips list"""
        if not clips:
            return '<div class="no-clips">No mistake clips available.</div>'
        
        html_parts = []
        for i, clip in enumerate(clips):
            timestamp = self._format_timestamp(clip.get("start_time", 0))
            player = clip.get("player", "unknown")
            mistake_type = clip.get("mistake_type", "mistake")
            description = clip.get("description", "")
            suggestion = clip.get("suggestion", "")
            
            html_parts.append(f"""
                <div class="clip-item {player}" onclick="playClip({i}, currentFilter)">
                    <div class="clip-header">
                        <span class="clip-time">{timestamp}</span>
                        <span class="clip-type">{mistake_type}</span>
                    </div>
                    <div class="clip-description">{description}</div>
                    {f'<div class="clip-description" style="margin-top: 5px; font-style: italic;">💡 {suggestion}</div>' if suggestion else ''}
                </div>
            """)
        
        return "".join(html_parts)
    
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
