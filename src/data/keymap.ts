export interface KeyMapItem {
    key: string;
    zhuyin: string;
}

export const ZHUYIN_KEYMAP: Record<string, string> = {
    '1': 'ㄅ', 'q': 'ㄆ', 'a': 'ㄇ', 'z': 'ㄈ',
    '2': 'ㄉ', 'w': 'ㄊ', 's': 'ㄋ', 'x': 'ㄌ',
    '3': 'ˇ', 'e': 'ㄍ', 'd': 'ㄎ', 'c': 'ㄏ',
    '4': 'ˋ', 'r': 'ㄐ', 'f': 'ㄑ', 'v': 'ㄒ',
    '5': 'ㄓ', 't': 'ㄔ', 'g': 'ㄕ', 'b': 'ㄖ',
    '6': 'ˊ', 'y': 'ㄗ', 'h': 'ㄘ', 'n': 'ㄙ',
    '7': '˙', 'u': 'ㄧ', 'j': 'ㄨ', 'm': 'ㄩ',
    '8': 'ㄚ', 'i': 'ㄛ', 'k': 'ㄜ', ',': 'ㄝ',
    '9': 'ㄞ', 'o': 'ㄟ', 'l': 'ㄠ', '.': 'ㄡ',
    '0': 'ㄢ', 'p': 'ㄣ', ';': 'ㄤ', '/': 'ㄥ',
    '-': 'ㄦ'
};

export const REVERSE_KEYMAP: Record<string, string> = Object.entries(ZHUYIN_KEYMAP).reduce((acc, [key, char]) => {
    acc[char] = key;
    return acc;
}, {} as Record<string, string>);

export const KEYBOARD_ROWS = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
];
