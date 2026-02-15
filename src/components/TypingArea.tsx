import React, { useRef, useEffect } from 'react';

interface TypingAreaProps {
    syllables: string[];
    currentSyllableIndex: number;
    currentCharIndex: number;
    errors: { syllableIndex: number; charIndex: number }[];
    completed: boolean;
    onRestart: () => void;
}

export const TypingArea: React.FC<TypingAreaProps> = ({
    syllables,
    currentSyllableIndex,
    currentCharIndex,
    errors,
    completed,
    onRestart
}) => {
    const containerRef = useRef<HTMLDivElement>(null);
    const cursorRef = useRef<HTMLSpanElement>(null);

    // Auto-scroll to cursor
    useEffect(() => {
        if (cursorRef.current && containerRef.current) {
            cursorRef.current.scrollIntoView({
                behavior: 'smooth',
                block: 'center',
                inline: 'center'
            });
        }
    }, [currentSyllableIndex, currentCharIndex]);

    return (
        <div className="max-w-4xl mx-auto w-full mb-8">
            <div
                ref={containerRef}
                className="
                    relative bg-gray-800 rounded-xl p-8 min-h-[160px] 
                    font-mono text-3xl leading-relaxed tracking-wider break-words
                    shadow-inner overflow-hidden border border-gray-700
                "
            >
                {/* Overlay for Completion */}
                {completed && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm z-10 rounded-xl">
                        <button
                            onClick={onRestart}
                            className="px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-bold rounded-full shadow-lg transition-transform transform hover:scale-105"
                        >
                            Restart Lesson
                        </button>
                    </div>
                )}

                {/* Syllable Display */}
                <div className="flex flex-wrap gap-4">
                    {syllables.map((syllable, sIndex) => {
                        const isCurrentSyllable = sIndex === currentSyllableIndex;
                        const isPastSyllable = sIndex < currentSyllableIndex;

                        return (
                            <div
                                key={sIndex}
                                className={`
                                    flex px-2 rounded-lg transition-colors duration-200
                                    ${isCurrentSyllable ? 'bg-blue-900/40 ring-2 ring-blue-500/50' : ''}
                                    ${isPastSyllable ? 'opacity-50' : ''}
                                `}
                            >
                                {syllable.split('').map((char, cIndex) => {
                                    let statusColor = 'text-gray-500';
                                    let bgColor = 'bg-transparent';

                                    const isCurrentChar = isCurrentSyllable && cIndex === currentCharIndex;
                                    const isPastChar = isCurrentSyllable && cIndex < currentCharIndex;
                                    const isError = errors.some(e => e.syllableIndex === sIndex && e.charIndex === cIndex);

                                    if (isPastSyllable || isPastChar) {
                                        statusColor = isError ? 'text-red-400' : 'text-white';
                                    } else if (isCurrentChar) {
                                        statusColor = 'text-white';
                                        bgColor = 'bg-blue-500';
                                    }

                                    return (
                                        <span
                                            key={cIndex}
                                            ref={isCurrentChar ? cursorRef : null}
                                            className={`
                                                relative px-0.5 rounded
                                                ${statusColor} ${bgColor}
                                                ${isCurrentChar ? 'animate-pulse' : ''}
                                            `}
                                        >
                                            {char}
                                        </span>
                                    );
                                })}
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};
