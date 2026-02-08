"""
Sports Video AI Summarizer - GUI
Using Tkinter (built-in Python library)
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path

# Import core modules
from src.transcribe import VideoTranscriber
from src.multi_model_analyzer import MultiModelAnalyzer
from src.audio_analyzer import AudioAnalyzer
from src.video_editor import VideoEditor
from src.summarizer import TextSummarizer
import config

class VideoSummarizerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏀 Sports Video AI Summarizer")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Set style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.video_path = tk.StringVar()
        self.selected_model = tk.StringVar(value=config.SELECTED_MODEL)
        self.use_audio = tk.BooleanVar(value=True)
        self.processing = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI components"""
        
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        
        title_label = tk.Label(
            title_frame,
            text="🏀 Sports Video AI Summarizer",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 1. Video selection area
        video_frame = tk.LabelFrame(
            main_frame,
            text=" 1. Select Video File ",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        video_frame.pack(fill=tk.X, pady=(0, 15))
        
        video_input_frame = tk.Frame(video_frame, bg="#ecf0f1")
        video_input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.video_entry = tk.Entry(
            video_input_frame,
            textvariable=self.video_path,
            font=("Arial", 10),
            width=50
        )
        self.video_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            video_input_frame,
            text="📁 Browse",
            command=self.browse_video,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        browse_btn.pack(side=tk.LEFT)
        
        # 2. AI model selection
        model_frame = tk.LabelFrame(
            main_frame,
            text=" 2. Select AI Model ",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        model_frame.pack(fill=tk.X, pady=(0, 15))
        
        model_inner_frame = tk.Frame(model_frame, bg="#ecf0f1")
        model_inner_frame.pack(padx=10, pady=10)
        
        models = {
            "claude": "Claude Sonnet 4 (Best Semantic Understanding)",
            "gpt": "GPT-5 Chat Latest (OpenAI Latest)",
            "gemini": "Gemini 2.5 Flash (Fastest Speed)"
        }
        
        for key, label in models.items():
            rb = tk.Radiobutton(
                model_inner_frame,
                text=label,
                variable=self.selected_model,
                value=key,
                font=("Arial", 10),
                bg="#ecf0f1",
                activebackground="#ecf0f1",
                cursor="hand2"
            )
            rb.pack(anchor=tk.W, pady=3)
        
        # 3. Advanced options
        options_frame = tk.LabelFrame(
            main_frame,
            text=" 3. Advanced Options ",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        options_inner = tk.Frame(options_frame, bg="#ecf0f1")
        options_inner.pack(padx=10, pady=10)
        
        audio_check = tk.Checkbutton(
            options_inner,
            text="Enable Audio Peak Detection (Assist in identifying highlights)",
            variable=self.use_audio,
            font=("Arial", 10),
            bg="#ecf0f1",
            activebackground="#ecf0f1",
            cursor="hand2"
        )
        audio_check.pack(anchor=tk.W)
        
        # 4. Process button
        self.process_btn = tk.Button(
            main_frame,
            text="🚀 Start Processing",
            command=self.start_processing,
            bg="#27ae60",
            fg="white",
            font=("Arial", 14, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=15
        )
        self.process_btn.pack(pady=(0, 15))
        
        # 5. Progress display
        progress_frame = tk.LabelFrame(
            main_frame,
            text=" 📊 Processing Progress ",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(padx=10, pady=(10, 5))
        
        # Log output
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=15,
            font=("Consolas", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            insertbackground="white"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Bottom status bar
        status_frame = tk.Frame(self.root, bg="#34495e", height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            bg="#34495e",
            fg="white",
            font=("Arial", 9),
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
    
    def browse_video(self):
        """Browse and select video file"""
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv *.flv"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.video_path.set(filename)
            self.log(f"✓ Video selected: {os.path.basename(filename)}")
    
    def log(self, message):
        """Output log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_status(self, text):
        """Update status bar"""
        self.status_label.config(text=text)
        self.root.update()
    
    def start_processing(self):
        """Start processing video"""
        if self.processing:
            messagebox.showwarning("Warning", "Processing in progress, please wait!")
            return
        
        video_path = self.video_path.get()
        if not video_path or not os.path.exists(video_path):
            messagebox.showerror("Error", "Please select a valid video file!")
            return
        
        # Disable button
        self.processing = True
        self.process_btn.config(state=tk.DISABLED, bg="#95a5a6")
        self.progress.start()
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Process in new thread
        thread = threading.Thread(
            target=self.process_video,
            args=(video_path,),
            daemon=True
        )
        thread.start()
    
    def process_video(self, video_path):
        """Process video (runs in background thread)"""
        try:
            self.log("=" * 60)
            self.log("🎬 Start Processing Video")
            self.log("=" * 60)
            
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            video_name = Path(video_path).stem
            
            # Step 1: Speech to text
            self.update_status("Step 1/5: Speech to Text...")
            self.log("\n📝 Step 1/5: Speech to Text")
            self.log(f"Using model: {config.WHISPER_MODEL}")
            
            transcriber = VideoTranscriber(model_size=config.WHISPER_MODEL)
            result = transcriber.transcribe(video_path, language=config.WHISPER_LANGUAGE)
            formatted_transcript = transcriber.format_transcript(result)
            
            transcript_path = os.path.join(output_dir, f"{video_name}_transcript.json")
            transcriber.save_transcript(formatted_transcript, transcript_path)
            
            full_text = transcriber.get_full_text(formatted_transcript)
            self.log(f"✓ Transcription completed, {len(formatted_transcript)} segments")
            
            # Step 2: AI Analysis
            self.update_status("Step 2/5: AI Analysis of Highlights...")
            self.log("\n🤖 Step 2/5: AI Analysis of Highlights")
            
            model_name = config.AVAILABLE_MODELS[self.selected_model.get()]['name']
            self.log(f"Using model: {model_name}")
            
            analyzer = MultiModelAnalyzer(
                api_key=config.API_KEY,
                model_type=self.selected_model.get(),
                api_base=config.API_BASE.replace("https://", "").replace("http://", "")
            )
            
            highlights = analyzer.analyze_highlights(full_text)
            
            if not highlights:
                self.log("⚠ No highlights detected")
                self.finish_processing(False)
                return
            
            highlights = analyzer.filter_by_score(highlights, min_score=6)
            self.log(f"✓ Detected {len(highlights)} highlights")
            
            # Step 3: Audio analysis (optional)
            if self.use_audio.get():
                self.update_status("Step 3/5: Audio Peak Detection...")
                self.log("\n🔊 Step 3/5: Audio Peak Detection")
                
                audio_analyzer = AudioAnalyzer(threshold=config.AUDIO_PEAK_THRESHOLD)
                audio_peaks = audio_analyzer.detect_peaks(video_path)
                highlights = audio_analyzer.compare_with_transcript(audio_peaks, highlights)
                self.log(f"✓ Audio analysis completed")
            else:
                self.log("\n⏭ Step 3/5: Skip audio analysis")
                for h in highlights:
                    h['final_score'] = h.get('score', 5)
            
            highlights = sorted(highlights, key=lambda x: x.get('final_score', 0), reverse=True)
            
            # Step 4: Video editing
            self.update_status("Step 4/5: Generating Highlight Reel...")
            self.log("\n✂ Step 4/5: Generating Highlight Reel")
            
            editor = VideoEditor(buffer_seconds=config.HIGHLIGHT_BUFFER)
            highlight_video_path = os.path.join(output_dir, f"{video_name}_highlights.mp4")
            
            success = editor.create_highlights_video(video_path, highlights, highlight_video_path)
            
            if success:
                self.log(f"✓ Highlight reel generated: {highlight_video_path}")
            else:
                self.log("⚠ Video editing failed")
            
            # Step 5: Generate summary
            self.update_status("Step 5/5: Generating Text Summary...")
            self.log("\n📄 Step 5/5: Generating Text Summary")
            
            summarizer = TextSummarizer()
            summary_path = os.path.join(output_dir, f"{video_name}_summary.txt")
            summarizer.generate_summary(highlights, summary_path)
            
            self.log(f"✓ Text summary generated: {summary_path}")
            
            # Complete
            self.log("\n" + "=" * 60)
            self.log("✅ Processing Complete!")
            self.log("=" * 60)
            self.log(f"\n📁 Output Files:")
            self.log(f"   - Highlight Reel: {highlight_video_path}")
            self.log(f"   - Text Summary: {summary_path}")
            self.log(f"   - Transcript: {transcript_path}")
            
            self.finish_processing(True, highlight_video_path)
            
        except Exception as e:
            self.log(f"\n❌ Processing Error: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            self.finish_processing(False)
    
    def finish_processing(self, success, output_path=None):
        """Processing complete"""
        self.processing = False
        self.progress.stop()
        self.process_btn.config(state=tk.NORMAL, bg="#27ae60")
        
        if success:
            self.update_status("✓ Processing Complete")
            
            # Show completion dialog
            result = messagebox.askquestion(
                "Processing Complete",
                "Video processing completed!\n\nOpen output folder?",
                icon='info'
            )
            
            if result == 'yes':
                output_dir = os.path.abspath("output")
                os.startfile(output_dir)
        else:
            self.update_status("✗ Processing Failed")
            messagebox.showerror("Error", "Video processing failed. Check logs for details.")


def main():
    """Main function"""
    root = tk.Tk()
    app = VideoSummarizerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
