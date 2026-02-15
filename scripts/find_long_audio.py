import os
import subprocess
import re

AUDIO_DIR = os.path.join(os.path.dirname(__file__), '../public/audio/syllables_ogg')

def get_duration(file_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 0.0

def main():
    files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.ogg')]
    print(f"Checking {len(files)} files for duration > 0.8s...")
    
    long_files = []
    
    for f in files:
        path = os.path.join(AUDIO_DIR, f)
        duration = get_duration(path)
        if duration > 0.8:
            long_files.append((f, duration))
            
    long_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Found {len(long_files)} long files.")
    for name, dur in long_files:
        print(f"{name}: {dur:.2f}s")

if __name__ == "__main__":
    main()
