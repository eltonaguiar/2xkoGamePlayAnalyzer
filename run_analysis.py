"""
Quick script to run analysis on the provided Blitzcrank vs Blitzcrank video.
"""

import sys
from analyzer import GameplayAnalyzer

def main():
    video_path = r"C:\Users\zerou\Desktop\2xko_blitzvsblitzjuggernaut_Recording 2026-01-17 154457.mp4"
    
    print("2XKO Gameplay Analyzer")
    print("=" * 80)
    print(f"Analyzing: {video_path}")
    print()
    
    try:
        analyzer = GameplayAnalyzer(
            video_path=video_path,
            matchup_type="mirror",
            character="Blitzcrank"
        )
        
        # Run analysis
        report = analyzer.analyze()
        
        # Print report
        analyzer.print_report(report)
        
        # Save report
        output_path = "analysis_report.json"
        analyzer.save_report(report, output_path)
        
        analyzer.close()
        
        print("\nAnalysis complete!")
        
    except FileNotFoundError as e:
        print(f"Error: Video file not found: {e}")
        print("Please check the video path.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
