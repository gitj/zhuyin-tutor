import os
import requests
import time
from valid_syllables import VALID_SYLLABLES_NO_TONE

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../public/audio/syllables')

def download_audio(text, filename):
    # Google TTS URL
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
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Downloading {len(VALID_SYLLABLES_NO_TONE)} syllable audio files to {OUTPUT_DIR}...")
    
    count = 0
    for syllable in VALID_SYLLABLES_NO_TONE:
        filename = os.path.join(OUTPUT_DIR, f"{syllable}.mp3")
        
        # Skip if exists to save bandwidth/time
        if os.path.exists(filename):
            continue
            
        if download_audio(syllable, filename):
            count += 1
            # Be nice to the API
            time.sleep(0.5)
            
    print(f"Finished. Downloaded {count} new files.")

if __name__ == "__main__":
    main()
