import React from 'react';
import { ZHUYIN_KEYMAP, KEYBOARD_ROWS, REVERSE_KEYMAP } from '../data/keymap';

interface VirtualKeyboardProps {
    nextChar: string | null;
}

export const VirtualKeyboard: React.FC<VirtualKeyboardProps> = ({ nextChar }) => {
    // Determine which key to highlight
    const highlightKey = nextChar ? REVERSE_KEYMAP[nextChar] : null;

    return (
        <div className="flex flex-col gap-2 p-4 bg-gray-800 rounded-xl shadow-lg w-full max-w-4xl mx-auto">
            {KEYBOARD_ROWS.map((row, rowIndex) => (
                <div key={rowIndex} className="flex justify-center gap-2">
                    {row.map((key) => {
                        const zhuyin = ZHUYIN_KEYMAP[key];
                        const isHighlighted = highlightKey === key;

                        return (
                            <div
                                key={key}
                                className={`
                                    relative flex flex-col items-center justify-center p-2 rounded-lg w-12 h-12 sm:w-14 sm:h-14 transition-all duration-200
                                    ${isHighlighted
                                        ? 'bg-blue-500 text-white transform scale-105 shadow-md ring-2 ring-blue-300'
                                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}
                                `}
                            >
                                <span className={`text-xs absolute top-1 left-1 opacity-60 font-mono`}>
                                    {key.toUpperCase()}
                                </span>
                                <span className="text-lg font-bold">
                                    {zhuyin || ''}
                                </span>
                            </div>
                        );
                    })}
                </div>
            ))}
        </div>
    );
};
