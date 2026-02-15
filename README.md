# Zhuyin Typing Tutor

A web-based typing tutor for learning the Zhuyin (Bopomofo) keyboard layout.

## Features
- **Visual Keyboard**: Highlights the correct key for the current character.
- **Audio Feedback**: Pronounces the Zhuyin character when you press the key.
- **Progress Tracking**: Tracks WPM and Accuracy.
- **Custom Lessons**: Generate your own lessons using Python.

## Getting Started

1.  **Install Dependencies**:
    ```bash
    npm install
    ```

2.  **Start Development Server**:
    ```bash
    npm run dev
    ```

3.  **Generate New Lessons**:
    Modify `scripts/generate_lessons.py` and run:
    ```bash
    python3 scripts/generate_lessons.py
    ```
    This will update the lessons available in the app.

## Audio Sources
### Default (Open Source)
- **Syllable Pronunciations**: Provided by [Moedict](https://github.com/g0v/moedict-data) (Ministry of Education, Taiwan).
  - License: [CC BY-ND 3.0 Taiwan](https://creativecommons.org/licenses/by-nd/3.0/tw/)
  - Note: Some audio files may contain compound words (e.g., "tang" -> "tang shui").

### High Quality (Optional)
If you prefer higher quality, isolated syllable audio (Google TTS), you can generate it yourself:
1.  Run the download script:
    ```bash
    python3 scripts/download_syllables.py
    ```
2.  The app will automatically prioritize these `.mp3` files over the default `.ogg` files.
    - Note: These files are ignored by git to respect usage terms.

## Tech Stack
- Frontend: React + TypeScript + Vite + TailwindCSS
- Lesson Generation: Python
