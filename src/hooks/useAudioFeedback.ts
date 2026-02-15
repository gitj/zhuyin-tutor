import { useCallback } from 'react';

export const useAudioFeedback = () => {
    // Get the base URL from Vite (handles the /zhuyin-tutor/ prefix on GitHub Pages)
    const baseUrl = import.meta.env.BASE_URL;

    // Helper to ensure path is correct regardless of leading slash in base
    const getPath = (path: string) => {
        // Remove leading slash from path if base already ends with one
        const cleanBase = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
        const cleanPath = path.startsWith('/') ? path : `/${path}`;
        return `${cleanBase}${cleanPath}`;
    };

    const playKeySound = useCallback((key: string) => {
        // Map special keys to filenames
        let filename = key;
        if (key === '/') filename = 'slash';
        if (key === ',') filename = 'comma';
        if (key === '.') filename = 'period';
        if (key === ';') filename = 'semicolon';
        if (key === '-') filename = 'minus';

        const audio = new Audio(getPath(`audio/${filename}.mp3`));
        audio.play().catch(e => console.error("Error playing key audio:", e));
    }, []);

    const playSyllableSound = useCallback((syllable: string) => {
        // Hybrid System: Try MP3 (Google TTS - High Quality) first
        // If not found (404), fallback to OGG (Moedict - Open Source)
        const mp3Path = getPath(`audio/syllables/${syllable}.mp3`);
        const oggPath = getPath(`audio/syllables_ogg/${syllable}.ogg`);

        const audio = new Audio(mp3Path);

        audio.onerror = () => {
            // MP3 failed (likely missing), try OGG
            console.log(`MP3 missing for ${syllable}, falling back to OGG`);
            const fallbackAudio = new Audio(oggPath);
            fallbackAudio.play().catch(e => console.warn(`Both MP3 and OGG failed for ${syllable}`));
        };

        audio.play().catch(e => {
            // This catch handles playback errors (e.g. autoplay), not loading errors (404)
            // But sometimes 404 triggers this too depending on browser
            console.log(`MP3 playback error for ${syllable}, trying OGG`);
            const fallbackAudio = new Audio(oggPath);
            fallbackAudio.play();
        });
    }, []);

    return { playKeySound, playSyllableSound };
};
