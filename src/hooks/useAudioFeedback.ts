import { useCallback, useEffect, useState } from 'react';

export const useAudioFeedback = () => {
    // We no longer need speech synthesis voices state
    // const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);

    const playKeySound = useCallback((key: string) => {
        // Map special keys to filenames
        let filename = key;
        if (key === '/') filename = 'slash';
        if (key === ',') filename = 'comma';
        if (key === '.') filename = 'period';
        if (key === ';') filename = 'semicolon';
        if (key === '-') filename = 'minus';

        const audio = new Audio(`/audio/${filename}.mp3`);
        audio.play().catch(e => console.error("Error playing key audio:", e));
    }, []);

    const playSyllableSound = useCallback((syllable: string) => {
        // Hybrid System: Try MP3 (Google TTS - High Quality) first
        // If not found (404), fallback to OGG (Moedict - Open Source)
        const mp3Path = `/audio/syllables/${syllable}.mp3`;
        const oggPath = `/audio/syllables_ogg/${syllable}.ogg`;

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
