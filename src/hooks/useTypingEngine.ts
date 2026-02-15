import { useState, useCallback, useEffect } from 'react';
import { ZHUYIN_KEYMAP } from '../data/keymap';

export interface TypingState {
    currentLessonId: string;
    text: string;
    cursorIndex: number;
    errors: number[];
    startTime: number | null;
    wpm: number;
    accuracy: number;
    completed: boolean;
}

export const useTypingEngine = (lessonText: string, lessonId: string) => {
    const [state, setState] = useState<TypingState>({
        currentLessonId: lessonId,
        text: lessonText,
        cursorIndex: 0,
        errors: [],
        startTime: null,
        wpm: 0,
        accuracy: 100,
        completed: false,
    });

    // Reset state when lesson changes
    useEffect(() => {
        setState({
            currentLessonId: lessonId,
            text: lessonText,
            cursorIndex: 0,
            errors: [],
            startTime: null,
            wpm: 0,
            accuracy: 100,
            completed: false,
        });
    }, [lessonId, lessonText]);

    const calculateStats = useCallback((currState: TypingState) => {
        if (!currState.startTime) return { wpm: 0, accuracy: 100 };

        const timeElapsedMin = (Date.now() - currState.startTime) / 60000;
        const wpm = Math.round((currState.cursorIndex / 5) / timeElapsedMin) || 0;
        const totalTyped = currState.cursorIndex + currState.errors.length;
        const accuracy = totalTyped > 0
            ? Math.round(((totalTyped - currState.errors.length) / totalTyped) * 100)
            : 100;

        return { wpm, accuracy };
    }, []);

    const handleKeyPress = useCallback((key: string) => {
        if (state.completed) return;

        setState(prev => {
            let newState = { ...prev };

            // Start timer on first keypress
            if (!newState.startTime) {
                newState.startTime = Date.now();
            }

            const targetChar = newState.text[newState.cursorIndex];
            // Map typed key to Zhuyin if possible, otherwise treat as raw key (e.g. punctuation?)
            // For this tutor, we expect the user to type the key that produces the symbol.
            // The `key` passed here should be the keyboard event key (e.g. '1', 'q').

            // Check if the key maps to the target char
            const mappedChar = ZHUYIN_KEYMAP[key];

            const isCorrect = mappedChar === targetChar;

            if (isCorrect) {
                newState.cursorIndex += 1;
                if (newState.cursorIndex >= newState.text.length) {
                    newState.completed = true;
                }
            } else {
                // Only record unique errors per index to avoid spamming error count on same char
                if (!newState.errors.includes(newState.cursorIndex)) {
                    newState.errors = [...newState.errors, newState.cursorIndex];
                }
            }

            const stats = calculateStats(newState);
            return { ...newState, ...stats };
        });

        return state.completed;
    }, [state.completed, calculateStats]);

    return {
        ...state,
        handleKeyPress,
        restart: () => {
            setState({
                currentLessonId: lessonId,
                text: lessonText,
                cursorIndex: 0,
                errors: [],
                startTime: null,
                wpm: 0,
                accuracy: 100,
                completed: false,
            });
        }
    };
};
