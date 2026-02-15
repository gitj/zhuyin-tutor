import json
import os
import requests
import re
import time
import shutil

# Load our valid syllables
try:
    from valid_syllables import VALID_SYLLABLES_NO_TONE
except ImportError:
    import sys
    sys.path.append(os.path.dirname(__file__))
    from valid_syllables import VALID_SYLLABLES_NO_TONE

MAPPING_FILE = os.path.join(os.path.dirname(__file__), 'moedict_audio_map.json')
AUDIO_DIR_OGG = os.path.join(os.path.dirname(__file__), '../public/audio/syllables_ogg')
AUDIO_DIR_MP3 = os.path.join(os.path.dirname(__file__), '../public/audio/syllables') # Legacy

def get_bopomofo(key):
    # Key format is "Word.Bopu" e.g. "焿.ㄍㄥ"
    parts = key.split('.')
    if len(parts) >= 2:
        return parts[-1]
    return ""

def strip_tones(bopomofo):
    # Remove tone marks: ˊ ˇ ˋ ˙
    return re.sub(r'[ˊˇˋ˙]', '', bopomofo)

def download_file(url, filename):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if not os.path.exists(MAPPING_FILE):
        print("Mapping file not found.")
        return

    os.makedirs(AUDIO_DIR_OGG, exist_ok=True)
    
    print("Loading Moedict mapping...")
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        moedict_map = json.load(f)

    # Pre-process map for fast lookup
    # Map toneless -> [list of candidates]
    available_audio = {}
    for key, audio_id in moedict_map.items():
        full_bopomofo = get_bopomofo(key)
        if not full_bopomofo: continue
        
        toneless = strip_tones(full_bopomofo)
        if toneless not in available_audio:
            available_audio[toneless] = []
        
        available_audio[toneless].append({
            'full': full_bopomofo,
            'id': audio_id,
            'word': key.split('.')[0]
        })

    print(f"Starting migration for {len(VALID_SYLLABLES_NO_TONE)} syllables...")
    
    downloaded_count = 0
    missing_count = 0

    for idx, target in enumerate(VALID_SYLLABLES_NO_TONE):
        filename = os.path.join(AUDIO_DIR_OGG, f"{target}.ogg")
        if os.path.exists(filename):
            print(f"[{idx+1}/{len(VALID_SYLLABLES_NO_TONE)}] Skipped (exists): {target}")
            continue

        if target in available_audio:
            candidates = available_audio[target]
            
            # Selection Strategy:
            # 1. Exact match (First Tone, no mark)
            # 2. Shortest match (single character word preferred)
            # 3. First available
            
            selected = None
            
            # Priority 1: Exact match with target (Tone 1)
            exact_matches = [c for c in candidates if c['full'] == target]
            if exact_matches:
                # Sub-sort by word length (shortest word = likely most common single char)
                exact_matches.sort(key=lambda x: len(x['word']))
                selected = exact_matches[0]
            else:
                # Priority 2: Sort by tone (1, 2, 3, 4, 5) if possible? 
                # Or just shortest word again
                candidates.sort(key=lambda x: len(x['word']))
                selected = candidates[0]
            
            url = f"http://a.moedict.tw/{selected['id']}.ogg"
            print(f"[{idx+1}/{len(VALID_SYLLABLES_NO_TONE)}] Downloading {target} from {selected['word']} ({selected['full']})...")
            
            if download_file(url, filename):
                downloaded_count += 1
                # time.sleep(0.1) 
            else:
                print(f"  FAILED to download {target}")
                missing_count += 1
        else:
            print(f"[{idx+1}/{len(VALID_SYLLABLES_NO_TONE)}] MISSING in Moedict: {target}")
            missing_count += 1

    print("Migration Complete.")
    print(f"Downloaded: {downloaded_count}")
    print(f"Missing: {missing_count}")
    
    # Optional: Swap folders
    # print("To apply changes: Update frontend to point to /audio/syllables_ogg/*.ogg")

if __name__ == "__main__":
    main()
