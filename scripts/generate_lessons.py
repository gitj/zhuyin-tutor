import json
import random
import os

# Standard Zhuyin Layout
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

# Reverse mapping for easy lookup
CHAR_TO_KEY = {v: k for k, v in KEYMAP.items()}

def generate_random_lesson(length=50):
    chars = list(KEYMAP.values())
    return "".join(random.choices(chars, k=length))

def generate_lessons():
    lessons = [
        {
            "id": "random-50",
            "name": "Random 50 Characters",
            "content": generate_random_lesson(50)
        },
        {
            "id": "row-1",
            "name": "Row 1 (BPMF D...)",
            "content": "ㄅㄆㄇㄈㄉㄊㄋㄌ" * 5
        }
    ]
    
    output_path = os.path.join(os.path.dirname(__file__), "../src/data/lessons.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(lessons)} lessons to {output_path}")

if __name__ == "__main__":
    generate_lessons()
