"""
Sports Video AI Summarizer - 
Main Program Automatically identifies highlights in sports videos and generates highlight reels and text summaries.
"""
import os
import sys
import argparse
from src.transcribe import VideoTranscriber
from src.audio_analyzer import AudioAnalyzer
from src.video_editor import VideoEditor
from src.summarizer import TextSummarizer
import config

# Select the API request method and model based on the configuration.
if config.USE_HTTP_REQUEST:
    # Use a multi-model analyzer (supports Claude/GPT/Gemini)
    from src.multi_model_analyzer import MultiModelAnalyzer as ClaudeAnalyzer
    print(f"Using a multi-model analyzer: {config.AVAILABLE_MODELS[config.SELECTED_MODEL]['name']}")
else:
    from src.claude_analyzer import ClaudeAnalyzer
    print("Calling APIs using the anthropic library")

def main(video_path, output_dir="output", use_audio_analysis=True):
    """
    Main processing flow
    
    Args:
        video_path: Enter video path
        output_dir: Output directory
        use_audio_analysis: Use audio analysis enhancement
    """
    print("=" * 70)
    print("体Sports Video AI Summarizer".center(70))
    print("=" * 70)
    
    # Check video files
    if not os.path.exists(video_path):
        print(f"[ERROR] Video file does not exist: {video_path}")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the video file name (excluding the extension)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    print(f"\nInput video: {video_path}")
    print(f"Output directory: {output_dir}")
    print("-" * 70)
    
    # ========== Step 1: Speech-to-Text ==========
    print("\n【Step 1/5】Speech to Text")
    transcriber = VideoTranscriber(model_size=config.WHISPER_MODEL)
    result = transcriber.transcribe(video_path, language=config.WHISPER_LANGUAGE)
    formatted_transcript = transcriber.format_transcript(result)
    
    # Save transcription results
    transcript_path = os.path.join(output_dir, f"{video_name}_transcript.json")
    transcriber.save_transcript(formatted_transcript, transcript_path)
    
    # Obtain the complete text for AI analysis
    full_text = transcriber.get_full_text(formatted_transcript)
    
    # ========== Step 2: AI Analysis of Highlights ==========
    print("\n【Step 2/5】AI Analysis of Highlights")
    
    if config.USE_HTTP_REQUEST:
        # Using a multi-model analyzer
        analyzer = ClaudeAnalyzer(
            api_key=config.API_KEY,
            model_type=config.SELECTED_MODEL,
            api_base=config.API_BASE.replace("https://", "").replace("http://", "")
        )
    else:
        # Use the anthropic library (Claude is supported only).
        from src.claude_analyzer import ClaudeAnalyzer as ClaudeOnly
        analyzer = ClaudeOnly(
            api_key=config.CLAUDE_API_KEY, 
            model=config.CLAUDE_MODEL,
            base_url=config.CLAUDE_API_BASE
        )
    highlights = analyzer.analyze_highlights(full_text)
    
    if not highlights:
        print("[WARNING] No exciting moments were detected; the program has ended")
        return
    
    # Filtering low-scoring moments
    highlights = analyzer.filter_by_score(highlights, min_score=6)
    
    # ========== Step 3: Audio Peak Detection (Optional) ==========
    if use_audio_analysis:
        print("\n[Step 3/5] Audio Peak Detection (Enhanced Analysis)")
        audio_analyzer = AudioAnalyzer(threshold=config.AUDIO_PEAK_THRESHOLD)
        audio_peaks = audio_analyzer.detect_peaks(video_path)
        
        # Fusion of audio and text analysis results
        highlights = audio_analyzer.compare_with_transcript(audio_peaks, highlights)
    else:
        print("\n[Step 3/5] Skip audio analysis")
        for h in highlights:
            h['final_score'] = h.get('score', 5)
    
    # Sort by final score
    highlights = sorted(highlights, key=lambda x: x['final_score'], reverse=True)
    
    # ========== Step 4: Generate Highlights Video ==========
    print("\n[Step 4/5] Generate a highlight reel video")
    editor = VideoEditor(buffer_seconds=config.HIGHLIGHT_BUFFER)
    
    highlight_video_path = os.path.join(output_dir, f"{video_name}_highlights.mp4")
    success = editor.create_highlights_video(video_path, highlights, highlight_video_path)
    
    if not success:
        print("[WARNING] Video editing failed")
    
    # ========== Step 5: Generate Text Summary ==========
    print("\n【Step 5/5】Generate a text summary")
    summarizer = TextSummarizer()
    
    summary_path = os.path.join(output_dir, f"{video_name}_summary.txt")
    summarizer.generate_summary(highlights, summary_path)
    
    # Display summary in console
    summarizer.print_summary(highlights)
    
    # ========== Completed ==========
    print("\n" + "=" * 70)
    print("[SUCCESS] Processing complete!".center(70))
    print("=" * 70)
    print(f"\nOutput file:")
    print(f"  1. Highlights Video: {highlight_video_path}")
    print(f"  2. Text Summary: {summary_path}")
    print(f"  3. Transcription results: {transcript_path}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sports Video AI Summarizer")
    parser.add_argument("video", help="Enter the video file path")
    parser.add_argument("-o", "--output", default="output", help="Output directory (default: output)")
    parser.add_argument("--no-audio", action="store_true", help="Without using audio analysis")
    
    args = parser.parse_args()
    
    # Check API Key
    if config.CLAUDE_API_KEY == "your-api-key-here":
        print("[ERROR] Please set CLAUDE_API_KEY in config.py first.")
        sys.exit(1)
    
    # Run the main program
    main(
        video_path=args.video,
        output_dir=args.output,
        use_audio_analysis=not args.no_audio
    )

