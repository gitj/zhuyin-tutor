import os
import requests

# Standard Zhuyin Layout Mapping with Keys
KEYMAP = {
    '1': 'ㄅ', 'q': 'ㄆ', 'a': 'ㄇ', 'z': 'ㄈ',
    '2': 'ㄉ', 'w': 'ㄊ', 's': 'ㄋ', 'x': 'ㄌ',
    '3': 'ˇ', 'e': 'ㄍ', 'd': 'ㄎ', 'c': 'ㄏ',
    '4': 'ˋ', 'r': 'ㄐ', 'f': 'ㄑ', 'v': 'ㄒ',
    '5': 'ㄓ', 't': 'ㄔ', 'g': 'ㄕ', 'b': 'ㄖ',
    '6': 'ˊ', 'y': 'ㄗ', 'h': 'ㄘ', 'n': 'ㄙ',
    '7': '˙', 'u': 'ㄧ', 'j': 'ㄨ', 'm': 'ㄩ',
    '8': 'ㄚ', 'i': 'ㄛ', 'k': 'ㄜ', ',': 'ㄝ',
    '9': 'ㄞ', 'o': 'ㄟ', 'l': 'ㄠ', '.': 'ㄡ',
    '0': 'ㄢ', 'p': 'ㄣ', ';': 'ㄤ', '/': 'ㄥ',
    '-': 'ㄦ'
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../public/audio')

def download_audio(char, filename):
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={char}&tl=zh-TW&client=tw-ob"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {char} -> {filename}")
        else:
            print(f"Failed to download {char}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {char}: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Downloading {len(KEYMAP)} audio files to {OUTPUT_DIR}...")
    
    for key, char in KEYMAP.items():
        # Clean filename to be safe
        safe_key = key
        if key == '/': safe_key = 'slash'
        if key == ',': safe_key = 'comma'
        if key == '.': safe_key = 'period'
        if key == ';': safe_key = 'semicolon'
        if key == '-': safe_key = 'minus'
        
        filename = os.path.join(OUTPUT_DIR, f"{safe_key}.mp3")
        
        # Download only if not exists (or force overwrite)
        download_audio(char, filename)

if __name__ == "__main__":
    main()
