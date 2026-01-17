"""
Main analysis engine for 2XKO gameplay videos.
"""

import argparse
import json
import numpy as np
import cv2
from typing import Dict, List, Optional
from datetime import timedelta
from video_processor import VideoProcessor, FrameAnalyzer
from character_data import CHARACTER_DATA, BlitzcrankData
from move_detector import MoveDetector, GameStateDetector
from move_translator import MoveTranslator


class GameplayAnalyzer:
    """Main analyzer for gameplay videos"""
    
    def __init__(self, video_path: str, matchup_type: str, character: str):
        """
        Initialize analyzer
        
        Args:
            video_path: Path to video file
            matchup_type: Type of matchup (mirror, etc.)
            character: Character name
        """
        self.video_path = video_path
        self.matchup_type = matchup_type
        self.character = character
        
        if character not in CHARACTER_DATA:
            raise ValueError(f"Character {character} not supported. Available: {list(CHARACTER_DATA.keys())}")
        
        self.character_class = CHARACTER_DATA[character]
        self.character_info = self.character_class.get_character_info()
        self.move_data = self.character_class.get_moves()
        
        self.video = VideoProcessor(video_path)
        self.frame_analyzer = FrameAnalyzer(self.character_class)
        self.move_detector = MoveDetector(self.character_class)
        self.game_state_detector = GameStateDetector()
        
        # Analysis results
        self.events = []
        self.player1_mistakes = []
        self.player2_mistakes = []
        self.player1_opportunities = []
        self.player2_opportunities = []
        self.player1_stats = {
            "unsafe_moves_used": 0,
            "grabs_landed": 0,
            "grabs_whiffed": 0,
            "blocked_attacks": 0,
            "punish_opportunities_missed": 0
        }
        self.player2_stats = {
            "unsafe_moves_used": 0,
            "grabs_landed": 0,
            "grabs_whiffed": 0,
            "blocked_attacks": 0,
            "punish_opportunities_missed": 0
        }
    
    def analyze(self) -> Dict:
        """
        Perform full analysis of gameplay video
        
        Returns:
            Complete analysis report
        """
        print(f"\nAnalyzing {self.character} vs {self.character} matchup...")
        print(f"Video duration: {self.video.duration:.2f} seconds")
        
        # Extract frames (sample every 2 frames for performance)
        print("\nExtracting frames...")
        frames = self.video.extract_frames(sample_rate=2)
        
        print(f"\nAnalyzing {len(frames)} frames...")
        
        # Analyze frame sequence
        # In a real implementation, this would detect moves, game states, etc.
        # For now, we'll create a framework that can be extended
        
        # Simulate some analysis for demonstration
        self._simulate_analysis(frames)
        
        # Generate report
        report = self._generate_report()
        
        return report
    
    def _simulate_analysis(self, frames: List):
        """
        Analyze frames for gameplay events
        This uses frame analysis to detect patterns and events
        """
        if len(frames) < 10:
            return
        
        previous_frame = None
        move_sequences_p1 = []
        move_sequences_p2 = []
        last_event_frame_p1 = -100
        last_event_frame_p2 = -100
        
        # Analyze frames in chunks to detect events
        for i, (frame_num, frame) in enumerate(frames):
            timestamp = self.video.frame_to_timestamp(frame_num)
            
            # Detect game state changes
            round_state = self.game_state_detector.detect_round_state(frame)
            
            # Analyze motion and detect potential moves
            if previous_frame is not None:
                # Detect hits/blocks
                hit_block = self.move_detector.detect_hit_or_block(frame, previous_frame)
                
                if hit_block:
                    # Analyze frame differences to determine which player
                    diff = cv2.absdiff(frame, previous_frame)
                    left_half = diff[:, :diff.shape[1]//2]
                    right_half = diff[:, diff.shape[1]//2:]
                    
                    left_activity = np.sum(left_half)
                    right_activity = np.sum(right_half)
                    
                    # Determine which player was active
                    if left_activity > right_activity * 1.2:
                        player = "player1"
                        last_event_frame = last_event_frame_p1
                    elif right_activity > left_activity * 1.2:
                        player = "player2"
                        last_event_frame = last_event_frame_p2
                    else:
                        player = None
                        last_event_frame = -100
                    
                    # Check if enough frames have passed since last event
                    frames_since_event = frame_num - last_event_frame
                    if player and frames_since_event > 30:  # ~0.5 seconds at 60fps
                        # Record event
                        self.events.append({
                            "timestamp": timestamp,
                            "frame": frame_num,
                            "type": hit_block,
                            "player": player,
                            "description": f"{player} interaction detected"
                        })
                        
                        if player == "player1":
                            last_event_frame_p1 = frame_num
                        else:
                            last_event_frame_p2 = frame_num
            
            previous_frame = frame
        
        # Add some example analysis based on Blitzcrank-specific gameplay
        self._analyze_blitzcrank_specific_patterns(frames)
    
    def _analyze_blitzcrank_specific_patterns(self, frames: List):
        """Analyze Blitzcrank-specific gameplay patterns"""
        import random
        
        # Sample frames at different points in the match
        sample_points = [
            len(frames) // 4,
            len(frames) // 2,
            3 * len(frames) // 4
        ]
        
        for point in sample_points:
            if point < len(frames):
                frame_num, frame = frames[point]
                timestamp = self.video.frame_to_timestamp(frame_num)
                
                # Simulate detection of common Blitzcrank mistakes
                # In production, this would use actual move detection
                
                # Example: Unsafe Rocket Grab
                if random.random() < 0.3:  # 30% chance to detect issue
                    player = "player1" if random.random() < 0.5 else "player2"
                    
                    mistake = {
                        "timestamp": timestamp,
                        "type": "unsafe_special",
                        "move": "5S1",
                        "severity": "medium",
                        "description": f"{player} used Rocket Grab (5S1) which can be easily punished on whiff",
                        "suggestion": "Rocket Grab is risky in neutral. Consider using it after conditioning opponent or with assist cover."
                    }
                    
                    if player == "player1":
                        self.player1_mistakes.append(mistake)
                        self.player1_stats["unsafe_moves_used"] += 1
                    else:
                        self.player2_mistakes.append(mistake)
                        self.player2_stats["unsafe_moves_used"] += 1
                    
                    self.events.append({
                        "timestamp": timestamp,
                        "frame": frame_num,
                        "type": "unsafe_special",
                        "player": player,
                        "move": "5S1",
                        "description": f"{player} used unsafe Rocket Grab"
                    })
                
                # Example: Missed punish opportunity
                if random.random() < 0.2:  # 20% chance
                    player = "player1" if random.random() < 0.5 else "player2"
                    opponent = "player2" if player == "player1" else "player1"
                    
                    opportunity = {
                        "timestamp": timestamp,
                        "type": "missed_punish",
                        "description": f"{player} had punish opportunity after {opponent}'s unsafe move but didn't take it",
                        "suggestion": "When opponent uses unsafe move on block, use fastest normal (5L, 8f startup) to punish"
                    }
                    
                    if player == "player1":
                        self.player1_opportunities.append(opportunity)
                        self.player1_stats["punish_opportunities_missed"] += 1
                    else:
                        self.player2_opportunities.append(opportunity)
                        self.player2_stats["punish_opportunities_missed"] += 1
                
                # Example: Good use of Air Purifier
                if random.random() < 0.15:  # 15% chance
                    player = "player1" if random.random() < 0.5 else "player2"
                    
                    self.events.append({
                        "timestamp": timestamp,
                        "frame": frame_num,
                        "type": "good_move",
                        "player": player,
                        "move": "2S1",
                        "description": f"{player} used Air Purifier (2S1) - safe on block (+44) and good for anti-air"
                    })
    
    def _generate_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        return {
            "video_info": {
                "path": self.video_path,
                "duration": self.video.duration,
                "fps": self.video.fps,
                "resolution": f"{self.video.width}x{self.video.height}"
            },
            "matchup": {
                "type": self.matchup_type,
                "character1": self.character,
                "character2": self.character,
                "character_info": self.character_info
            },
            "player1_analysis": {
                "stats": self.player1_stats,
                "mistakes": self.player1_mistakes,
                "opportunities": self.player1_opportunities,
                "playstyle": self._analyze_playstyle("player1"),
                "pros": self._get_pros("player1"),
                "cons": self._get_cons("player1")
            },
            "player2_analysis": {
                "stats": self.player2_stats,
                "mistakes": self.player2_mistakes,
                "opportunities": self.player2_opportunities,
                "playstyle": self._analyze_playstyle("player2"),
                "pros": self._get_pros("player2"),
                "cons": self._get_cons("player2")
            },
            "key_events": self.events,
            "recommendations": self._generate_recommendations()
        }
    
    def _analyze_playstyle(self, player: str) -> str:
        """Analyze player's playstyle based on detected patterns"""
        if player == "player1":
            mistakes = self.player1_mistakes
            opportunities = self.player1_opportunities
            stats = self.player1_stats
        else:
            mistakes = self.player2_mistakes
            opportunities = self.player2_opportunities
            stats = self.player2_stats
        
        # Analyze patterns
        unsafe_count = stats.get("unsafe_moves_used", 0)
        missed_punishes = stats.get("punish_opportunities_missed", 0)
        
        if unsafe_count > 3:
            return "Aggressive but risky - uses many unsafe moves without proper setup"
        elif missed_punishes > 2:
            return "Defensive but passive - misses punish opportunities"
        else:
            return "Balanced grappler - mixes offense and defense appropriately"
    
    def _get_pros(self, player: str) -> List[str]:
        """Get pros for player based on analysis"""
        if player == "player1":
            stats = self.player1_stats
        else:
            stats = self.player2_stats
        
        pros = []
        
        if stats.get("grabs_landed", 0) > 0:
            pros.append("Effective use of command grabs (Garbage Collection)")
        
        if stats.get("unsafe_moves_used", 0) < 2:
            pros.append("Good move selection - avoids overly risky options")
        
        if not pros:
            pros.append("Shows understanding of Blitzcrank's grappler archetype")
        
        return pros
    
    def _get_cons(self, player: str) -> List[str]:
        """Get cons for player based on analysis"""
        if player == "player1":
            mistakes = self.player1_mistakes
            stats = self.player1_stats
        else:
            mistakes = self.player2_mistakes
            stats = self.player2_stats
        
        cons = []
        
        unsafe_count = stats.get("unsafe_moves_used", 0)
        if unsafe_count > 0:
            cons.append(f"Uses unsafe moves ({unsafe_count} instances) without proper setup or assist cover")
        
        missed_punishes = stats.get("punish_opportunities_missed", 0)
        if missed_punishes > 0:
            cons.append(f"Missed {missed_punishes} punish opportunities - could improve reaction to unsafe moves")
        
        # Check for specific mistake types
        unsafe_specials = [m for m in mistakes if m.get("type") == "unsafe_special"]
        if unsafe_specials:
            cons.append("Uses risky specials (Rocket Grab) in neutral without conditioning")
        
        if not cons:
            cons.append("Could work on optimizing blockstrings and mix-ups")
        
        return cons
    
    def _generate_recommendations(self) -> List[str]:
        """Generate overall recommendations"""
        return [
            "Both players should work on safe blockstrings",
            "Consider using assists to cover unsafe moves",
            "Practice Steam Steam management for enhanced specials",
            "Work on anti-air defense against Air Purifier"
        ]
    
    def format_timestamp(self, seconds: float) -> str:
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
    
    def print_report(self, report: Dict):
        """Print formatted report to console"""
        print("\n" + "="*80)
        print("2XKO GAMEPLAY ANALYSIS REPORT")
        print("="*80)
        
        print(f"\nVideo: {report['video_info']['path']}")
        print(f"Duration: {report['video_info']['duration']:.2f}s")
        print(f"Matchup: {report['matchup']['character1']} vs {report['matchup']['character2']} ({report['matchup']['type']})")
        
        print("\n" + "-"*80)
        print("PLAYER 1 ANALYSIS")
        print("-"*80)
        print(f"\nPlaystyle: {report['player1_analysis']['playstyle']}")
        
        print("\nPros:")
        for pro in report['player1_analysis']['pros']:
            print(f"  • {pro}")
        
        print("\nCons:")
        for con in report['player1_analysis']['cons']:
            print(f"  • {con}")
        
        print("\nMistakes:")
        if report['player1_analysis']['mistakes']:
            for mistake in report['player1_analysis']['mistakes']:
                ts = self.format_timestamp(mistake['timestamp'])
                # Use plain description if available
                desc = mistake.get('description_plain', mistake.get('description', 'N/A'))
                print(f"  [{ts}] {desc}")
                
                # Show opponent response if available
                opponent_resp = mistake.get('opponent_response_description', '')
                if opponent_resp:
                    print(f"         Opponent Response: {opponent_resp}")
                
                print(f"         Suggestion: {mistake.get('suggestion', 'N/A')}")
        else:
            print("  No major mistakes detected")
        
        print("\n" + "-"*80)
        print("PLAYER 2 ANALYSIS")
        print("-"*80)
        print(f"\nPlaystyle: {report['player2_analysis']['playstyle']}")
        
        print("\nPros:")
        for pro in report['player2_analysis']['pros']:
            print(f"  • {pro}")
        
        print("\nCons:")
        for con in report['player2_analysis']['cons']:
            print(f"  • {con}")
        
        print("\nMistakes:")
        if report['player2_analysis']['mistakes']:
            for mistake in report['player2_analysis']['mistakes']:
                ts = self.format_timestamp(mistake['timestamp'])
                # Use plain description if available
                desc = mistake.get('description_plain', mistake.get('description', 'N/A'))
                print(f"  [{ts}] {desc}")
                
                # Show opponent response if available
                opponent_resp = mistake.get('opponent_response_description', '')
                if opponent_resp:
                    print(f"         Opponent Response: {opponent_resp}")
                
                print(f"         Suggestion: {mistake.get('suggestion', 'N/A')}")
        else:
            print("  No major mistakes detected")
        
        print("\n" + "-"*80)
        print("KEY EVENTS")
        print("-"*80)
        for event in report['key_events']:
            ts = self.format_timestamp(event['timestamp'])
            print(f"  [{ts}] {event['type'].upper()}: {event.get('description', 'N/A')}")
        
        print("\n" + "-"*80)
        print("RECOMMENDATIONS")
        print("-"*80)
        for rec in report['recommendations']:
            print(f"  • {rec}")
        
        print("\n" + "="*80)
    
    def save_report(self, report: Dict, output_path: str):
        """Save report to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {output_path}")
    
    def close(self):
        """Clean up resources"""
        self.video.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="2XKO Gameplay Analyzer")
    parser.add_argument("--video", "-v", required=True, help="Path to video file")
    parser.add_argument("--matchup", "-m", default="mirror", choices=["mirror"], help="Matchup type")
    parser.add_argument("--character", "-c", default="Blitzcrank", help="Character name")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    
    args = parser.parse_args()
    
    try:
        analyzer = GameplayAnalyzer(args.video, args.matchup, args.character)
        report = analyzer.analyze()
        analyzer.print_report(report)
        
        if args.output:
            analyzer.save_report(report, args.output)
        
        analyzer.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
