import { useState, useCallback, useEffect } from 'react';
import { ZHUYIN_KEYMAP } from '../data/keymap';

export interface TypingState {
    syllables: string[];
    currentSyllableIndex: number;
    currentCharIndex: number;
    errors: { syllableIndex: number; charIndex: number }[];
    startTime: number | null;
    wpm: number;
    accuracy: number;
    completed: boolean;
    // Events for audio triggers
    lastEvent: 'none' | 'char-correct' | 'syllable-complete' | 'error';
}

export const useTypingEngine = (lessonContent: string[]) => {
    const [state, setState] = useState<TypingState>({
        syllables: lessonContent,
        currentSyllableIndex: 0,
        currentCharIndex: 0,
        errors: [],
        startTime: null,
        wpm: 0,
        accuracy: 100,
        completed: false,
        lastEvent: 'none'
    });

    useEffect(() => {
        setState({
            syllables: lessonContent,
            currentSyllableIndex: 0,
            currentCharIndex: 0,
            errors: [],
            startTime: null,
            wpm: 0,
            accuracy: 100,
            completed: false,
            lastEvent: 'none'
        });
    }, [lessonContent]);

    const calculateStats = useCallback((currState: TypingState) => {
        if (!currState.startTime) return { wpm: 0, accuracy: 100 };

        const timeElapsedMin = (Date.now() - currState.startTime) / 60000;

        // Calculate total chars typed correctly
        let correctChars = 0;
        for (let i = 0; i < currState.currentSyllableIndex; i++) {
            correctChars += currState.syllables[i].length;
        }
        correctChars += currState.currentCharIndex;

        const wpm = Math.round((correctChars / 5) / timeElapsedMin) || 0;
        const totalTyped = correctChars + currState.errors.length;
        const accuracy = totalTyped > 0
            ? Math.round(((totalTyped - currState.errors.length) / totalTyped) * 100)
            : 100;

        return { wpm, accuracy };
    }, []);

    const handleKeyPress = useCallback((key: string) => {
        if (state.completed) return { event: 'none', currentSyllable: '' };

        let event: TypingState['lastEvent'] = 'none';
        let justCompletedSyllable = '';

        setState(prev => {
            let newState = { ...prev };

            if (!newState.startTime) {
                newState.startTime = Date.now();
            }

            const currentSyllable = newState.syllables[newState.currentSyllableIndex];
            const targetChar = currentSyllable[newState.currentCharIndex];

            const mappedChar = ZHUYIN_KEYMAP[key];
            const isCorrect = mappedChar === targetChar;

            if (isCorrect) {
                newState.currentCharIndex += 1;
                event = 'char-correct';

                // Check if syllable complete
                if (newState.currentCharIndex >= currentSyllable.length) {
                    justCompletedSyllable = currentSyllable;
                    newState.currentSyllableIndex += 1;
                    newState.currentCharIndex = 0;
                    event = 'syllable-complete';

                    if (newState.currentSyllableIndex >= newState.syllables.length) {
                        newState.completed = true;
                    }
                }
            } else {
                // Record error if not already recorded for this specific position
                const errorExists = newState.errors.some(e =>
                    e.syllableIndex === newState.currentSyllableIndex &&
                    e.charIndex === newState.currentCharIndex
                );
                if (!errorExists) {
                    newState.errors = [...newState.errors, {
                        syllableIndex: newState.currentSyllableIndex,
                        charIndex: newState.currentCharIndex
                    }];
                }
                event = 'error';
            }

            const stats = calculateStats(newState);
            return { ...newState, ...stats, lastEvent: event };
        });

        return { event, justCompletedSyllable };
    }, [state.completed, calculateStats]);

    return {
        ...state,
        handleKeyPress,
        restart: () => {
            setState({
                syllables: lessonContent,
                currentSyllableIndex: 0,
                currentCharIndex: 0,
                errors: [],
                startTime: null,
                wpm: 0,
                accuracy: 100,
                completed: false,
                lastEvent: 'none'
            });
        }
    };
};
