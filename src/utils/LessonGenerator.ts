import syllableFrequency from '../data/syllable_frequency.json';

// Type assertion for the imported JSON
const FREQUENCY_DATA: [string, number][] = syllableFrequency as [string, number][];

// Pre-calculate cumulative weights for efficient random selection
let cumulativeWeights: number[] = [];
let totalWeight = 0;

const initWeights = () => {
    if (cumulativeWeights.length > 0) return;

    for (const [_, weight] of FREQUENCY_DATA) {
        totalWeight += weight;
        cumulativeWeights.push(totalWeight);
    }
};

export const generateWeightedLesson = (length: number = 20): string[] => {
    initWeights();
    const lesson: string[] = [];

    for (let i = 0; i < length; i++) {
        const r = Math.random() * totalWeight;

        // Binary search for performance (though linear is probably fine for 400 syllables)
        let low = 0;
        let high = cumulativeWeights.length - 1;
        let index = -1;

        while (low <= high) {
            const mid = Math.floor((low + high) / 2);
            if (cumulativeWeights[mid] >= r) {
                index = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

        if (index !== -1) {
            lesson.push(FREQUENCY_DATA[index][0]);
        } else {
            // Fallback (shouldn't happen)
            lesson.push(FREQUENCY_DATA[FREQUENCY_DATA.length - 1][0]);
        }
    }

    return lesson;
};
