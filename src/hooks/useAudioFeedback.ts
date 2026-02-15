import { useCallback } from 'react';

export const useAudioFeedback = () => {
    const playSound = useCallback((key: string) => {
        // Map special keys to filenames as done in the python script
        let filename = key;
        if (key === '/') filename = 'slash';
        if (key === ',') filename = 'comma';
        if (key === '.') filename = 'period';
        if (key === ';') filename = 'semicolon';
        if (key === '-') filename = 'minus';

        const audio = new Audio(`/audio/${filename}.mp3`);
        audio.play().catch(e => console.error("Error playing audio:", e));
    }, []);

    return { playSound };
};
