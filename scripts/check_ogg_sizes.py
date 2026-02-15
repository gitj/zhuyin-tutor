import os

AUDIO_DIR = os.path.join(os.path.dirname(__file__), '../public/audio/syllables_ogg')

files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.ogg')]
print(f"Found {len(files)} OGG files.")

sizes = []
for f in files:
    path = os.path.join(AUDIO_DIR, f)
    size = os.path.getsize(path)
    sizes.append((f, size))

# Sort by size descending
sizes.sort(key=lambda x: x[1], reverse=True)

print("Top 10 largest files:")
for name, size in sizes[:10]:
    print(f"{name}: {size/1024:.2f} KB")

print("\nTop 10 smallest files:")
for name, size in sizes[-10:]:
    print(f"{name}: {size/1024:.2f} KB")
