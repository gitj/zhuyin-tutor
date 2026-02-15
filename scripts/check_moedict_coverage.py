import json
import os
import re

# Load our valid syllables
try:
    from valid_syllables import VALID_SYLLABLES_NO_TONE
except ImportError:
    # Fallback if running from different dir
    import sys
    sys.path.append(os.path.dirname(__file__))
    from valid_syllables import VALID_SYLLABLES_NO_TONE

MAPPING_FILE = os.path.join(os.path.dirname(__file__), 'moedict_audio_map.json')

def get_bopomofo(key):
    # Key format is "Word.Bopu" e.g. "焿.ㄍㄥ"
    parts = key.split('.')
    if len(parts) >= 2:
        return parts[-1]
    return ""

def strip_tones(bopomofo):
    # Remove tone marks: ˊ ˇ ˋ ˙
    return re.sub(r'[ˊˇˋ˙]', '', bopomofo)

def main():
    if not os.path.exists(MAPPING_FILE):
        print("Mapping file not found.")
        return

    print("Loading Moedict mapping...")
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        moedict_map = json.load(f)

    print(f"Loaded {len(moedict_map)} entries.")

    # Create a lookup for available syllables
    # We want to map "toneless_syllable" -> [list of (full_bopomofo, id)]
    available_audio = {}

    for key, audio_id in moedict_map.items():
        full_bopomofo = get_bopomofo(key)
        if not full_bopomofo: continue
        
        # Strip tones to compare with our list
        toneless = strip_tones(full_bopomofo)
        
        if toneless not in available_audio:
            available_audio[toneless] = []
        
        available_audio[toneless].append({
            'full': full_bopomofo,
            'id': audio_id,
            'word': key.split('.')[0]
        })

    # Check coverage
    found_count = 0
    missing = []
    
    print("\n--- Checking Coverage ---")
    
    for target in VALID_SYLLABLES_NO_TONE:
        if target in available_audio:
            found_count += 1
            # Optional: Prefer Tone 1 (exact match to toneless)
            # matches = available_audio[target]
            # exact = [m for m in matches if m['full'] == target]
            # if exact:
            #     print(f"Found exact: {target} -> ID {exact[0]['id']}")
            # else:
            #     print(f"Found variant: {target} -> {matches[0]['full']} (ID {matches[0]['id']})")
        else:
            missing.append(target)
            
    print(f"\nTotal Valid Syllables: {len(VALID_SYLLABLES_NO_TONE)}")
    print(f"Found in Moedict: {found_count}")
    print(f"Missing: {len(missing)}")
    
    if missing:
        print("\nMissing Syllables:")
        print(missing)

if __name__ == "__main__":
    main()
