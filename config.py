"""
configuration file
"""

# # AI Model Configuration (using yunwu.ai)
API_KEY = "sk-P3BRwNi1xMdFbTZvRDYXDrRcQkBwK7QQNfSdcGVOJ6MGWXPZ"
API_BASE = "https://yunwu.ai"

# List of available models (user can choose)
AVAILABLE_MODELS = {
    "claude": {
        "name": "Claude Sonnet 4",
        "model_id": "claude-sonnet-4-20250514",
        "api_endpoint": "/v1/messages",
        "description": "The strongest semantic understanding, with the highest accuracy."
    },
    "gpt": {
        "name": "GPT-5 Chat Latest",
        "model_id": "gpt-5-chat-latest",
        "api_endpoint": "/v1/chat/completions",
        "description": "OpenAI GPT-5 latest version"
    },
    "gemini": {
        "name": "Gemini 2.5 Flash",
        "model_id": "gemini-2.5-flash",
        "api_endpoint": "/v1beta/models/gemini-2.5-flash:streamGenerateContent",
        "description": "Google's latest model, fast"
    }
}

# The default model used (can be switched in the UI).
SELECTED_MODEL = "claude"  # claude / gpt / gemini

# Compatible with older configurations
CLAUDE_API_KEY = API_KEY
CLAUDE_MODEL = AVAILABLE_MODELS[SELECTED_MODEL]["model_id"]
CLAUDE_API_BASE = API_BASE + "/v1"

# API request method (if the anthropic library connection fails, switch to True to use raw HTTP)
USE_HTTP_REQUEST = True  # True = raw HTTP request, False = anthropic library

# Whisper configuration
WHISPER_MODEL = "medium"  # tiny, base, small, medium, large - Use medium to improve accuracy
WHISPER_LANGUAGE = None  # zh=Chinese, en=English, None=Auto-detect (Recommended)

# FFmpeg path (specify manually if the system cannot find it)
FFMPEG_PATH = r"D:\ffmpeg\ffmpeg-N-121640-g08eda05967-win64-gpl-shared\bin\ffmpeg.exe"

# Audio analysis configuration
AUDIO_PEAK_THRESHOLD = 0.7  # Audio peak threshold (0-1)

# Video editing configuration
HIGHLIGHT_BUFFER = 5  # Leave a few seconds before and after the highlight.
