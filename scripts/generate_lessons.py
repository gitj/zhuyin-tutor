import json
import random
import os
from valid_syllables import VALID_SYLLABLES_NO_TONE

def generate_random_lesson(count=20):
    return random.choices(VALID_SYLLABLES_NO_TONE, k=count)

def generate_lessons():
    lessons = [
        {
            "id": "syllables-20",
            "name": "Random 20 Syllables",
            "content": generate_random_lesson(20) # Now returning list of strings
        },
        {
            "id": "syllables-50",
            "name": "Random 50 Syllables",
            "content": generate_random_lesson(50)
        }
    ]
    
    output_path = os.path.join(os.path.dirname(__file__), "../src/data/lessons.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(lessons)} lessons to {output_path}")

if __name__ == "__main__":
    generate_lessons()
