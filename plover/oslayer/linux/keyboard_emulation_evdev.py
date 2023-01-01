
from plover.output import Output
from plover.key_combo import parse_key_combo
from evdev import UInput, ecodes as e
import os

char_mappings = {
    '`': [e.KEY_GRAVE],
    '~': [e.KEY_LEFTSHIFT, e.KEY_GRAVE],
    '1': [e.KEY_1],
    '!': [e.KEY_LEFTSHIFT, e.KEY_1],
    '2': [e.KEY_2],
    '@': [e.KEY_LEFTSHIFT, e.KEY_2],
    '3': [e.KEY_3],
    '#': [e.KEY_LEFTSHIFT, e.KEY_3],
    '4': [e.KEY_4],
    '$': [e.KEY_LEFTSHIFT, e.KEY_4],
    '5': [e.KEY_5],
    '%': [e.KEY_LEFTSHIFT, e.KEY_5],
    '6': [e.KEY_6],
    '^': [e.KEY_LEFTSHIFT, e.KEY_6],
    '7': [e.KEY_7],
    '&': [e.KEY_LEFTSHIFT, e.KEY_7],
    '8': [e.KEY_8],
    '*': [e.KEY_LEFTSHIFT, e.KEY_8],
    '9': [e.KEY_9],
    '(': [e.KEY_LEFTSHIFT, e.KEY_9],
    '0': [e.KEY_0],
    ')': [e.KEY_LEFTSHIFT, e.KEY_0],
    '-': [e.KEY_MINUS],
    '_': [e.KEY_LEFTSHIFT, e.KEY_MINUS],
    '=': [e.KEY_EQUAL],
    '+': [e.KEY_LEFTSHIFT, e.KEY_EQUAL],
    'q': [e.KEY_Q],
    'Q': [e.KEY_LEFTSHIFT, e.KEY_Q],
    'w': [e.KEY_W],
    'W': [e.KEY_LEFTSHIFT, e.KEY_W],
    'e': [e.KEY_E],
    'E': [e.KEY_LEFTSHIFT, e.KEY_E],
    'r': [e.KEY_R],
    'R': [e.KEY_LEFTSHIFT, e.KEY_R],
    't': [e.KEY_T],
    'T': [e.KEY_LEFTSHIFT, e.KEY_T],
    'y': [e.KEY_Y],
    'Y': [e.KEY_LEFTSHIFT, e.KEY_Y],
    'u': [e.KEY_U],
    'U': [e.KEY_LEFTSHIFT, e.KEY_U],
    'i': [e.KEY_I],
    'I': [e.KEY_LEFTSHIFT, e.KEY_I],
    'o': [e.KEY_O],
    'O': [e.KEY_LEFTSHIFT, e.KEY_O],
    'p': [e.KEY_P],
    'P': [e.KEY_LEFTSHIFT, e.KEY_P],
    '[': [e.KEY_LEFTBRACE],
    '{': [e.KEY_LEFTSHIFT, e.KEY_LEFTBRACE],
    ']': [e.KEY_RIGHTBRACE],
    '}': [e.KEY_LEFTSHIFT, e.KEY_RIGHTBRACE],
    '\\': [e.KEY_BACKSLASH],
    '|': [e.KEY_LEFTSHIFT, e.KEY_BACKSLASH],
    'a': [e.KEY_A],
    'A': [e.KEY_LEFTSHIFT, e.KEY_A],
    's': [e.KEY_S],
    'S': [e.KEY_LEFTSHIFT, e.KEY_S],
    'd': [e.KEY_D],
    'D': [e.KEY_LEFTSHIFT, e.KEY_D],
    'f': [e.KEY_F],
    'F': [e.KEY_LEFTSHIFT, e.KEY_F],
    'g': [e.KEY_G],
    'G': [e.KEY_LEFTSHIFT, e.KEY_G],
    'h': [e.KEY_H],
    'H': [e.KEY_LEFTSHIFT, e.KEY_H],
    'j': [e.KEY_J],
    'J': [e.KEY_LEFTSHIFT, e.KEY_J],
    'k': [e.KEY_K],
    'K': [e.KEY_LEFTSHIFT, e.KEY_K],
    'l': [e.KEY_L],
    'L': [e.KEY_LEFTSHIFT, e.KEY_L],
    ';': [e.KEY_SEMICOLON],
    ':': [e.KEY_LEFTSHIFT, e.KEY_SEMICOLON],
    "'": [e.KEY_APOSTROPHE],
    '"': [e.KEY_LEFTSHIFT, e.KEY_APOSTROPHE],
    'z': [e.KEY_Z],
    'Z': [e.KEY_LEFTSHIFT, e.KEY_Z],
    'x': [e.KEY_X],
    'X': [e.KEY_LEFTSHIFT, e.KEY_X],
    'c': [e.KEY_C],
    'C': [e.KEY_LEFTSHIFT, e.KEY_C],
    'v': [e.KEY_V],
    'V': [e.KEY_LEFTSHIFT, e.KEY_V],
    'b': [e.KEY_B],
    'B': [e.KEY_LEFTSHIFT, e.KEY_B],
    'n': [e.KEY_N],
    'N': [e.KEY_LEFTSHIFT, e.KEY_N],
    'm': [e.KEY_M],
    'M': [e.KEY_LEFTSHIFT, e.KEY_M],
    ',': [e.KEY_COMMA],
    '<': [e.KEY_LEFTSHIFT, e.KEY_COMMA],
    '.': [e.KEY_DOT],
    '>': [e.KEY_LEFTSHIFT, e.KEY_DOT],
    '/': [e.KEY_SLASH],
    '?': [e.KEY_LEFTSHIFT, e.KEY_SLASH],
    ' ': [e.KEY_SPACE],
    '\n': [e.KEY_ENTER]
}

