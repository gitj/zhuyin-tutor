import json
import os
import requests
import random

MAPPING_FILE = os.path.join(os.path.dirname(__file__), 'moedict_audio_map.json')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../public/audio/moedict_test')

def download_file(url, filename):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(r.content)
            print(f"Downloaded: {filename}")
            return True
        else:
            print(f"Failed to download {url}: {r.status_code}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if not os.path.exists(MAPPING_FILE):
        print("Mapping file not found.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} audio mappings.")
    
    # Structure seems to be a list of objects based on previous research, or a list of list.
    # Let's check type again to be sure.
    if isinstance(data, list):
        print("Data is a list.")
        # Only print first item to avoid massive spam
        print(f"Sample item: {data[0]}")
    elif isinstance(data, dict):
         print("Data is a dict.")
         print(f"Sample item: {list(data.items())[0]}")

    # Based on search: "Word.Bopu" -> ID
    # or list of {"title": "Word", ...}
    
    # Strategy: 
    # 1. Parse Key-Value pairs.
    # 2. Try to find "ㄅㄚ" (as a single char or part of word)
    
    # Let's try downloading a known ID if we can find one. 
    # For now, just print the structure so I can write the logic in next step.
    
    # Actually, let's try to just download a few random ones from the list/dict
    
    count = 0
    for key in data:
        if count >= 3: break
        
        # If it's a dict, key is the word identifier
        # If list, key is an item
        
        # Taking a guess it is a dict based on "mapping"
        if isinstance(data, dict):
            # key might be "町.ㄉㄧㄥ", value "1220"
            audio_id = data[key]
            url = f"http://a.moedict.tw/{audio_id}.ogg"
            filename = os.path.join(OUTPUT_DIR, f"{audio_id}.ogg")
            print(f"Attempting to download {key} -> {url}")
            download_file(url, filename)
            count += 1
            
    print("Done.")

if __name__ == "__main__":
    main()
