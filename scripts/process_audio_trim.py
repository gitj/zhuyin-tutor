import os
import subprocess
import wave
import struct
import math
import shutil

AUDIO_DIR = os.path.join(os.path.dirname(__file__), '../public/audio/syllables_ogg')
TEMP_WAV = "temp_process.wav"

def get_trim_point(ogg_path):
    # Convert to WAV for analysis
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
        
        chunk_ms = 20 # finer granularity
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
        
        if max_amp < 100: return None # Two quiet
        
        threshold = max_amp * 0.1
        silence_threshold = max_amp * 0.05
        
        state = "WAIT_START"
        consecutive_silence = 0
        required_silence_chunks = int(300 / chunk_ms) # 300ms gap
        
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
                        trim_time = (end_speech_idx * chunk_ms / 1000) + 0.1 # Add buffer
                        break
                else:
                    consecutive_silence = 0
        
        return trim_time
        
    except Exception as e:
        print(f"Error analyzing {ogg_path}: {e}")
        return None
    finally:
        if os.path.exists(TEMP_WAV):
            os.remove(TEMP_WAV)

def trim_file(ogg_path, endpoint):
    temp_out = "temp_trimmed.ogg"
    # ffmpeg -i input -t duration -c copy output
    cmd = ["ffmpeg", "-y", "-i", ogg_path, "-t", str(endpoint), "-c", "copy", temp_out]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(temp_out):
        shutil.move(temp_out, ogg_path)
        return True
    return False

def main():
    files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.ogg')]
    print(f"Processing {len(files)} files...")
    
    processed = 0
    skipped = 0
    errors = 0
    
    for idx, f in enumerate(files):
        path = os.path.join(AUDIO_DIR, f)
        
        # Helper logging
        if idx % 50 == 0:
            print(f"Progress: {idx}/{len(files)}")
            
        trim_point = get_trim_point(path)
        
        if trim_point:
            if trim_point < 0.2:
                # Too short, suspicious
                print(f"Skipping {f}: trim point too short ({trim_point:.2f}s)")
                skipped += 1
            else:
                if trim_file(path, trim_point):
                    processed += 1
                   # print(f"Trimmed {f} at {trim_point:.2f}s")
                else:
                    errors += 1
        else:
            print(f"Skipping {f}: No clear gap found")
            skipped += 1

    print("-" * 30)
    print(f"Total: {len(files)}")
    print(f"Trimmed: {processed}")
    print(f"Skipped/No Gap: {skipped}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    main()
