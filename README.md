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

## Tech Stack
- Frontend: React + TypeScript + Vite + TailwindCSS
- Lesson Generation: Python
