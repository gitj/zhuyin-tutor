import { useState, useEffect } from 'react';
import { useTypingEngine } from './hooks/useTypingEngine';
import { useAudioFeedback } from './hooks/useAudioFeedback';
import { TypingArea } from './components/TypingArea';
import { VirtualKeyboard } from './components/VirtualKeyboard';
import { Stats } from './components/Stats';
import { ZHUYIN_KEYMAP } from './data/keymap';
// import lessons from './data/lessons.json'; // We will load this dynamically or import it

// Fallback lesson if json not loaded yet
const DEFAULT_LESSON = {
  id: 'demo',
  content: 'ㄅㄆㄇㄈㄉㄊㄋㄌ',
  name: 'Demo Lesson'
};

import lessonsData from './data/lessons.json';

function App() {
  const [currentLesson, setCurrentLesson] = useState(lessonsData[0] || DEFAULT_LESSON);

  const {
    text,
    cursorIndex,
    errors,
    wpm,
    accuracy,
    completed,
    handleKeyPress,
    restart
  } = useTypingEngine(currentLesson.content, currentLesson.id);

  const { playSound } = useAudioFeedback();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignore modifier keys
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      // Prevent default for some keys if needed, but usually better to let browser handle unless it conflicts
      if (e.key.length === 1) {
        // e.preventDefault(); // Maybe not needed
        const isLessonComplete = handleKeyPress(e.key);

        // Play sound if correct? Or play sound of the target char?
        // Original request: "when I press a key it plays the corresponding approximate sound"
        // So we play the sound of the KEY PRESSED or the TARGET? 
        // "when I press a key it plays the corresponding approximate sound" -> Key pressed.
        // But for a tutor, usually we want to reinforce the Correct sound.
        // Let's play the sound of the key pressed.

        // Map key to Zhuyin
        // We need the zhuyin char for the key pressed
        // We can look it up in ZHUYIN_KEYMAP inside useAudioFeedback or here.
        // Let's import ZHUYIN_KEYMAP here to look it up for audio.
        // Actually useAudioFeedback could take the zhuyin char.

        // To be safe, let's get the char from the keymap
        // I need to export ZHUYIN_KEYMAP from hooks or data
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyPress]);

  // Effect to play sound on keypress is tricky inside the event handler if we need React state.
  // Better: The `handleKeyPress` returns stats. 
  // Maybe we just modify `useAudioFeedback` to expose a play function we call in the event handler.

  // Re-implementing specific key listener for audio to separate concerns
  useEffect(() => {
    const handleAudio = (e: KeyboardEvent) => {
      if (e.key.length === 1 && !e.metaKey && !e.ctrlKey && !e.altKey) {
        // We need to map key to zhuyin to play it.
        const char = ZHUYIN_KEYMAP[e.key];
        if (char) {
          playSound(e.key);
        }
      }
    };
    window.addEventListener('keydown', handleAudio);
    return () => window.removeEventListener('keydown', handleAudio);
  }, [playSound]);


  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center py-10 font-sans selection:bg-blue-500 selection:text-white">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-2">
          Zhuyin Typing Tutor
        </h1>
        <p className="text-gray-400">Master Bopomofo with audio feedback</p>
      </header>

      <div className="w-full max-w-5xl px-4 flex flex-col items-center">
        {/* Lesson Selector */}
        <div className="mb-6 w-full flex justify-between items-center bg-gray-800 p-4 rounded-lg">
          <div className="text-lg font-semibold text-gray-300 mr-4">Current Lesson:</div>
          <select
            className="bg-gray-700 text-white border-none rounded px-4 py-2 flex-grow focus:ring-2 focus:ring-blue-500 outline-none"
            value={currentLesson.id}
            onChange={(e) => {
              const selected = lessonsData.find(l => l.id === e.target.value);
              if (selected) setCurrentLesson(selected);
            }}
          >
            {lessonsData.map(l => (
              <option key={l.id} value={l.id}>{l.name}</option>
            ))}
          </select>
        </div>

        <Stats wpm={wpm} accuracy={accuracy} completed={completed} />

        <TypingArea
          text={text}
          cursorIndex={cursorIndex}
          errors={errors}
          completed={completed}
          onRestart={restart}
        />

        <VirtualKeyboard nextChar={!completed ? text[cursorIndex] : null} />

        <div className="mt-8 text-sm text-gray-500">
          Press the key corresponding to the highlighted Zhuyin character.
        </div>
      </div>
    </div>
  );
}

export default App;
