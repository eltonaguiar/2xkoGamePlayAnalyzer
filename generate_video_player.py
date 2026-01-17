"""
Main script to generate HTML5 video player with annotated clips.
"""

import sys
import json
import os
from analyzer import GameplayAnalyzer
from enhanced_analyzer import EnhancedAnalyzer
from clip_generator import ClipGenerator
from character_identifier import CharacterIdentifier
from enhanced_character_identifier import EnhancedCharacterIdentifier
from video_player_generator import VideoPlayerGenerator
from enhanced_video_player_generator import EnhancedVideoPlayerGenerator


def main():
    """Generate video player with annotated clips"""
    if len(sys.argv) < 2:
        print("Usage: python generate_video_player.py <video_path>")
        print("Example: python generate_video_player.py \"C:\\Users\\zerou\\Desktop\\video.mp4\"")
        sys.exit(1)
    
    video_path = sys.argv[1]
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        sys.exit(1)
    
    print("="*80)
    print("2XKO Video Player Generator")
    print("="*80)
    print(f"\nVideo: {video_path}")
    
    # Step 1: Analyze gameplay with enhanced analyzer
    print("\n[1/6] Analyzing gameplay with enhanced features...")
    analyzer = EnhancedAnalyzer(video_path, "mirror", "Blitzcrank")
    report = analyzer.analyze()
    enhanced_data = report.get("enhanced_data", {})
    analyzer.close()
    
    # Step 2: Identify characters with starting positions
    print("\n[2/6] Identifying characters and starting positions...")
    identifier = EnhancedCharacterIdentifier(video_path)
    
    # Get character info at start of round
    start_character_info = identifier.identify_characters_at_start()
    
    # Extract character images
    character_images = identifier.extract_character_images(num_samples=10)
    
    # Build character info with starting positions
    character_info = {}
    for player in ["player1", "player2"]:
        start_info = start_character_info.get(player, {})
        char_img = character_images.get(player)
        start_img = start_info.get("image")
        
        # Use character image if available, otherwise use start image
        final_img = char_img if char_img is not None else start_img
        
        if char_img is not None:
            colors = identifier.detect_character_colors(char_img)
        else:
            colors = start_info.get("colors", {})
        
        character_info[player] = {
            "image": final_img,
            "colors": colors,
            "starting_position": start_info.get("starting_position") or enhanced_data.get("starting_positions", {}).get(player, "left" if player == "player1" else "right")
        }
    
    # Extract usernames with improved method
    usernames = identifier.extract_usernames(num_samples=10)  # Sample more frames
    # Fallback to default names if extraction fails
    if not usernames.get('player1'):
        usernames['player1'] = "Player 1"
    if not usernames.get('player2'):
        usernames['player2'] = "Player 2"
    print(f"  Player 1: {usernames.get('player1', 'Player 1')} (Starting: {character_info['player1']['starting_position']})")
    print(f"  Player 2: {usernames.get('player2', 'Player 2')} (Starting: {character_info['player2']['starting_position']})")
    
    # Save character images
    char_images_dir = os.path.join("output", "character_images")
    os.makedirs(char_images_dir, exist_ok=True)
    saved_paths = identifier.save_character_images(character_images, char_images_dir)
    for player, path in saved_paths.items():
        # Use relative path for web
        rel_path = os.path.relpath(path, "output") if "output" in os.getcwd() else f"character_images/{os.path.basename(path)}"
        character_info[player]["image_path"] = rel_path
    
    identifier.close()
    
    # Step 3: Enhance mistakes with additional data
    print("\n[3/6] Enhancing mistakes with damage and range info...")
    all_mistakes = []
    all_mistakes.extend(report["player1_analysis"]["mistakes"])
    all_mistakes.extend(report["player2_analysis"]["mistakes"])
    
    if not all_mistakes:
        print("  No mistakes found. Creating sample clips from key events...")
        # Use key events if no mistakes
        for event in report["key_events"]:
            if event.get("type") in ["unsafe_move", "unsafe_special"]:
                mistake = {
                    "timestamp": event.get("timestamp", 0),
                    "player": event.get("player", "unknown"),
                    "type": event.get("type", "mistake"),
                    "move": event.get("move", ""),
                    "description": event.get("description", ""),
                    "suggestion": "Review this moment for improvement"
                }
                
                # Add enhanced data
                if mistake["player"] == "player1":
                    mistake["player_name"] = usernames.get("player1", "Player 1")
                    # Get damage at mistake end time
                    mistake_end = mistake["timestamp"] + 5.0
                    p1_info = enhanced_data.get("damage_history", {}).get("player1", [])
                    if p1_info:
                        for entry in reversed(p1_info):
                            if len(entry) >= 4 and entry[0] <= mistake_end:
                                mistake["damage_dealt"] = entry[1]
                                mistake["damage_taken"] = entry[2]
                                mistake["round"] = entry[3]
                                break
                    
                    # Get opponent moves during window
                    mistake_end = mistake["timestamp"] + 5.0
                    opponent_timestamps = enhanced_data.get("move_timestamps", {}).get("player2", [])
                    opponent_moves = []
                    for ts, move in opponent_timestamps:
                        if mistake["timestamp"] <= ts <= mistake_end:
                            opponent_moves.append(move)
                    
                    mistake["opponent_response"] = opponent_moves
                    mistake["opponent_response_description"] = MoveTranslator.describe_mistake_context(
                        mistake.get("move", ""), opponent_moves
                    )
                    mistake["move_plain"] = MoveTranslator.translate_move(mistake.get("move", ""))
                    mistake["description_plain"] = f"{mistake['player_name']} used {mistake['move_plain']}, which left them vulnerable"
                    mistake["contextual_description"] = f"{mistake['player_name']} used {mistake['move_plain']}" + (
                        f", then opponent responded with {', then '.join([MoveTranslator.translate_move(m) for m in opponent_moves])}" 
                        if opponent_moves else ""
                    )
                else:
                    mistake["player_name"] = usernames.get("player2", "Player 2")
                    mistake_end = mistake["timestamp"] + 5.0
                    p2_info = enhanced_data.get("damage_history", {}).get("player2", [])
                    if p2_info:
                        for entry in reversed(p2_info):
                            if len(entry) >= 4 and entry[0] <= mistake_end:
                                mistake["damage_dealt"] = entry[1]
                                mistake["damage_taken"] = entry[2]
                                mistake["round"] = entry[3]
                                break
                    
                    # Get opponent moves during window
                    mistake_end = mistake["timestamp"] + 5.0
                    opponent_timestamps = enhanced_data.get("move_timestamps", {}).get("player1", [])
                    opponent_moves = []
                    for ts, move in opponent_timestamps:
                        if mistake["timestamp"] <= ts <= mistake_end:
                            opponent_moves.append(move)
                    
                    mistake["opponent_response"] = opponent_moves
                    mistake["opponent_response_description"] = MoveTranslator.describe_mistake_context(
                        mistake.get("move", ""), opponent_moves
                    )
                    mistake["move_plain"] = MoveTranslator.translate_move(mistake.get("move", ""))
                    mistake["description_plain"] = f"{mistake['player_name']} used {mistake['move_plain']}, which left them vulnerable"
                    mistake["contextual_description"] = f"{mistake['player_name']} used {mistake['move_plain']}" + (
                        f", then opponent responded with {', then '.join([MoveTranslator.translate_move(m) for m in opponent_moves])}" 
                        if opponent_moves else ""
                    )
                
                all_mistakes.append(mistake)
    
    # Step 4: Generate clips
    print("\n[4/6] Generating mistake clips...")
    clips_dir = os.path.join("output", "clips")
    os.makedirs(clips_dir, exist_ok=True)
    clip_gen = ClipGenerator(video_path, clips_dir)
    
    if all_mistakes:
        clips = clip_gen.generate_clips_from_mistakes(all_mistakes, clip_duration=5.0)
        # Update paths and add enhanced data
        for clip in clips:
            if "path" in clip:
                # Make path relative to output directory
                abs_path = clip["path"]
                rel_path = os.path.relpath(abs_path, "output")
                clip["path"] = rel_path
            
            # Find corresponding mistake and add enhanced data
            for mistake in all_mistakes:
                if abs(mistake.get("timestamp", 0) - clip.get("start_time", 0)) < 2.0:
                    clip["damage_dealt"] = mistake.get("damage_dealt", 0)
                    clip["damage_taken"] = mistake.get("damage_taken", 0)
                    clip["player_name"] = mistake.get("player_name", f"Player {clip.get('player', 'unknown')[-1]}")
                    clip["range_suggestion"] = mistake.get("range_suggestion", "")
                    clip["round"] = mistake.get("round", 1)
                    clip["leader"] = mistake.get("leader", "tied")
                    break
        
        print(f"  Generated {len(clips)} clips")
    else:
        print("  No clips to generate")
        clips = []
    
    clip_gen.save_clips_manifest("clips_manifest.json")
    clip_gen.close()
    
    # Step 5: Generate HTML player
    print("\n[5/6] Generating enhanced HTML5 video player...")
    player_gen = EnhancedVideoPlayerGenerator("output")
    html_path = player_gen.generate_player_html(
        clips, 
        character_info, 
        usernames,
        enhanced_data,
        "video_player.html"
    )
    print(f"  Player generated: {html_path}")
    
    # Step 6: Save metadata
    print("\n[6/6] Saving metadata...")
    metadata = {
        "video_path": video_path,
        "clips": clips,
        "character_info": {
            "player1": {
                "image_path": character_info.get("player1", {}).get("image_path", ""),
                "colors": character_info.get("player1", {}).get("colors", {}),
                "starting_position": character_info.get("player1", {}).get("starting_position", "left")
            },
            "player2": {
                "image_path": character_info.get("player2", {}).get("image_path", ""),
                "colors": character_info.get("player2", {}).get("colors", {}),
                "starting_position": character_info.get("player2", {}).get("starting_position", "right")
            }
        },
        "usernames": usernames,
        "enhanced_data": enhanced_data,
        "analysis_report": report
    }
    
    metadata_path = os.path.join("output", "metadata.json")
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "="*80)
    print("Video Player Generation Complete!")
    print("="*80)
    print(f"\nOutput files:")
    print(f"  - HTML Player: {html_path}")
    print(f"  - Metadata: {metadata_path}")
    print(f"  - Clips: {len(clips)} clips in 'clips/' directory")
    print(f"  - Character Images: 'character_images/' directory")
    print(f"\nOpen the HTML file in your browser to view the video player!")
    print(f"   File: {os.path.abspath(html_path)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
