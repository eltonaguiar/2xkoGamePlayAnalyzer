"""
Enhanced analyzer with move tracking, damage estimation, and improved mistake detection.
"""

import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
from analyzer import GameplayAnalyzer
from video_processor import VideoProcessor
from move_translator import MoveTranslator


class EnhancedAnalyzer(GameplayAnalyzer):
    """Enhanced analyzer with move tracking and damage estimation"""
    
    def __init__(self, video_path: str, matchup_type: str, character: str):
        """Initialize enhanced analyzer"""
        super().__init__(video_path, matchup_type, character)
        
        # Move tracking
        self.player1_moves = defaultdict(int)  # move_name -> count
        self.player2_moves = defaultdict(int)
        self.player1_move_timestamps = []  # List of (timestamp, move_name, used_meter)
        self.player2_move_timestamps = []  # List of (timestamp, move_name, used_meter)
        
        # Meter usage tracking
        self.player1_meter_usage = defaultdict(int)  # move_name -> count of meter uses
        self.player2_meter_usage = defaultdict(int)
        
        # Damage tracking - separate dealt and taken
        self.player1_damage_dealt = 0  # Damage P1 dealt to P2
        self.player1_damage_taken = 0  # Damage P1 took from P2
        self.player2_damage_dealt = 0  # Damage P2 dealt to P1
        self.player2_damage_taken = 0  # Damage P2 took from P1
        
        # Damage history with full details
        self.player1_damage_history = []  # List of (timestamp, damage_dealt, damage_taken, round)
        self.player2_damage_history = []  # List of (timestamp, damage_dealt, damage_taken, round)
        
        # Round tracking
        self.current_round = 1
        self.round_starts = [0.0]  # Timestamps when rounds start
        self.round_history = []  # List of (timestamp, round_number)
        
        # Opponent move tracking during mistakes
        self.opponent_moves_during_mistakes = {}  # mistake_timestamp -> list of opponent moves
    
    def analyze(self) -> Dict:
        """Perform enhanced analysis"""
        # Detect starting positions first
        self._detect_starting_positions()
        
        # Track moves and damage
        self._track_moves_and_damage()
        
        # First do standard analysis (this will populate mistakes)
        report = super().analyze()
        
        # Enhance mistakes with additional info
        self._enhance_mistakes()
        
        # Update report with enhanced mistake data
        report["player1_analysis"]["mistakes"] = self.player1_mistakes
        report["player2_analysis"]["mistakes"] = self.player2_mistakes
        
        # Add enhanced data to report
        report["enhanced_data"] = {
            "starting_positions": {
                "player1": self.player1_start_position,
                "player2": self.player2_start_position
            },
            "move_statistics": {
                "player1": dict(self.player1_moves),
                "player2": dict(self.player2_moves),
                "player1_total_moves": sum(self.player1_moves.values()),
                "player2_total_moves": sum(self.player2_moves.values()),
                "player1_move_variety": len(self.player1_moves),
                "player2_move_variety": len(self.player2_moves),
                "player1_meter_usage": dict(self.player1_meter_usage),
                "player2_meter_usage": dict(self.player2_meter_usage)
            },
            "damage_history": {
                "player1": self.player1_damage_history,
                "player2": self.player2_damage_history
            },
            "round_info": {
                "current_round": self.current_round,
                "round_starts": self.round_starts,
                "round_history": self.round_history
            },
            "move_timestamps": {
                "player1": self.player1_move_timestamps,
                "player2": self.player2_move_timestamps
            }
        }
        
        return report
    
    def _detect_starting_positions(self):
        """Detect which side each player starts on"""
        # Get first frame
        self.video.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = self.video.cap.read()
        
        if not ret:
            return
        
        # Analyze character positions in first frame
        height, width = frame.shape[:2]
        left_half = frame[:, :width//2]
        right_half = frame[:, width//2:]
        
        # Detect character presence (look for non-background pixels)
        # Simple heuristic: more activity = character presence
        left_activity = np.sum(cv2.cvtColor(left_half, cv2.COLOR_BGR2GRAY) > 50)
        right_activity = np.sum(cv2.cvtColor(right_half, cv2.COLOR_BGR2GRAY) > 50)
        
        # Check multiple early frames for consistency
        positions_p1 = []
        positions_p2 = []
        
        for frame_num in range(0, min(30, int(self.video.frame_count)), 5):
            self.video.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = self.video.cap.read()
            if not ret:
                continue
            
            # Detect which side has more character-like pixels
            left_half = frame[:, :width//2]
            right_half = frame[:, width//2:]
            
            left_chars = self._detect_character_pixels(left_half)
            right_chars = self._detect_character_pixels(right_half)
            
            if left_chars > right_chars * 1.2:
                positions_p1.append("left")
                positions_p2.append("right")
            elif right_chars > left_chars * 1.2:
                positions_p1.append("right")
                positions_p2.append("left")
        
        if positions_p1:
            self.player1_start_position = Counter(positions_p1).most_common(1)[0][0]
            self.player2_start_position = Counter(positions_p2).most_common(1)[0][0]
        else:
            # Default fallback
            self.player1_start_position = "left"
            self.player2_start_position = "right"
    
    def _detect_character_pixels(self, region: np.ndarray) -> int:
        """Detect number of character-like pixels in region"""
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        # Character pixels are typically not too dark and not too bright
        mask = (gray > 30) & (gray < 220)
        return np.sum(mask)
    
    def _track_moves_and_damage(self):
        """Track moves used and estimate damage with round tracking"""
        # Extract frames
        frames = self.video.extract_frames(sample_rate=2)
        
        previous_frame = None
        last_damage_timestamp = 0
        
        for i, (frame_num, frame) in enumerate(frames):
            timestamp = self.video.frame_to_timestamp(frame_num)
            
            # Detect round changes (simplified - look for reset patterns)
            # In production, would detect round start screens
            if timestamp - last_damage_timestamp > 10 and self.player1_damage_dealt + self.player2_damage_dealt > 500:
                # Possible round end/start
                self.current_round += 1
                self.round_starts.append(timestamp)
                # Reset damage for new round (or track separately)
                last_damage_timestamp = timestamp
            
            # Track round
            self.round_history.append((timestamp, self.current_round))
            
            if previous_frame is not None:
                # Detect move usage (simplified - in production would use actual move detection)
                diff = cv2.absdiff(frame, previous_frame)
                left_half = diff[:, :diff.shape[1]//2]
                right_half = diff[:, diff.shape[1]//2:]
                
                left_activity = np.sum(left_half)
                right_activity = np.sum(right_half)
                
                # Detect hit/block
                hit_block = self.move_detector.detect_hit_or_block(frame, previous_frame)
                
                if hit_block:
                    # Estimate which player and which move
                    if left_activity > right_activity * 1.2:
                        player = "player1"
                        # Simulate move detection (in production would use actual detection)
                        move = self._estimate_move(frame, previous_frame, "left")
                        if move:
                            # Check if meter was used (super moves or enhanced specials)
                            meter_used = self._is_super_move(move) or self._check_meter_usage(frame, "player1")
                            self.player1_moves[move] += 1
                            self.player1_move_timestamps.append((timestamp, move, meter_used))
                            if meter_used:
                                self.player1_meter_usage[move] += 1
                            
                            # Estimate damage
                            damage = self._estimate_damage(move)
                            if damage > 0:
                                # P1 dealt damage to P2
                                self.player1_damage_dealt += damage
                                self.player2_damage_taken += damage
                                
                                # Record in history
                                self.player1_damage_history.append((
                                    timestamp, 
                                    self.player1_damage_dealt, 
                                    self.player1_damage_taken,
                                    self.current_round
                                ))
                                self.player2_damage_history.append((
                                    timestamp,
                                    self.player2_damage_dealt,
                                    self.player2_damage_taken,
                                    self.current_round
                                ))
                                last_damage_timestamp = timestamp
                    
                    elif right_activity > left_activity * 1.2:
                        player = "player2"
                        move = self._estimate_move(frame, previous_frame, "right")
                        if move:
                            # Check if meter was used (super moves or enhanced specials)
                            meter_used = self._is_super_move(move) or self._check_meter_usage(frame, "player2")
                            self.player2_moves[move] += 1
                            self.player2_move_timestamps.append((timestamp, move, meter_used))
                            if meter_used:
                                self.player2_meter_usage[move] += 1
                            
                            # Estimate damage
                            damage = self._estimate_damage(move)
                            if damage > 0:
                                # P2 dealt damage to P1
                                self.player2_damage_dealt += damage
                                self.player1_damage_taken += damage
                                
                                # Record in history
                                self.player1_damage_history.append((
                                    timestamp,
                                    self.player1_damage_dealt,
                                    self.player1_damage_taken,
                                    self.current_round
                                ))
                                self.player2_damage_history.append((
                                    timestamp,
                                    self.player2_damage_dealt,
                                    self.player2_damage_taken,
                                    self.current_round
                                ))
                                last_damage_timestamp = timestamp
            
            previous_frame = frame
    
    def _estimate_move(self, frame: np.ndarray, previous_frame: np.ndarray, side: str) -> Optional[str]:
        """Estimate which move was used (simplified)"""
        # In production, this would use actual move detection
        # For now, return a random move for demonstration
        import random
        moves = ["5L", "5M", "5H", "2L", "2M", "2H", "5S1", "2S1", "2S2"]
        return random.choice(moves) if random.random() < 0.1 else None
    
    def _estimate_damage(self, move_name: str) -> int:
        """Estimate damage for a move"""
        if move_name in self.move_data:
            return self.move_data[move_name].damage
        # Default damage estimates
        damage_map = {
            "5L": 45, "2L": 40,
            "5M": 80, "2M": 75,
            "5H": 120, "2H": 110,
            "5S1": 150, "2S1": 100, "2S2": 200
        }
        return damage_map.get(move_name, 50)
    
    def _enhance_mistakes(self):
        """Enhance mistakes with comprehensive damage, range info, opponent actions, and clearer player identification"""
        # Track opponent moves during mistake windows
        self._track_opponent_moves_during_mistakes()
        
        for mistake in self.player1_mistakes:
            timestamp = mistake.get("timestamp", 0)
            mistake_end_time = timestamp + 5.0  # End of mistake clip
            
            # Get damage info at end of mistake
            damage_info = self._get_damage_info_at_timestamp(mistake_end_time, "player1")
            mistake.update(damage_info)
            mistake["player_name"] = "Player 1"
            mistake["character_side"] = self.player1_start_position
            mistake["round"] = damage_info.get("round", 1)
            mistake["leader"] = self._get_leader_at_timestamp(mistake_end_time)
            
            # Get opponent moves during mistake window
            opponent_moves = self._get_opponent_moves_during_window(timestamp, mistake_end_time, "player2")
            mistake["opponent_response"] = opponent_moves
            mistake["opponent_response_description"] = self._describe_opponent_response(mistake.get("move", ""), opponent_moves, "player1")
            
            # Translate move names to plain English
            mistake["move_plain"] = MoveTranslator.translate_move(mistake.get("move", ""))
            mistake["description_plain"] = self._create_plain_description(mistake)
            
            self._add_range_info(mistake)
        
        for mistake in self.player2_mistakes:
            timestamp = mistake.get("timestamp", 0)
            mistake_end_time = timestamp + 5.0  # End of mistake clip
            
            # Get damage info at end of mistake
            damage_info = self._get_damage_info_at_timestamp(mistake_end_time, "player2")
            mistake.update(damage_info)
            mistake["player_name"] = "Player 2"
            mistake["character_side"] = self.player2_start_position
            mistake["round"] = damage_info.get("round", 1)
            mistake["leader"] = self._get_leader_at_timestamp(mistake_end_time)
            
            # Get opponent moves during mistake window
            opponent_moves = self._get_opponent_moves_during_window(timestamp, mistake_end_time, "player1")
            mistake["opponent_response"] = opponent_moves
            mistake["opponent_response_description"] = self._describe_opponent_response(mistake.get("move", ""), opponent_moves, "player2")
            
            # Translate move names to plain English
            mistake["move_plain"] = MoveTranslator.translate_move(mistake.get("move", ""))
            mistake["description_plain"] = self._create_plain_description(mistake)
            
            self._add_range_info(mistake)
    
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
                        "description_plain": f"{player} used Rocket Grab which can be easily punished if it misses",
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
    
    def _get_damage_info_at_timestamp(self, timestamp: float, player: str) -> Dict:
        """Get comprehensive damage info at a specific timestamp"""
        if player == "player1":
            history = self.player1_damage_history
        else:
            history = self.player2_damage_history
        
        # Find most recent damage entry before or at timestamp
        damage_dealt = 0
        damage_taken = 0
        round_num = 1
        
        for entry in reversed(history):
            if len(entry) >= 4:
                ts, dealt, taken, rnd = entry
                if ts <= timestamp:
                    damage_dealt = dealt
                    damage_taken = taken
                    round_num = rnd
                    break
        
        return {
            "damage_dealt": damage_dealt,
            "damage_taken": damage_taken,
            "round": round_num
        }
    
    def _get_leader_at_timestamp(self, timestamp: float) -> str:
        """Determine which player is leading at a specific timestamp"""
        p1_info = self._get_damage_info_at_timestamp(timestamp, "player1")
        p2_info = self._get_damage_info_at_timestamp(timestamp, "player2")
        
        # Leader is the one who dealt more damage (or took less)
        p1_net = p1_info["damage_dealt"] - p1_info["damage_taken"]
        p2_net = p2_info["damage_dealt"] - p2_info["damage_taken"]
        
        if p1_net > p2_net:
            return "player1"
        elif p2_net > p1_net:
            return "player2"
        else:
            return "tied"
    
    def _track_opponent_moves_during_mistakes(self):
        """Track what opponent did during each mistake window"""
        all_mistakes = self.player1_mistakes + self.player2_mistakes
        
        for mistake in all_mistakes:
            timestamp = mistake.get("timestamp", 0)
            mistake_end = timestamp + 5.0  # 5 second window
            
            # Find opponent moves in this window
            mistake_player = mistake.get("player", "")
            opponent = "player2" if mistake_player == "player1" else "player1"
            
            opponent_moves = self._get_opponent_moves_during_window(timestamp, mistake_end, opponent)
            self.opponent_moves_during_mistakes[timestamp] = opponent_moves
    
    def _check_meter_usage(self, frame: np.ndarray, player: str) -> bool:
        """Check if super meter was used in this frame"""
        # Detect meter usage by checking for:
        # 1. Meter bar decrease
        # 2. Super move visual effects
        # 3. Enhanced special move indicators
        
        meter_info = self.game_state_detector.detect_meter(frame)
        player_meter = meter_info.get(f"{player}_meter", 0)
        
        # In production, would compare with previous meter level
        # For now, check if move is a super or enhanced special
        # This is a simplified check - in production would track meter changes
        return False  # Placeholder - would need meter tracking
    
    def _is_super_move(self, move_name: str) -> bool:
        """Check if a move is a super move (uses meter)"""
        if not move_name:
            return False
        # Super moves typically have "Super" in name or are special enhanced moves
        super_indicators = ["Super", "super", "SU", "EX", "Enhanced"]
        return any(indicator in move_name for indicator in super_indicators)
    
    def _get_opponent_moves_during_window(self, start_time: float, end_time: float, opponent: str) -> List[str]:
        """Get moves opponent used during a time window"""
        if opponent == "player1":
            move_timestamps = self.player1_move_timestamps
        else:
            move_timestamps = self.player2_move_timestamps
        
        opponent_moves = []
        for entry in move_timestamps:
            if len(entry) >= 2:
                ts, move = entry[0], entry[1]
                if start_time <= ts <= end_time:
                    opponent_moves.append(move)
        
        return opponent_moves
    
    def _describe_opponent_response(self, mistake_move: str, opponent_moves: List[str], mistake_player: str) -> str:
        """Describe what opponent did in response to the mistake"""
        mistake_plain = MoveTranslator.translate_move(mistake_move)
        
        if not opponent_moves:
            return f"After {mistake_plain} was used, opponent did not respond with any moves"
        
        # Translate opponent moves
        opponent_moves_plain = [MoveTranslator.translate_move(m) for m in opponent_moves]
        
        # Create natural language description
        if len(opponent_moves_plain) == 1:
            return f"After {mistake_plain} was used, opponent responded with {opponent_moves_plain[0]}"
        elif len(opponent_moves_plain) == 2:
            return f"After {mistake_plain} was used, opponent responded with {opponent_moves_plain[0]}, then {opponent_moves_plain[1]}"
        else:
            moves_str = ", ".join(opponent_moves_plain[:-1])
            return f"After {mistake_plain} was used, opponent responded with {moves_str}, and {opponent_moves_plain[-1]}"
    
    def _create_contextual_description(self, mistake: Dict) -> str:
        """Create contextual description showing the sequence"""
        player_name = mistake.get("player_name", "Player")
        move_plain = mistake.get("move_plain", MoveTranslator.translate_move(mistake.get("move", "")))
        opponent_moves = mistake.get("opponent_response", [])
        
        # Example: "Player 1 missed their Command Grab, then opponent used Command Grab, then Light Kick"
        if mistake.get("type") == "whiffed_grab" or "miss" in mistake.get("description", "").lower():
            if opponent_moves:
                opponent_plain = [MoveTranslator.translate_move(m) for m in opponent_moves]
                if len(opponent_plain) == 1:
                    return f"{player_name} missed their {move_plain}, then opponent used {opponent_plain[0]}"
                else:
                    moves_str = ", then ".join(opponent_plain)
                    return f"{player_name} missed their {move_plain}, then opponent used {moves_str}"
            else:
                return f"{player_name} missed their {move_plain}"
        
        return mistake.get("description_plain", "")
    
    def _create_plain_description(self, mistake: Dict) -> str:
        """Create plain English description of mistake"""
        player_name = mistake.get("player_name", "Player")
        move_plain = mistake.get("move_plain", MoveTranslator.translate_move(mistake.get("move", "")))
        mistake_type = mistake.get("type", "mistake")
        
        # Create context-aware description
        if mistake_type == "unsafe_special" or mistake_type == "unsafe_move":
            desc = f"{player_name} used {move_plain}, which left them vulnerable"
        elif mistake_type == "missed_punish":
            desc = f"{player_name} missed an opportunity to punish the opponent"
        elif mistake_type == "whiffed_grab":
            desc = f"{player_name} attempted {move_plain} but missed"
        else:
            desc = f"{player_name} made a mistake using {move_plain}"
        
        # Add opponent response if available
        opponent_desc = mistake.get("opponent_response_description", "")
        if opponent_desc:
            desc += f". {opponent_desc}"
        
        return desc
    
    def _add_range_info(self, mistake: Dict):
        """Add range information to mistake description"""
        move = mistake.get("move", "")
        description = mistake.get("description", "")
        
        # Check if it's a range-related mistake
        if "range" in description.lower() or move in ["5S1", "2S1"]:  # Rocket Grab, Air Purifier
            # Determine if they should be closer or further
            if move == "5S1":  # Rocket Grab - typically used at mid-far range
                if "close" in description.lower():
                    mistake["range_suggestion"] = "Should be further away for optimal Rocket Grab range"
                else:
                    mistake["range_suggestion"] = "Consider using at mid-range (not point-blank)"
            
            if "range_suggestion" in mistake:
                mistake["suggestion"] = f"{mistake.get('suggestion', '')} {mistake['range_suggestion']}"
