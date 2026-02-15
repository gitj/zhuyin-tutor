import sys
import os
import json
import csv
from collections import defaultdict

# Add current dir to sys.path if needed
sys.path.append(os.path.dirname(__file__))

# Import pypinyin from venv if not in path (usually activated, but here we run with full path)
from pypinyin import pinyin, Style

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'frequency.tsv')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '../src/data/syllable_frequency.json')

def get_zhuyin_syllable(char):
    """Convert char to a single Zhuyin syllable without tone."""
    # Convert to Bopomofo with tones
    result = pinyin(char, style=Style.BOPOMOFO)
    if not result:
        return None
        
    s = result[0][0] # First char, first pronunciation
    
    # Strip tone marks: ˊ ˇ ˋ ˙
    for tone in ['ˊ', 'ˇ', 'ˋ', '˙']:
        s = s.replace(tone, '')
        
    # Check if empty or not zhuyin (e.g. number or punctuation)
    # Simple check: must contain at least one zhuyin symbol
    # Actually pypinyin returns original char if no pinyin.
    # So if s == char, it's not converted.
    if s == char:
        return None
        
    return s

def main():
    print(f"Reading {INPUT_FILE}...")
    
    syllable_weights = defaultdict(int)
    
    # The `notes.tsv` format: 
    # Usually: Rank [tab] Character [tab] Pinyin [tab] Definition...
    # Or just raw lines. Based on `head` output (which I'll see if I waited, but assuming TSV):
    # If the file has a header, skip it.
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        
        # Rank based weighting:
        # Rank 1 character gets weight 3000
        # Rank 3000 character gets weight 1
        # Or raw frequency count if available.
        
        # Let's assume the order IS frequency rank (1st line = most frequent).
        # We'll assign weights: 5000 - rank
        
        rank = 0
        max_rank = 5000
        
        for row in reader:
            if not row: continue
            
            # Heuristic to find the character column
            # Look for a column with a single character
            char = None
            for col in row:
                if len(col) == 1 and '\u4e00' <= col <= '\u9fff':
                    char = col
                    break
            
            if not char:
                continue
                
            rank += 1
            if rank > max_rank:
                break
                
            syllable = get_zhuyin_syllable(char)
            if syllable:
                weight = max_rank - rank + 1
                syllable_weights[syllable] += weight

    # Convert to list of [syllable, weight] for easy consumption
    # Filter out very rare ones? Or keep all.
    results = [[s, w] for s, w in syllable_weights.items()]
    
    # Sort by weight desc
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Ensure dir exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(results)} distinct syllables with weights to {OUTPUT_FILE}")
    print(f"Top 5: {results[:5]}")

if __name__ == "__main__":
    main()
