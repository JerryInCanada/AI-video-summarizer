# AI-video-summarizer
Developed an advanced AI-powered video summarizer designed to efficiently extract key highlights and condense long-form video content into concise, actionable summaries. This project addresses the growing need for rapid content consumption and intelligent information extraction from dynamic media.

Hardware and Software Requirements

Hardware Requirements

-   A computer capable of running Python 3.8+
-   At least 8GB RAM (recommended 16GB for processing longer videos)
-   Sufficient disk space (processing long videos may temporarily
    require several GB)

Software Requirements

-   Python 3.8 or higher

-   Required Python libraries
    Install using: pip install -r requirements.txt

    The required libraries include:

    -   openai-whisper
    -   moviepy
    -   anthropic
    -   librosa, numpy, soundfile
    -   ffmpeg-python

-   FFmpeg
    Ensure FFmpeg is added to PATH or configure in config.py

Contributors

Xixian Yang

-   Implemented core system architecture
-   Integrated Whisper
-   Audio peak detection
-   Video highlight extraction pipeline
-   CLI workflow development

Xiang Li

-   Multi-model AI analysis module
-   Highlight scoring logic
-   Text summarization engine
-   GUI implementation
-   System debugging and optimization

Both contributed to system design, integration, testing, and
documentation.

Project Overview

This project is an AI-driven multimedia communication system for
generating sports video highlights. It combines speech-to-text, semantic
analysis, audio detection, and automated video editing. The system
identifies exciting moments from commentary and audio cues, producing
both video highlights and structured summaries. It supports Claude, GPT,
and Gemini models with both CLI and GUI interfaces.

Instructions for Setup and Execution

1. Install Dependencies

    pip install -r requirements.txt

2. Configure FFmpeg

Set FFmpeg path in config.py if needed.

3. Set API Key

Edit config.py:

    API_KEY = "your_api_key"

4. Optional Environment Check

    python check_ready.py

5. Run Main Program (CLI)

    python main.py your_video.mp4

6. Run GUI

    python ui.py

7. Output Files

-   *_highlights.mp4
-   *_summary.txt
-   *_summary.md
-   *_summary.json
-   *_transcript.json
