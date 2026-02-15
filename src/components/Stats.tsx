import React from 'react';

interface StatsProps {
    wpm: number;
    accuracy: number;
    completed: boolean;
}

export const Stats: React.FC<StatsProps> = ({ wpm, accuracy, completed }) => {
    return (
        <div className="flex gap-8 justify-center items-center">
            <div className="text-center">
                <div className="text-xs text-gray-400 uppercase tracking-widest font-semibold">WPM</div>
                <div className={`text-2xl font-bold ${completed ? 'text-green-400' : 'text-white'}`}>
                    {wpm}
                </div>
            </div>

            <div className="w-px h-8 bg-gray-600"></div>

            <div className="text-center">
                <div className="text-xs text-gray-400 uppercase tracking-widest font-semibold">Accuracy</div>
                <div className={`text-2xl font-bold ${completed ? 'text-green-400' : 'text-white'}`}>
                    {accuracy}%
                </div>
            </div>
        </div>
    );
};
