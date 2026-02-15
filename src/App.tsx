import { useState, useEffect, useCallback } from 'react';
import { useTypingEngine } from './hooks/useTypingEngine';
import { useAudioFeedback } from './hooks/useAudioFeedback';
import { TypingArea } from './components/TypingArea';
import { VirtualKeyboard } from './components/VirtualKeyboard';
import { Stats } from './components/Stats';
import { ZHUYIN_KEYMAP } from './data/keymap';
import { generateWeightedLesson } from './utils/LessonGenerator';

// Fallback lesson if json not loaded yet
const DEFAULT_LESSON = {
  id: 'demo',
  content: 'ㄅㄆㄇㄈㄉㄊㄋㄌ',
  name: 'Demo Lesson'
};

import lessonsData from './data/lessons.json';

function App() {
  // Use random lesson as initial state
  const [currentLesson, setCurrentLesson] = useState(() => {
    const content = generateWeightedLesson(24);
    return {
      id: `random-${Date.now()}`,
      name: 'Random High-Freq',
      content: content
    };
  });

  // Hard Mode State
  const [isHardMode, setIsHardMode] = useState(false);

  // Method to generate a new random lesson
  const handleNewRandomLesson = useCallback(() => {
    // Reduced to 24 syllables for better fit
    const newContent = generateWeightedLesson(24);
    setCurrentLesson({
      id: `random-${Date.now()}`,
      name: 'Random High-Freq',
      content: newContent
    });
  }, []);

  const {
    syllables,
    currentSyllableIndex,
    currentCharIndex,
    errors,
    wpm,
    accuracy,
    completed,
    handleKeyPress,
    restart,
    lastEvent
  } = useTypingEngine(currentLesson.content);

  const { playKeySound, playSyllableSound } = useAudioFeedback();

  // Handle Audio Logic based on Engine State
  useEffect(() => {
    if (completed) return;

    if (lastEvent === 'char-correct') {
      // Logic to play key sound ONLY if we didn't just complete a syllable
      // But wait, lastEvent is 'char-correct' only if it WAS NOT 'syllable-complete'.
      // The engine sets event = 'syllable-complete' PRIORITY over 'char-correct' if both happen.
      // So if lastEvent is 'char-correct', it means we are MID-syllable.

      const currentSyllable = syllables[currentSyllableIndex];
      // currentCharIndex is already advanced. Target char was at index-1.
      const charIndexTyped = currentCharIndex - 1;

      if (charIndexTyped >= 0 && currentSyllable) {
        const charTyped = currentSyllable[charIndexTyped];
        // Reverse lookup char -> key to find filename
        const key = Object.keys(ZHUYIN_KEYMAP).find(k => ZHUYIN_KEYMAP[k] === charTyped);
        if (key) playKeySound(key);
      }
    } else if (lastEvent === 'syllable-complete') {
      // Syllable just finished. Play the full syllable sound (which is now an MP3).
      // We do NOT play the key sound here, effectively silencing the final keystroke's individual sound.

      const completedSyllable = syllables[currentSyllableIndex - 1];
      const nextSyllable = syllables[currentSyllableIndex];

      if (completedSyllable) playSyllableSound(completedSyllable);

      // Queue the next one if available
      if (nextSyllable && !completed) {
        setTimeout(() => {
          playSyllableSound(nextSyllable);
        }, 800);
      }
    } else if (lastEvent === 'none' && currentSyllableIndex === 0 && currentCharIndex === 0) {
      // Initial load
      const firstSyllable = syllables[0];
      if (firstSyllable) playSyllableSound(firstSyllable);
    }
  }, [lastEvent, currentSyllableIndex, currentCharIndex, completed, playSyllableSound, playKeySound, syllables]);


  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignore modifier keys
      if (e.metaKey || e.ctrlKey || e.altKey) return;

      // Prevent Firefox Quick Search on '/'
      if (e.key === '/') {
        e.preventDefault();
      }

      // Replay Audio on Space
      if (e.code === 'Space') {
        e.preventDefault();
        const currentSyllable = syllables[currentSyllableIndex];
        if (!completed && currentSyllable) {
          playSyllableSound(currentSyllable);
        }
        return;
      }

      if (completed) {
        // Generate new lesson on any key press if completed
        handleNewRandomLesson();
        return;
      }

      if (e.key.length === 1) {
        handleKeyPress(e.key);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyPress, completed, handleNewRandomLesson, syllables, currentSyllableIndex, playSyllableSound]);

  const currentSyllable = syllables[currentSyllableIndex];
  // In Hard Mode, we do NOT show the next char hint on the keyboard
  const nextChar = !completed && currentSyllable && !isHardMode
    ? currentSyllable[currentCharIndex]
    : null;

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center py-10 font-sans selection:bg-blue-500 selection:text-white">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-2">
          Zhuyin Typing Tutor
        </h1>
        <p className="text-gray-400">Master Bopomofo with audio feedback</p>
      </header>

      <div className="w-full max-w-5xl px-4 flex flex-col items-center">
        {/* Control Bar: Mode Toggle + Random Button + Stats */}
        <div className="mb-6 w-full bg-gray-800 p-4 rounded-lg flex flex-col xl:flex-row gap-4 items-center justify-between">

          {/* Left: Controls */}
          <div className="flex flex-col sm:flex-row gap-4 w-full xl:w-auto items-center">

            {/* Mode Toggle */}
            <button
              onClick={() => setIsHardMode(!isHardMode)}
              className={`
                px-4 py-2 rounded font-bold shadow transition-all whitespace-nowrap w-full sm:w-auto flex items-center justify-center gap-2
                ${isHardMode
                  ? 'bg-red-600 hover:bg-red-700 text-white'
                  : 'bg-green-600 hover:bg-green-700 text-white'}
              `}
            >
              {isHardMode ? '🔥 Hard Mode' : '🌱 Easy Mode'}
            </button>

            <button
              onClick={handleNewRandomLesson}
              className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold rounded shadow transition-all whitespace-nowrap w-full sm:w-auto"
            >
              🎲 New Random
            </button>
          </div>

          {/* Right: Stats (Inline) */}
          <div className="w-full xl:w-auto border-t xl:border-t-0 xl:border-l border-gray-700 pt-4 xl:pt-0 xl:pl-4">
            <Stats wpm={wpm} accuracy={accuracy} completed={completed} />
          </div>
        </div>

        <TypingArea
          syllables={syllables}
          currentSyllableIndex={currentSyllableIndex}
          currentCharIndex={currentCharIndex}
          errors={errors}
          completed={completed}
          onRestart={restart}
          isHardMode={isHardMode}
        />

        <VirtualKeyboard nextChar={nextChar} />

        <div className="mt-8 text-sm text-gray-500">
          {completed
            ? <span className="text-green-400 font-bold animate-pulse">Press any key to start next lesson</span>
            : isHardMode
              ? "Hard Mode: Listen and type. Press 'Space' to replay audio."
              : "Type the highlighted character. Audio plays for full syllables and keys."}
        </div>
      </div>
    </div>
  );
}


export default App;
