"""
Combo detection and tracking module for gameplay analysis.
Tracks combo length, damage, and provides performance metrics.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class Combo:
    """Represents a detected combo"""
    player: str  # "player1" or "player2"
    round_number: int
    start_frame: int
    end_frame: int
    start_time: float  # seconds
    end_time: float  # seconds
    hit_count: int
    moves_used: List[str]
    damage_dealt: int  # If available
    ended_by: str  # "dropped", "finished", "reset", "unknown"
    
    @property
    def duration_frames(self) -> int:
        """Get combo duration in frames"""
        return self.end_frame - self.start_frame
    
    @property
    def duration_seconds(self) -> float:
        """Get combo duration in seconds"""
        return self.end_time - self.start_time
    
    def to_dict(self) -> Dict:
        """Convert combo to dictionary"""
        return {
            "player": self.player,
            "round": self.round_number,
            "hit_count": self.hit_count,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_seconds": round(self.duration_seconds, 2),
            "duration_frames": self.duration_frames,
            "moves_used": self.moves_used,
            "damage": self.damage_dealt,
            "ended_by": self.ended_by
        }


class ComboTracker:
    """Tracks and analyzes combos during gameplay"""
    
    def __init__(self, fps: int = 60):
        """
        Initialize combo tracker
        
        Args:
            fps: Frames per second of the video
        """
        self.fps = fps
        self.combos: List[Combo] = []
        self.current_combo: Optional[Dict] = None
        
        # Combo detection settings
        self.min_hits_for_combo = 2  # Minimum hits to count as combo
        self.combo_timeout_frames = 90  # ~1.5 seconds at 60fps
        
    def start_combo(self, player: str, round_number: int, frame: int, 
                   timestamp: float, first_move: str):
        """
        Start tracking a new combo
        
        Args:
            player: "player1" or "player2"
            round_number: Current round number
            frame: Frame number when combo started
            timestamp: Time in seconds
            first_move: First move that started combo
        """
        self.current_combo = {
            "player": player,
            "round": round_number,
            "start_frame": frame,
            "start_time": timestamp,
            "hits": 1,
            "moves": [first_move],
            "last_hit_frame": frame,
            "damage": 0
        }
    
    def add_hit(self, frame: int, move: str, damage: int = 0):
        """
        Add a hit to current combo
        
        Args:
            frame: Current frame number
            move: Move that hit
            damage: Damage dealt (if known)
        """
        if self.current_combo is None:
            return
        
        self.current_combo["hits"] += 1
        self.current_combo["moves"].append(move)
        self.current_combo["last_hit_frame"] = frame
        self.current_combo["damage"] += damage
    
    def end_combo(self, frame: int, timestamp: float, reason: str = "finished"):
        """
        End current combo and save it
        
        Args:
            frame: Frame number when combo ended
            timestamp: Time in seconds
            reason: Why combo ended ("dropped", "finished", "reset", "unknown")
        """
        if self.current_combo is None:
            return
        
        # Only save if it meets minimum hit requirement
        if self.current_combo["hits"] >= self.min_hits_for_combo:
            combo = Combo(
                player=self.current_combo["player"],
                round_number=self.current_combo["round"],
                start_frame=self.current_combo["start_frame"],
                end_frame=frame,
                start_time=self.current_combo["start_time"],
                end_time=timestamp,
                hit_count=self.current_combo["hits"],
                moves_used=self.current_combo["moves"],
                damage_dealt=self.current_combo["damage"],
                ended_by=reason
            )
            self.combos.append(combo)
        
        self.current_combo = None
    
    def check_timeout(self, current_frame: int, timestamp: float):
        """
        Check if current combo has timed out
        
        Args:
            current_frame: Current frame number
            timestamp: Current timestamp in seconds
        """
        if self.current_combo is None:
            return
        
        frames_since_last_hit = current_frame - self.current_combo["last_hit_frame"]
        if frames_since_last_hit > self.combo_timeout_frames:
            self.end_combo(current_frame, timestamp, reason="finished")
    
    def get_longest_combo_by_round(self) -> Dict[int, Dict[str, Optional[Combo]]]:
        """
        Get longest combo for each player in each round
        
        Returns:
            Dictionary: {round_number: {"player1": Combo, "player2": Combo}}
        """
        longest_by_round = {}
        
        for combo in self.combos:
            round_num = combo.round_number
            
            if round_num not in longest_by_round:
                longest_by_round[round_num] = {"player1": None, "player2": None}
            
            current_longest = longest_by_round[round_num][combo.player]
            if current_longest is None or combo.hit_count > current_longest.hit_count:
                longest_by_round[round_num][combo.player] = combo
        
        return longest_by_round
    
    def get_combo_stats(self, player: Optional[str] = None, 
                       round_number: Optional[int] = None) -> Dict:
        """
        Get combo statistics
        
        Args:
            player: Filter by player ("player1" or "player2"), None for all
            round_number: Filter by round, None for all rounds
        
        Returns:
            Dictionary with combo statistics
        """
        # Filter combos
        filtered_combos = self.combos
        if player:
            filtered_combos = [c for c in filtered_combos if c.player == player]
        if round_number:
            filtered_combos = [c for c in filtered_combos if c.round_number == round_number]
        
        if not filtered_combos:
            return {
                "total_combos": 0,
                "avg_combo_length": 0,
                "max_combo_length": 0,
                "total_damage": 0
            }
        
        hit_counts = [c.hit_count for c in filtered_combos]
        
        return {
            "total_combos": len(filtered_combos),
            "avg_combo_length": round(sum(hit_counts) / len(hit_counts), 1),
            "max_combo_length": max(hit_counts),
            "min_combo_length": min(hit_counts),
            "total_damage": sum(c.damage_dealt for c in filtered_combos),
            "longest_combo": max(filtered_combos, key=lambda c: c.hit_count)
        }
    
    def get_performance_level(self, avg_combo_length: float) -> str:
        """
        Determine performance level based on average combo length
        
        Args:
            avg_combo_length: Average combo length
        
        Returns:
            Performance level string
        """
        if avg_combo_length >= 10:
            return "Expert"
        elif avg_combo_length >= 7:
            return "Advanced"
        elif avg_combo_length >= 5:
            return "Intermediate"
        elif avg_combo_length >= 3:
            return "Beginner"
        else:
            return "Learning"
    
    def generate_combo_report(self) -> Dict:
        """
        Generate comprehensive combo report
        
        Returns:
            Dictionary with full combo report
        """
        longest_by_round = self.get_longest_combo_by_round()
        
        report = {
            "summary": {
                "total_combos": len(self.combos),
                "player1_stats": self.get_combo_stats("player1"),
                "player2_stats": self.get_combo_stats("player2")
            },
            "by_round": {},
            "longest_combos": {
                "player1": None,
                "player2": None
            }
        }
        
        # Stats by round
        for round_num in sorted(longest_by_round.keys()):
            report["by_round"][f"round_{round_num}"] = {
                "player1": longest_by_round[round_num]["player1"].to_dict() 
                          if longest_by_round[round_num]["player1"] else None,
                "player2": longest_by_round[round_num]["player2"].to_dict() 
                          if longest_by_round[round_num]["player2"] else None
            }
        
        # Overall longest combos
        p1_combos = [c for c in self.combos if c.player == "player1"]
        p2_combos = [c for c in self.combos if c.player == "player2"]
        
        if p1_combos:
            longest_p1 = max(p1_combos, key=lambda c: c.hit_count)
            report["longest_combos"]["player1"] = longest_p1.to_dict()
            report["summary"]["player1_stats"]["performance_level"] = \
                self.get_performance_level(report["summary"]["player1_stats"]["avg_combo_length"])
        
        if p2_combos:
            longest_p2 = max(p2_combos, key=lambda c: c.hit_count)
            report["longest_combos"]["player2"] = longest_p2.to_dict()
            report["summary"]["player2_stats"]["performance_level"] = \
                self.get_performance_level(report["summary"]["player2_stats"]["avg_combo_length"])
        
        return report
    
    def format_combo_for_display(self, combo: Combo) -> str:
        """
        Format combo for human-readable display
        
        Args:
            combo: Combo to format
        
        Returns:
            Formatted string
        """
        time_str = str(timedelta(seconds=int(combo.start_time)))
        moves_str = " > ".join(combo.moves_used[:5])  # Show first 5 moves
        if len(combo.moves_used) > 5:
            moves_str += "..."
        
        return (f"{combo.hit_count}-hit combo by {combo.player} "
                f"at {time_str} (Round {combo.round_number}): {moves_str}")


def detect_combo_opportunities(move_history: List[Dict], 
                               character_combos: Dict) -> List[Dict]:
    """
    Detect missed combo opportunities based on move history
    
    Args:
        move_history: List of moves performed
        character_combos: BnB combos from character data
    
    Returns:
        List of missed opportunities
    """
    opportunities = []
    
    # Check if player performed combo starters but didn't follow through
    for i, move in enumerate(move_history[:-2]):
        # Check each known combo
        for combo_id, combo_data in character_combos.items():
            starter = combo_data["starter"]
            expected_sequence = combo_data["inputs"][:3]  # First 3 moves
            
            if move["move"] == starter:
                # Check if they followed through with combo
                actual_sequence = [m["move"] for m in move_history[i:i+3]]
                
                if len(actual_sequence) >= 2:
                    # They started combo but didn't follow optimal route
                    if actual_sequence[0] == expected_sequence[0] and \
                       actual_sequence[1] != expected_sequence[1]:
                        opportunities.append({
                            "timestamp": move["timestamp"],
                            "missed_combo": combo_data["name"],
                            "notation": combo_data["notation"],
                            "what_happened": f"Started with {starter} but didn't continue optimally",
                            "suggestion": f"Practice {combo_data['name']}: {combo_data['notation']}"
                        })
    
    return opportunities
