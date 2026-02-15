import os
import subprocess
import wave
import struct
import math
import shutil

AUDIO_DIR = os.path.join(os.path.dirname(__file__), '../public/audio/syllables_ogg')
TEMP_WAV = "temp_fix.wav"
TEMP_OUT = "temp_fix_out.ogg"

def get_duration(file_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return 0.0

def get_trim_point(ogg_path):
    # Convert to WAV for analysis (force 16k mono)
    cmd = ["ffmpeg", "-y", "-i", ogg_path, "-ac", "1", "-ar", "16000", TEMP_WAV]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if not os.path.exists(TEMP_WAV):
        return None

    try:
        wav = wave.open(TEMP_WAV, 'r')
        frames = wav.readframes(wav.getnframes())
        framerate = wav.getframerate()
        wav.close()
        
        samples = struct.unpack_from(f"{len(frames)//2}h", frames)
        
        chunk_ms = 10 
        chunk_size = int(framerate * chunk_ms / 1000)
        
        max_amp = 0
        rms_values = []
        
        for i in range(0, len(samples), chunk_size):
            chunk = samples[i:i+chunk_size]
            if not chunk: break
            sum_sq = sum(s*s for s in chunk)
            rms = math.sqrt(sum_sq / len(chunk))
            rms_values.append(rms)
            max_amp = max(max_amp, rms)
        
        # Thresholds
        threshold = max_amp * 0.1
        silence_threshold = max_amp * 0.05
        
        state = "WAIT_START"
        consecutive_silence = 0
        required_silence_chunks = int(250 / chunk_ms) # 250ms gap
        
        trim_time = None
        
        for idx, rms in enumerate(rms_values):
            time_sec = idx * (chunk_ms / 1000)
            
            if state == "WAIT_START":
                if rms > threshold:
                    state = "SPEAKING"
            elif state == "SPEAKING":
                if rms < silence_threshold:
                    consecutive_silence += 1
                    if consecutive_silence >= required_silence_chunks:
                        # Gap detected
                        end_speech_idx = idx - consecutive_silence
                        trim_time = (end_speech_idx * chunk_ms / 1000) + 0.15 # Tighter buffer
                        break
                else:
                    consecutive_silence = 0
        
        # Fallback: if no gap found but file is long
        if not trim_time:
             # Look for just *any* drop off?
             pass
             
        return trim_time
        
    except Exception as e:
        print(f"Error analyzing {ogg_path}: {e}")
        return None
    finally:
        if os.path.exists(TEMP_WAV):
            os.remove(TEMP_WAV)

def trim_file(ogg_path, endpoint):
    # Re-encode to ensure length is correct (-c:a libvorbis)
    cmd = ["ffmpeg", "-y", "-i", ogg_path, "-t", str(endpoint), "-c:a", "libvorbis", TEMP_OUT]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(TEMP_OUT):
        shutil.move(TEMP_OUT, ogg_path)
        return True
    return False

def main():
    files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.ogg')]
    print(f"Checking {len(files)} files...")
    
    fixed_count = 0
    
    for idx, f in enumerate(files):
        path = os.path.join(AUDIO_DIR, f)
        duration = get_duration(path)
        
        if duration > 1.0: # Threshold for "Needs Fix"
            # print(f"Fixing {f} (Current: {duration:.2f}s)")
            
            trim_point = get_trim_point(path)
            
            if trim_point:
                if trim_point < 0.2: trim_point = 0.5 # Safety floor
                
                print(f"Trimming {f}: {duration:.2f}s -> {trim_point:.2f}s")
                trim_file(path, trim_point)
                fixed_count += 1
            else:
                # Force trim to 0.8s if no gap found?
                print(f"Could not find gap for {f}, FORCE trimming to 0.8s")
                trim_file(path, 0.8)
                fixed_count += 1
                
    print(f"Fixed {fixed_count} files.")

if __name__ == "__main__":
    main()
