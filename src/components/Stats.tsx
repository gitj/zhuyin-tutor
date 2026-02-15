import React from 'react';

interface StatsProps {
    wpm: number;
    accuracy: number;
    completed: boolean;
}

export const Stats: React.FC<StatsProps> = ({ wpm, accuracy, completed }) => {
    return (
        <div className="flex gap-8 justify-center items-center p-4 bg-gray-800 rounded-lg shadow-md mb-6">
            <div className="text-center">
                <div className="text-sm text-gray-400 uppercase tracking-widest font-semibold">WPM</div>
                <div className={`text-3xl font-bold ${completed ? 'text-green-400' : 'text-white'}`}>
                    {wpm}
                </div>
            </div>

            <div className="w-px h-10 bg-gray-600"></div>

            <div className="text-center">
                <div className="text-sm text-gray-400 uppercase tracking-widest font-semibold">Accuracy</div>
                <div className={`text-3xl font-bold ${completed ? 'text-green-400' : 'text-white'}`}>
                    {accuracy}%
                </div>
            </div>
        </div>
    );
};
