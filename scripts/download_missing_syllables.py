import os
import json
import time
import requests

# Paths
FREQUENCY_FILE = os.path.join(os.path.dirname(__file__), '../src/data/syllable_frequency.json')
AUDIO_DIR = os.path.join(os.path.dirname(__file__), '../public/audio/syllables')

def download_audio(text, filename):
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl=zh-TW&client=tw-ob"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {text} -> {filename}")
            return True
        else:
            print(f"Failed to download {text}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {text}: {e}")
        return False

def main():
    if not os.path.exists(FREQUENCY_FILE):
        print(f"Frequency file not found: {FREQUENCY_FILE}")
        return

    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    print("Loading syllable frequency data...")
    with open(FREQUENCY_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # data is [[syllable, weight], ...]
    syllables = [item[0] for item in data]
    print(f"Found {len(syllables)} syllables in frequency list.")

    missing_count = 0
    downloaded_count = 0

    for syllable in syllables:
        filename = os.path.join(AUDIO_DIR, f"{syllable}.mp3")
        
        if not os.path.exists(filename):
            print(f"Missing audio for: {syllable}")
            missing_count += 1
            
            if download_audio(syllable, filename):
                downloaded_count += 1
                time.sleep(0.5) # Be nice to API
            
    print(f"Scan complete.")
    print(f"Missing files initially: {missing_count}")
    print(f"Downloaded: {downloaded_count}")

if __name__ == "__main__":
    main()