# This is enough to get basic functionality. I'm not sure what other
# keys are needed for full functionality.
key_mappings = {
    'control_l': e.KEY_LEFTCTRL,
    'backspace': e.KEY_BACKSPACE
}

class KeyboardEmulationEvDev(Output):
    def __init__(self):
        Output.__init__(self)
        
        if not os.path.exists('/dev/uinput'):
            raise RuntimeError('/dev/uinput does not exist')
        
        if not os.access('/dev/uinput', os.W_OK):
            raise RuntimeError('/dev/uinput is not writable')
        
        self.ui = UInput(
            {
                # FYI for people considering adding more keys: be careful not to
                # add keys above 562, as this will cause the keyboard not to be
                # detected as a keyboard by wlroots window managers such as sway.
                e.EV_KEY: [
                    e.KEY_GRAVE, e.KEY_1, e.KEY_2, e.KEY_3, e.KEY_4, e.KEY_5,
                    e.KEY_6, e.KEY_7, e.KEY_8, e.KEY_9, e.KEY_0, e.KEY_MINUS, e.KEY_EQUAL, e.KEY_BACKSPACE,
                    e.KEY_TAB, e.KEY_Q, e.KEY_W, e.KEY_E, e.KEY_R, e.KEY_T,
                    e.KEY_Y, e.KEY_U, e.KEY_I, e.KEY_O, e.KEY_P, e.KEY_LEFTBRACE, e.KEY_RIGHTBRACE, e.KEY_BACKSLASH,
                    e.KEY_A, e.KEY_S, e.KEY_D, e.KEY_F, e.KEY_G, e.KEY_H,
                    e.KEY_J, e.KEY_K, e.KEY_L, e.KEY_SEMICOLON, e.KEY_APOSTROPHE, e.KEY_ENTER,
                    e.KEY_LEFTSHIFT, e.KEY_Z, e.KEY_X, e.KEY_C, e.KEY_V, e.KEY_B,
                    e.KEY_N, e.KEY_M, e.KEY_COMMA, e.KEY_DOT, e.KEY_SLASH,
                    e.KEY_LEFTCTRL, e.KEY_SPACE,
                ]
            },
            name='plover',
            vendor=1,
            product=1,
            version=1,
            bustype=3,
        )
    
    def send_backspaces(self, count):
        for _ in range(count):
            self.ui.write(e.EV_KEY, e.KEY_BACKSPACE, 1)
            self.ui.write(e.EV_KEY, e.KEY_BACKSPACE, 0)
        self.ui.syn()

    def send_string(self, string):
        for ch in string:
            keys = char_mappings.get(ch, [])
            for k in keys:
                self.ui.write(e.EV_KEY, k, 1)
            for k in reversed(keys):
                self.ui.write(e.EV_KEY, k, 0)
        self.ui.syn()

    def send_key_combination(self, combo):
        for key_name, down in parse_key_combo(combo):
            found_code = key_mappings.get(key_name, None) 
            if found_code is not None:
                self.ui.write(e.EV_KEY, found_code, 1 if down else 0)
        self.ui.syn()

