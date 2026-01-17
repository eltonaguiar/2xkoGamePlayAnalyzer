"""
Enhanced HTML5 video player generator with move stats, damage, and starting positions.
"""

import json
import os
from typing import List, Dict
from datetime import timedelta
from video_player_generator import VideoPlayerGenerator


class EnhancedVideoPlayerGenerator(VideoPlayerGenerator):
    """Enhanced video player generator with additional features"""
    
    def generate_player_html(self, clips: List[Dict], character_info: Dict, 
                           usernames: Dict, enhanced_data: Dict = None,
                           output_file: str = "video_player.html"):
        """
        Generate enhanced HTML5 video player
        
        Args:
            clips: List of clip information dictionaries
            character_info: Character images and colors
            usernames: Player usernames
            enhanced_data: Enhanced analysis data (move stats, damage, positions)
            output_file: Output HTML filename
        """
        html_content = self._generate_enhanced_html_template(
            clips, character_info, usernames, enhanced_data or {}
        )
        
        output_path = os.path.join(self.output_dir, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _generate_enhanced_html_template(self, clips: List[Dict], character_info: Dict, 
                                        usernames: Dict, enhanced_data: Dict) -> str:
        """Generate enhanced HTML template"""
        
        # Get character images and info
        p1_info = character_info.get("player1", {})
        p2_info = character_info.get("player2", {})
        p1_image = p1_info.get("image_path", "")
        p2_image = p2_info.get("image_path", "")
        p1_colors = p1_info.get("colors", {})
        p2_colors = p2_info.get("colors", {})
        p1_start_pos = p1_info.get("starting_position", "left")
        p2_start_pos = p2_info.get("starting_position", "right")
        
        # Get usernames
        p1_username = usernames.get("player1", "Player 1")
        p2_username = usernames.get("player2", "Player 2")
        
        # Get move statistics
        move_stats = enhanced_data.get("move_statistics", {})
        p1_moves = move_stats.get("player1", {})
        p2_moves = move_stats.get("player2", {})
        p1_total = move_stats.get("player1_total_moves", 0)
        p2_total = move_stats.get("player2_total_moves", 0)
        p1_variety = move_stats.get("player1_move_variety", 0)
        p2_variety = move_stats.get("player2_move_variety", 0)
        
        # Get starting positions
        start_positions = enhanced_data.get("starting_positions", {})
        p1_start_pos = start_positions.get("player1", p1_start_pos)
        p2_start_pos = start_positions.get("player2", p2_start_pos)
        
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
            max-width: 1600px;
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
            min-width: 250px;
            margin: 10px;
        }}
        
        .player-card img {{
            width: 150px;
            height: 150px;
            border-radius: 10px;
            object-fit: cover;
            border: 3px solid white;
            margin-bottom: 10px;
        }}
        
        .player-card h3 {{
            font-size: 1.5em;
            margin-bottom: 10px;
        }}
        
        .player-card .position-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.3);
            padding: 5px 15px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.9em;
        }}
        
        .color-indicator {{
            display: inline-block;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            border: 2px solid white;
            margin: 5px;
        }}
        
        .stats-section {{
            padding: 20px;
            background: #f9f9f9;
            border-bottom: 2px solid #ddd;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }}
        
        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .stat-card h4 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        
        .move-list {{
            max-height: 200px;
            overflow-y: auto;
        }}
        
        .move-item {{
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .move-name {{
            font-weight: bold;
            color: #333;
        }}
        
        .move-count {{
            color: #667eea;
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
            background: rgba(0,0,0,0.85);
            color: white;
            padding: 20px;
            border-radius: 8px;
            display: none;
            border-left: 4px solid #ffd700;
        }}
        
        .annotation-overlay.active {{
            display: block;
        }}
        
        .annotation-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }}
        
        .annotation-text {{
            font-size: 1em;
            line-height: 1.6;
        }}
        
        .damage-badge {{
            display: inline-block;
            background: #f44336;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.9em;
            margin-left: 10px;
        }}
        
        .damage-info {{
            background: rgba(244, 67, 54, 0.1);
            padding: 10px;
            border-radius: 6px;
            margin-top: 8px;
            border-left: 3px solid #f44336;
        }}
        
        .damage-row {{
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            font-size: 0.95em;
        }}
        
        .damage-label {{
            font-weight: bold;
            color: #666;
        }}
        
        .damage-value {{
            color: #f44336;
            font-weight: bold;
        }}
        
        .round-badge {{
            display: inline-block;
            background: #9c27b0;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-left: 10px;
        }}
        
        .leader-badge {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-left: 10px;
        }}
        
        .leader-badge.tied {{
            background: #ff9800;
        }}
        
        .replay-controls {{
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 10px;
            z-index: 10;
        }}
        
        .replay-btn {{
            background: #ffd700;
            color: #000;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 1em;
            transition: all 0.3s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}
        
        .replay-btn:hover {{
            background: #ffed4e;
            transform: scale(1.05);
        }}
        
        .replay-btn.active {{
            background: #4CAF50;
            color: white;
        }}
        
        .replay-btn.slow-mo {{
            background: #2196F3;
            color: white;
        }}
        
        .mistake-marker {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(244, 67, 54, 0.9);
            color: white;
            padding: 20px 40px;
            border-radius: 10px;
            font-size: 2em;
            font-weight: bold;
            text-align: center;
            z-index: 5;
            display: none;
            border: 4px solid white;
            box-shadow: 0 0 30px rgba(244, 67, 54, 0.8);
            animation: pulse 1s infinite;
        }}
        
        .mistake-marker.active {{
            display: block;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.9; }}
            50% {{ transform: translate(-50%, -50%) scale(1.1); opacity: 1; }}
        }}
        
        .replay-info {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-size: 0.9em;
            z-index: 10;
            display: none;
        }}
        
        .replay-info.active {{
            display: block;
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
            font-size: 1.1em;
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
        
        .player-badge {{
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-right: 10px;
        }}
        
        .player-badge.player2 {{
            background: #f44336;
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
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        .player-selector {{
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 10;
            background: rgba(0, 0, 0, 0.7);
            padding: 10px;
            border-radius: 5px;
            color: white;
            font-size: 0.9em;
        }}
        
        .player-selector select {{
            background: #333;
            color: white;
            border: 1px solid #555;
            padding: 5px 10px;
            border-radius: 3px;
            margin-left: 10px;
        }}
        
        .player-status {{
            position: absolute;
            top: 60px;
            left: 20px;
            z-index: 10;
            background: rgba(76, 175, 80, 0.9);
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 0.85em;
            display: none;
        }}
        
        .player-status.error {{
            background: rgba(244, 67, 54, 0.9);
        }}
        
        .player-status.active {{
            display: block;
        }}
        
        #videoPlayerPlyr {{
            width: 100%;
            display: none;
        }}
        
        #videoPlayerVideoJS {{
            width: 100%;
            display: none;
        }}
        
        #videoPlayerAlt {{
            width: 100%;
            display: none;
        }}
    </style>
    
    <!-- Video.js CSS -->
    <link href="https://vjs.zencdn.net/8.5.2/video-js.css" rel="stylesheet" />
    
    <!-- Plyr CSS -->
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 2XKO Gameplay Analysis</h1>
            <p>Review mistakes and improve your gameplay</p>
            
            <div class="player-info">
                <div class="player-card">
                    <img src="{p1_image if p1_image else 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgZmlsbD0iIzRjYWY1MCIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+UDwvdGV4dD48L3N2Zz4='}" alt="Player 1">
                    <h3>{p1_username}</h3>
                    <div class="position-badge">Starting: {p1_start_pos.upper()}</div>
                    <div>
                        <span class="color-indicator" style="background: rgb({p1_colors.get('primary', [76, 175, 80])[0]}, {p1_colors.get('primary', [76, 175, 80])[1]}, {p1_colors.get('primary', [76, 175, 80])[2]})"></span>
                    </div>
                </div>
                
                <div class="player-card">
                    <img src="{p2_image if p2_image else 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgZmlsbD0iI2Y0NDM2NiIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+UDwvdGV4dD48L3N2Zz4='}" alt="Player 2">
                    <h3>{p2_username}</h3>
                    <div class="position-badge">Starting: {p2_start_pos.upper()}</div>
                    <div>
                        <span class="color-indicator" style="background: rgb({p2_colors.get('primary', [244, 67, 54])[0]}, {p2_colors.get('primary', [244, 67, 54])[1]}, {p2_colors.get('primary', [244, 67, 54])[2]})"></span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="stats-section">
            <h2 style="text-align: center; color: #333; margin-bottom: 10px;">Match Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h4>{p1_username} - Move Variety</h4>
                    <p><strong>Total Moves:</strong> {p1_total}</p>
                    <p><strong>Unique Moves:</strong> {p1_variety}</p>
                    <div class="move-list">
                        {self._generate_move_list_html(p1_moves, enhanced_data.get("move_statistics", {}).get("player1_meter_usage", {}))}
                    </div>
                </div>
                
                <div class="stat-card">
                    <h4>{p2_username} - Move Variety</h4>
                    <p><strong>Total Moves:</strong> {p2_total}</p>
                    <p><strong>Unique Moves:</strong> {p2_variety}</p>
                    <div class="move-list">
                        {self._generate_move_list_html(p2_moves, enhanced_data.get("move_statistics", {}).get("player2_meter_usage", {}))}
                    </div>
                </div>
                
                {self._generate_damage_summary_html(enhanced_data, p1_username, p2_username)}
            </div>
        </div>
        
        <div class="controls">
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterClips('all')">All Mistakes</button>
                <button class="filter-btn" onclick="filterClips('player1')">{p1_username} Mistakes</button>
                <button class="filter-btn" onclick="filterClips('player2')">{p2_username} Mistakes</button>
            </div>
        </div>
        
        <div class="video-section">
            <div class="video-container">
                <div class="player-selector">
                    <label>Player Method:</label>
                    <select id="playerMethod" onchange="switchPlayerMethod()">
                        <option value="native">Method 1: Native HTML5</option>
                        <option value="plyr">Method 2: Plyr Player</option>
                        <option value="videojs">Method 3: Video.js</option>
                        <option value="alt">Method 4: Alternative HTML5</option>
                    </select>
                </div>
                <div class="player-status" id="playerStatus"></div>
                
                <!-- Method 1: Native HTML5 -->
                <video id="videoPlayer" controls style="display: block;">
                    <source id="videoSource" src="" type="video/mp4">
                    <source id="videoSourceWebm" src="" type="video/webm">
                    Your browser does not support the video tag.
                </video>
                
                <!-- Method 2: Plyr Player -->
                <video id="videoPlayerPlyr" controls style="display: none;">
                    <source id="videoSourcePlyr" src="" type="video/mp4">
                </video>
                
                <!-- Method 3: Video.js -->
                <video id="videoPlayerVideoJS" class="video-js vjs-default-skin" controls preload="auto" data-setup="{{{{}}}}" style="display: none;">
                    <source id="videoSourceVideoJS" src="" type="video/mp4">
                    <p class="vjs-no-js">
                        To view this video please enable JavaScript, and consider upgrading to a web browser that
                        <a href="https://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>.
                    </p>
                </video>
                
                <!-- Method 4: Alternative HTML5 with multiple sources -->
                <video id="videoPlayerAlt" controls style="display: none;">
                    <source id="videoSourceAlt1" src="" type="video/mp4">
                    <source id="videoSourceAlt2" src="" type="video/webm">
                    <source id="videoSourceAlt3" src="" type="video/ogg">
                    Your browser does not support the video tag.
                </video>
                
                <div class="replay-controls">
                    <button class="replay-btn" id="replayBtn" onclick="toggleReplay()" title="Toggle Instant Replay">
                        🔄 Instant Replay
                    </button>
                    <button class="replay-btn slow-mo" id="slowMoBtn" onclick="toggleSlowMotion()" title="Toggle Slow Motion">
                        ⏱️ Slow Motion
                    </button>
                </div>
                <div class="mistake-marker" id="mistakeMarker">
                    ⚠️ MISTAKE MOMENT ⚠️
                </div>
                <div class="replay-info" id="replayInfo">
                    Replay: <span id="replayCount">0</span> times
                </div>
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
    
    <!-- Video.js JS -->
    <script src="https://vjs.zencdn.net/8.5.2/video.min.js"></script>
    
    <!-- Plyr JS -->
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    
    <script>
        const clips = {json.dumps(clips)};
        let currentFilter = 'all';
        let currentClipIndex = -1;
        let isReplayMode = false;
        let isSlowMotion = false;
        let replayCount = 0;
        let mistakeTimestamp = 0; // Timestamp of the mistake moment in the clip
        let replayInterval = null;
        let currentPlayerMethod = 'native';
        let currentPlayer = null;
        let plyrInstance = null;
        let videojsInstance = null;
        
        // Initialize players
        document.addEventListener('DOMContentLoaded', function() {{
            // Try to initialize Plyr
            try {{
                const plyrVideo = document.getElementById('videoPlayerPlyr');
                if (plyrVideo) {{
                    plyrInstance = new Plyr(plyrVideo, {{
                        controls: ['play', 'progress', 'current-time', 'mute', 'volume', 'fullscreen'],
                        settings: ['speed']
                    }});
                }}
            }} catch (e) {{
                console.log('Plyr initialization failed:', e);
            }}
            
            // Try to initialize Video.js
            try {{
                const videojsElement = document.getElementById('videoPlayerVideoJS');
                if (videojsElement && typeof videojs !== 'undefined') {{
                    videojsInstance = videojs(videojsElement, {{
                        controls: true,
                        fluid: true
                    }});
                }}
            }} catch (e) {{
                console.log('Video.js initialization failed:', e);
            }}
            
            // Set default player
            switchPlayerMethod('native');
        }});
        
        function switchPlayerMethod(method = null) {{
            const selector = document.getElementById('playerMethod');
            const methodToUse = method || selector.value;
            const statusDiv = document.getElementById('playerStatus');
            
            // Hide all players
            document.getElementById('videoPlayer').style.display = 'none';
            document.getElementById('videoPlayerPlyr').style.display = 'none';
            document.getElementById('videoPlayerVideoJS').style.display = 'none';
            document.getElementById('videoPlayerAlt').style.display = 'none';
            
            // Stop current player
            if (currentPlayer) {{
                try {{
                    currentPlayer.pause();
                }} catch (e) {{
                    console.log('Error pausing player:', e);
                }}
            }}
            
            currentPlayerMethod = methodToUse;
            selector.value = methodToUse;
            
            // Show selected player
            let playerElement = null;
            let playerName = '';
            
            switch (methodToUse) {{
                case 'native':
                    playerElement = document.getElementById('videoPlayer');
                    playerName = 'Native HTML5';
                    break;
                case 'plyr':
                    playerElement = document.getElementById('videoPlayerPlyr');
                    playerName = 'Plyr Player';
                    break;
                case 'videojs':
                    playerElement = document.getElementById('videoPlayerVideoJS');
                    playerName = 'Video.js';
                    break;
                case 'alt':
                    playerElement = document.getElementById('videoPlayerAlt');
                    playerName = 'Alternative HTML5';
                    break;
            }}
            
            if (playerElement) {{
                playerElement.style.display = 'block';
                currentPlayer = playerElement;
                
                // Update status
                statusDiv.textContent = `Using: ${{playerName}}`;
                statusDiv.className = 'player-status active';
                
                // Try to load current clip if one is selected
                if (currentClipIndex >= 0) {{
                    loadVideoInCurrentPlayer();
                }}
            }}
        }}
        
        function loadVideoInCurrentPlayer() {{
            const filteredClips = currentFilter === 'all' 
                ? clips 
                : clips.filter(c => c.player === currentFilter);
            
            if (currentClipIndex < 0 || currentClipIndex >= filteredClips.length) return;
            
            const clip = filteredClips[currentClipIndex];
            const videoPath = clip.path.startsWith('http') ? clip.path : 
                             (clip.path.startsWith('/') ? clip.path : 'clips/' + clip.path.split(/[/\\\\]/).pop());
            
            let sourceElement = null;
            let playerElement = null;
            
            switch (currentPlayerMethod) {{
                case 'native':
                    playerElement = document.getElementById('videoPlayer');
                    sourceElement = document.getElementById('videoSource');
                    if (sourceElement) sourceElement.src = videoPath;
                    break;
                case 'plyr':
                    playerElement = document.getElementById('videoPlayerPlyr');
                    sourceElement = document.getElementById('videoSourcePlyr');
                    if (sourceElement) sourceElement.src = videoPath;
                    if (plyrInstance) {{
                        const plyrSource = {{
                            type: 'video',
                            sources: [{{
                                src: videoPath,
                                type: 'video/mp4'
                            }}]
                        }};
                        plyrInstance.source = plyrSource;
                    }}
                    break;
                case 'videojs':
                    playerElement = document.getElementById('videoPlayerVideoJS');
                    sourceElement = document.getElementById('videoSourceVideoJS');
                    if (sourceElement) sourceElement.src = videoPath;
                    if (videojsInstance) {{
                        videojsInstance.src({{ type: 'video/mp4', src: videoPath }});
                    }}
                    break;
                case 'alt':
                    playerElement = document.getElementById('videoPlayerAlt');
                    sourceElement = document.getElementById('videoSourceAlt1');
                    if (sourceElement) sourceElement.src = videoPath;
                    break;
            }}
            
            if (playerElement) {{
                playerElement.load();
                currentPlayer = playerElement;
                
                // Set up error handling with fallback
                playerElement.addEventListener('error', function(e) {{
                    console.log(`Player method ${{currentPlayerMethod}} failed, trying fallback...`);
                    tryNextPlayerMethod();
                }}, {{ once: true }});
            }}
        }}
        
        function tryNextPlayerMethod() {{
            const methods = ['native', 'plyr', 'videojs', 'alt'];
            const currentIndex = methods.indexOf(currentPlayerMethod);
            const nextIndex = (currentIndex + 1) % methods.length;
            
            if (nextIndex !== currentIndex) {{
                const statusDiv = document.getElementById('playerStatus');
                statusDiv.textContent = `Method ${{currentPlayerMethod}} failed, switching to ${{methods[nextIndex]}}...`;
                statusDiv.className = 'player-status active error';
                
                setTimeout(() => {{
                    switchPlayerMethod(methods[nextIndex]);
                    if (currentClipIndex >= 0) {{
                        loadVideoInCurrentPlayer();
                    }}
                }}, 500);
            }} else {{
                const statusDiv = document.getElementById('playerStatus');
                statusDiv.textContent = 'All playback methods failed. Please check video file.';
                statusDiv.className = 'player-status active error';
            }}
        }}
        
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
                    const playerName = clip.player === 'player1' ? '{p1_username}' : '{p2_username}';
                    const playerClass = clip.player;
                    const round = clip.round || 1;
                    const leader = clip.leader || 'tied';
                    const leaderName = leader === 'player1' ? '{p1_username}' : (leader === 'player2' ? '{p2_username}' : 'Tied');
                    const leaderClass = leader === 'tied' ? 'tied' : '';
                    
                    // Damage info
                    const damageDealt = clip.damage_dealt || 0;
                    const damageTaken = clip.damage_taken || 0;
                    const damageInfo = damageDealt > 0 || damageTaken > 0 ? `
                        <div class="damage-info">
                            <div class="damage-row">
                                <span class="damage-label">Damage Dealt:</span>
                                <span class="damage-value">${{damageDealt}}</span>
                            </div>
                            <div class="damage-row">
                                <span class="damage-label">Damage Taken:</span>
                                <span class="damage-value">${{damageTaken}}</span>
                            </div>
                            <div class="damage-row">
                                <span class="damage-label">Net Damage:</span>
                                <span class="damage-value">${{damageDealt - damageTaken}}</span>
                            </div>
                        </div>
                    ` : '';
                    
                    return `
                        <div class="clip-item ${{playerClass}}" onclick="playClip(${{index}}, '${{filter}}')">
                            <div class="clip-header">
                                <div>
                                    <span class="player-badge ${{playerClass}}">${{playerName}}</span>
                                    <span class="clip-time">${{timestamp}}</span>
                                    <span class="round-badge">Round ${{round}}</span>
                                    <span class="leader-badge ${{leaderClass}}">${{leaderName}} Leading</span>
                                    <button class="replay-btn" style="padding: 5px 10px; font-size: 0.8em; margin-left: 10px;" onclick="event.stopPropagation(); playClip(${{index}}, '${{filter}}'); setTimeout(() => toggleReplay(), 500);" title="Play with Instant Replay">
                                        🔄 Replay
                                    </button>
                                </div>
                                <span class="clip-type">${{clip.mistake_type}}</span>
                            </div>
                    <div class="clip-description"><strong>${{clip.description_plain || clip.description}}</strong></div>
                    ${{clip.opponent_response_description ? `<div class="clip-description" style="margin-top: 5px; color: #2196F3; font-weight: bold;">⚔️ ${{clip.opponent_response_description}}</div>` : ''}}
                    ${{damageInfo}}
                    ${{clip.suggestion ? `<div class="clip-description" style="margin-top: 5px; font-style: italic;">💡 ${{clip.suggestion}}</div>` : ''}}
                    ${{clip.range_suggestion ? `<div class="clip-description" style="margin-top: 5px; color: #f44336;">📏 Range: ${{clip.range_suggestion}}</div>` : ''}}
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
            const overlay = document.getElementById('annotationOverlay');
            const title = document.getElementById('annotationTitle');
            const text = document.getElementById('annotationText');
            
            currentClipIndex = index;
            currentFilter = filter;
            
            // Load video in current player method
            loadVideoInCurrentPlayer();
            
            // Get the current player element
            let video = currentPlayer;
            if (!video) {{
                video = document.getElementById('videoPlayer');
                currentPlayer = video;
            }}
            
            // Reset replay state
            isReplayMode = false;
            isSlowMotion = false;
            replayCount = 0;
            updateReplayButton();
            updateSlowMoButton();
            document.getElementById('replayInfo').classList.remove('active');
            document.getElementById('mistakeMarker').classList.remove('active');
            
            // Calculate mistake timestamp in the clip
            // Clips start 1 second before mistake, so mistake is at ~1 second into clip
            // But we can also use the actual mistake timestamp if available
            if (clip.timestamp && clip.start_time) {{
                mistakeTimestamp = clip.timestamp - clip.start_time;
            }} else {{
                // Default: mistake happens around 1 second into the clip
                mistakeTimestamp = 1.0;
            }}
            
            // Try to play
            video.play().catch(e => {{
                console.log('Autoplay prevented:', e);
            }});
            
            // Set up video event listeners for replay
            setupReplayListeners();
            
            // Show annotation with comprehensive damage info
            const playerName = clip.player === 'player1' ? '{p1_username}' : '{p2_username}';
            const round = clip.round || 1;
            const leader = clip.leader || 'tied';
            const leaderName = leader === 'player1' ? '{p1_username}' : (leader === 'player2' ? '{p2_username}' : 'Tied');
            
            const damageDealt = clip.damage_dealt || 0;
            const damageTaken = clip.damage_taken || 0;
            const netDamage = damageDealt - damageTaken;
            
            title.innerHTML = `${{playerName}} - ${{clip.mistake_type}} | Round ${{round}}`;
            
            let damageText = '';
            if (damageDealt > 0 || damageTaken > 0) {{
                damageText = `
                    <div style="margin-top: 10px; padding: 10px; background: rgba(244, 67, 54, 0.2); border-radius: 5px;">
                        <strong>Damage at End of Mistake:</strong><br>
                        • ${{playerName}} Dealt: <span style="color: #4CAF50;">${{damageDealt}}</span><br>
                        • ${{playerName}} Taken: <span style="color: #f44336;">${{damageTaken}}</span><br>
                        • Net: <span style="color: ${{netDamage >= 0 ? '#4CAF50' : '#f44336'}};">${{netDamage >= 0 ? '+' : ''}}${{netDamage}}</span><br>
                        • Leader: <span style="color: #ffd700;">${{leaderName}}</span>
                    </div>
                `;
            }}
            
            const description = clip.contextual_description || clip.description_plain || clip.description;
            const opponentResponse = clip.opponent_response_description || '';
            
            text.innerHTML = `
                <strong>What Happened:</strong> ${{description}}<br>
                ${{opponentResponse ? `<strong style="color: #2196F3;">Opponent's Response:</strong> ${{opponentResponse}}<br>` : ''}}
                ${{damageText}}
                ${{clip.suggestion ? `<strong>Suggestion:</strong> ${{clip.suggestion}}<br>` : ''}}
                ${{clip.range_suggestion ? `<strong>Range:</strong> ${{clip.range_suggestion}}<br>` : ''}}
                <div style="margin-top: 15px; padding: 10px; background: rgba(255, 215, 0, 0.2); border-radius: 5px; border-left: 3px solid #ffd700;">
                    <strong>💡 Tip:</strong> Click "Instant Replay" to automatically loop this mistake. Use "Slow Motion" to see it in detail.
                </div>
            `;
            overlay.classList.add('active');
            
            // Hide annotation after 7 seconds
            setTimeout(() => {{
                overlay.classList.remove('active');
            }}, 7000);
            
            currentClipIndex = index;
        }}
        
        // Initialize with all clips
        filterClips('all');
    </script>
</body>
</html>
"""
        return html
    
    def _generate_move_list_html(self, moves: Dict, meter_usage: Dict = None) -> str:
        """Generate HTML for move list with plain English names and meter indicators"""
        if not moves:
            return "<p style='color: #999;'>No moves detected</p>"
        
        from move_translator import MoveTranslator
        
        if meter_usage is None:
            meter_usage = {}
        
        # Sort by count
        sorted_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)
        
        html_parts = []
        for move_name, count in sorted_moves:
            move_plain = MoveTranslator.translate_move(move_name)
            meter_count = meter_usage.get(move_name, 0)
            meter_indicator = ""
            if meter_count > 0:
                meter_indicator = f' <span style="color: #ffd700; font-weight: bold;" title="Used meter {meter_count} times">⚡{meter_count}</span>'
            
            html_parts.append(f"""
                <div class="move-item">
                    <span class="move-name">{move_plain}</span>
                    <span style="color: #999; font-size: 0.85em;">({move_name})</span>
                    {meter_indicator}
                    <span class="move-count">{count}x</span>
                </div>
            """)
        
        return "".join(html_parts)
    
    def _generate_damage_summary_html(self, enhanced_data: Dict, p1_username: str, p2_username: str) -> str:
        """Generate damage summary HTML"""
        damage_history = enhanced_data.get("damage_history", {})
        p1_history = damage_history.get("player1", [])
        p2_history = damage_history.get("player2", [])
        
        # Get final damage stats
        p1_final = p1_history[-1] if p1_history else (0, 0, 0, 1)
        p2_final = p2_history[-1] if p2_history else (0, 0, 0, 1)
        
        p1_dealt = p1_final[1] if len(p1_final) > 1 else 0
        p1_taken = p1_final[2] if len(p1_final) > 2 else 0
        p2_dealt = p2_final[1] if len(p2_final) > 1 else 0
        p2_taken = p2_final[2] if len(p2_final) > 2 else 0
        
        p1_net = p1_dealt - p1_taken
        p2_net = p2_dealt - p2_taken
        
        # Determine overall leader
        if p1_net > p2_net:
            leader = p1_username
            leader_color = "#4CAF50"
            leader_rgba = "rgba(76, 175, 80, 0.1)"
        elif p2_net > p1_net:
            leader = p2_username
            leader_color = "#f44336"
            leader_rgba = "rgba(244, 67, 54, 0.1)"
        else:
            leader = "Tied"
            leader_color = "#ff9800"
            leader_rgba = "rgba(255, 152, 0, 0.1)"
        
        return f"""
                <div class="stat-card">
                    <h4>Overall Damage Summary</h4>
                    <div style="margin-bottom: 15px;">
                        <div style="text-align: center; padding: 10px; background: {leader_rgba}; border-radius: 5px; margin-bottom: 10px;">
                            <strong style="color: {leader_color};">Current Leader: {leader}</strong>
                        </div>
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>{p1_username}:</strong>
                        <div style="margin-left: 15px; margin-top: 5px;">
                            <div>Dealt: <span style="color: #4CAF50;">{p1_dealt}</span></div>
                            <div>Taken: <span style="color: #f44336;">{p1_taken}</span></div>
                            <div>Net: <span style="color: {'#4CAF50' if p1_net >= 0 else '#f44336'}; font-weight: bold;">{p1_net:+d}</span></div>
                        </div>
                    </div>
                    <div>
                        <strong>{p2_username}:</strong>
                        <div style="margin-left: 15px; margin-top: 5px;">
                            <div>Dealt: <span style="color: #4CAF50;">{p2_dealt}</span></div>
                            <div>Taken: <span style="color: #f44336;">{p2_taken}</span></div>
                            <div>Net: <span style="color: {'#4CAF50' if p2_net >= 0 else '#f44336'}; font-weight: bold;">{p2_net:+d}</span></div>
                        </div>
                    </div>
                </div>
        """
    
    def _generate_clips_html(self, clips: List[Dict]) -> str:
        """Generate HTML for clips list with enhanced info"""
        if not clips:
            return '<div class="no-clips">No mistake clips available.</div>'
        
        html_parts = []
        for i, clip in enumerate(clips):
            timestamp = self._format_timestamp(clip.get("start_time", 0))
            player = clip.get("player", "unknown")
            player_name = clip.get("player_name", f"Player {player[-1]}")
            mistake_type = clip.get("mistake_type", "mistake")
            description = clip.get("description", "")
            suggestion = clip.get("suggestion", "")
            range_suggestion = clip.get("range_suggestion", "")
            estimated_damage = clip.get("estimated_damage", 0)
            
            # Get damage info
            damage_dealt = clip.get("damage_dealt", 0)
            damage_taken = clip.get("damage_taken", 0)
            round_num = clip.get("round", 1)
            leader = clip.get("leader", "tied")
            leader_name = "Player 1" if leader == "player1" else ("Player 2" if leader == "player2" else "Tied")
            leader_class = "tied" if leader == "tied" else ""
            
            # Get plain English description (prefer contextual if available)
            description_plain = clip.get("contextual_description") or clip.get("description_plain", description)
            opponent_response = clip.get("opponent_response_description", "")
            
            # Damage info HTML
            damage_info_html = ""
            if damage_dealt > 0 or damage_taken > 0:
                damage_info_html = f"""
                    <div class="damage-info">
                        <div class="damage-row">
                            <span class="damage-label">Damage Dealt:</span>
                            <span class="damage-value">{damage_dealt}</span>
                        </div>
                        <div class="damage-row">
                            <span class="damage-label">Damage Taken:</span>
                            <span class="damage-value">{damage_taken}</span>
                        </div>
                        <div class="damage-row">
                            <span class="damage-label">Net Damage:</span>
                            <span class="damage-value">{damage_dealt - damage_taken}</span>
                        </div>
                    </div>
                """
            
            html_parts.append(f"""
                <div class="clip-item {player}" onclick="playClip({i}, currentFilter)">
                    <div class="clip-header">
                        <div>
                            <span class="player-badge {player}">{player_name}</span>
                            <span class="clip-time">{timestamp}</span>
                            <span class="round-badge">Round {round_num}</span>
                            <span class="leader-badge {leader_class}">{leader_name} Leading</span>
                            <button class="replay-btn" style="padding: 5px 10px; font-size: 0.8em; margin-left: 10px;" onclick="event.stopPropagation(); playClip({i}, currentFilter); setTimeout(() => toggleReplay(), 500);" title="Play with Instant Replay">
                                🔄 Replay
                            </button>
                        </div>
                        <span class="clip-type">{mistake_type}</span>
                    </div>
                    <div class="clip-description"><strong>{description_plain}</strong></div>
                    {f'<div class="clip-description" style="margin-top: 5px; color: #2196F3; font-weight: bold;">⚔️ {opponent_response}</div>' if opponent_response else ''}
                    {damage_info_html}
                    {f'<div class="clip-description" style="margin-top: 5px; font-style: italic;">💡 {suggestion}</div>' if suggestion else ''}
                    {f'<div class="clip-description" style="margin-top: 5px; color: #f44336;">📏 Range: {range_suggestion}</div>' if range_suggestion else ''}
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
