import os
import subprocess
import re
import shutil

AUDIO_DIR = os.path.join(os.path.dirname(__file__), '../public/audio/syllables_ogg')
TEMP_OUT = "temp_norm.ogg"

def get_max_volume(file_path):
    cmd = ["ffmpeg", "-i", file_path, "-af", "volumedetect", "-f", "null", "-"]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    output = result.stderr
    
    # Parse max_volume: -20.5 dB
    match = re.search(r"max_volume: ([\-\d\.]+) dB", output)
    if match:
        return float(match.group(1))
    return None

def normalize_file(file_path, target_peak=-1.0):
    max_vol = get_max_volume(file_path)
    if max_vol is None:
        return False
        
    gain = target_peak - max_vol
    if gain < 0.1: # Already loud enough
        return True
        
    # Apply gain
    # ffmpeg -i input -af "volume=10dB" output
    cmd = ["ffmpeg", "-y", "-i", file_path, "-af", f"volume={gain}dB", "-c:a", "libvorbis", TEMP_OUT]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(TEMP_OUT):
        shutil.move(TEMP_OUT, file_path)
        return True
    return False

def main():
    files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.ogg')]
    print(f"Normalizing {len(files)} files...")
    
    count = 0
    for idx, f in enumerate(files):
        if idx % 20 == 0:
            print(f"Progress: {idx}/{len(files)}")
            
        path = os.path.join(AUDIO_DIR, f)
        if normalize_file(path):
            count += 1
            
    print(f"Normalized {count} files.")

if __name__ == "__main__":
    main()
