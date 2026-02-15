import React, { useRef, useEffect } from 'react';

interface TypingAreaProps {
    text: string;
    cursorIndex: number;
    errors: number[];
    completed: boolean;
    onRestart: () => void;
}

export const TypingArea: React.FC<TypingAreaProps> = ({
    text,
    cursorIndex,
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
    }, [cursorIndex]);

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

                {/* Text Display */}
                <div className="flex flex-wrap">
                    {text.split('').map((char, index) => {
                        let statusColor = 'text-gray-500'; // Upcoming
                        let bgColor = 'bg-transparent';
                        const isCurrent = index === cursorIndex;
                        const isError = errors.includes(index);
                        const isPast = index < cursorIndex;

                        if (isPast) {
                            statusColor = isError ? 'text-red-400' : 'text-white';
                        } else if (isCurrent) {
                            statusColor = 'text-white';
                            bgColor = 'bg-blue-500/30'; // Cursor Block Chars
                        }

                        // Special highlighting for the current character
                        return (
                            <span
                                key={index}
                                ref={isCurrent ? cursorRef : null}
                                className={`
                                    relative px-0.5 rounded
                                    ${statusColor} ${bgColor}
                                    ${isCurrent ? 'animate-pulse ring-2 ring-blue-500' : ''}
                                `}
                            >
                                {char}
                            </span>
                        );
                    })}
                </div>
            </div>
        </div>
    );
};
