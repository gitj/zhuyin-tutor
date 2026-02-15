import os
import subprocess
import wave
import struct
import math
import sys

def analyze_audio(ogg_path):
    print(f"Analyzing {ogg_path}")
    temp_wav = "temp_analyze.wav"
    
    # Convert to WAV
    cmd = ["ffmpeg", "-y", "-i", ogg_path, "-ac", "1", "-ar", "16000", temp_wav]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if not os.path.exists(temp_wav):
        print("Failed to convert to WAV")
        return

    wav = wave.open(temp_wav, 'r')
    frames = wav.readframes(wav.getnframes())
    framerate = wav.getframerate()
    sampwidth = wav.getsampwidth()
    wav.close()
    
    # Process audio
    # 16-bit audio, 16000Hz
    # Expect 2 bytes per sample
    
    samples = struct.unpack_from(f"{len(frames)//2}h", frames)
    
    chunk_ms = 50
    chunk_size = int(framerate * chunk_ms / 1000)
    
    max_amp = 0
    rms_values = []
    
    for i in range(0, len(samples), chunk_size):
        chunk = samples[i:i+chunk_size]
        if not chunk: break
        
        # Calculate RMS
        sum_sq = sum(s*s for s in chunk)
        rms = math.sqrt(sum_sq / len(chunk))
        rms_values.append(rms)
        max_amp = max(max_amp, rms)
        
    print(f"Max RMS: {max_amp}")
    
    # Threshold for silence (e.g., 5% of max volume or fixed value)
    threshold = max_amp * 0.1 
    silence_threshold = max_amp * 0.05
    
    print(f"Silence Threshold: {silence_threshold}")
    
    # State machine: 
    # 1. Wait for sound (start > threshold)
    # 2. Wait for silence (drop < silence_threshold for X duration)
    
    state = "WAIT_START"
    start_speech_idx = 0
    end_speech_idx = 0
    
    consecutive_silence = 0
    required_silence_chunks = 4 # 200ms
    
    for idx, rms in enumerate(rms_values):
        time_sec = idx * (chunk_ms / 1000)
        # bar = "#" * int(rms / max_amp * 50)
        # print(f"{time_sec:.2f}s: {int(rms)} {bar}")
        
        if state == "WAIT_START":
            if rms > threshold:
                state = "SPEAKING"
                start_speech_idx = idx
                print(f"Speech detected at {time_sec:.2f}s")
                
        elif state == "SPEAKING":
            if rms < silence_threshold:
                consecutive_silence += 1
                if consecutive_silence >= required_silence_chunks:
                    # Found gap!
                    end_speech_time = (idx - required_silence_chunks) * (chunk_ms / 1000)
                    print(f"Speech ended at {end_speech_time:.2f}s (Gap found)")
                    
                    # We found the first gap.
                    # Suggest a trim point slightly after end of speech
                    trim_point = end_speech_time + 0.2
                    print(f"Suggested trim point: {trim_point:.2f}s")
                    
                    try:
                        os.remove(temp_wav)
                    except: pass
                    return trim_point
            else:
                consecutive_silence = 0
                
    print("No clear gap found.")
    try:
        os.remove(temp_wav)
    except: pass
    return None

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(__file__), '../public/audio/syllables_ogg/ㄒㄧㄝ.ogg')
    analyze_audio(target)
