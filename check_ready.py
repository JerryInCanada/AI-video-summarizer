"""
A simple check to see if the environment is ready.
"""
import sys

print("="*60)
print("Environmental inspection")
print("="*60)

# Check Python packages
print("\n1. Check Python packages...")
packages_ok = True
try:
    import whisper
    print("  [OK] whisper")
except:
    print("  [X] whisper - Not installed")
    packages_ok = False

try:
    import moviepy
    print("  [OK] moviepy")
except:
    print("  [X] moviepy - Not installed")
    packages_ok = False

try:
    import anthropic
    print("  [OK] anthropic")
except:
    print("  [X] anthropic - Not installed")
    packages_ok = False

try:
    import librosa
    print("  [OK] librosa")
except:
    print("  [X] librosa - Not installed")
    packages_ok = False

# Check FFmpeg
print("\n2. Check FFmpeg...")
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, 
                          timeout=5)
    if result.returncode == 0:
        print("  [OK] FFmpeg is Already installed")
        ffmpeg_ok = True
    else:
        print("  [X] FFmpeg failed to run")
        ffmpeg_ok = False
except FileNotFoundError:
    # Try using the path in the config
    try:
        import config
        result = subprocess.run([config.FFMPEG_PATH, '-version'],
                              capture_output=True,
                              timeout=5)
        if result.returncode == 0:
            print(f"  [OK] FFmpeg (config path): {config.FFMPEG_PATH}")
            ffmpeg_ok = True
        else:
            print("  [X] Invalid FFmpeg path")
            ffmpeg_ok = False
    except:
        print("  [X] FFmpeg not found")
        ffmpeg_ok = False

# Check configuration
print("\n3. Check API configuration...")
try:
    import config
    if config.CLAUDE_API_KEY and config.CLAUDE_API_KEY != "your-api-key-here":
        print(f"  [OK] API KeyConfigured")
        print(f"  [OK] Model: {config.CLAUDE_MODEL}")
        print(f"  [OK] Request method: {'HTTP' if config.USE_HTTP_REQUEST else 'anthropic库'}")
        config_ok = True
    else:
        print("  [X] API Key not configured")
        config_ok = False
except:
    print("  [X] Configuration file error")
    config_ok = False

# Summary
print("\n" + "="*60)
print("Inspection results:")
print("="*60)
print(f"Python packages: {'OK' if packages_ok else 'fail'}")
print(f"FFmpeg: {'OK' if ffmpeg_ok else 'fail'}")
print(f"API Configuration: {'OK' if config_ok else 'fail'}")

if packages_ok and ffmpeg_ok and config_ok:
    print("\n[Success] Environment is ready! You can start using it!")
    print("\nExample of running:")
    print("  python main.py data/yourvideo.mp4")
    print("\n")
    sys.exit(0)
else:
    print("\n[WARNING] Partial check failed. Please resolve the above issues.")
    sys.exit(1)

