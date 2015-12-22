from .color import Color
from .rect import Rect



import sys
if sys.version_info[0] == 2:
    def utf8(text):
        """Convert text to UTF-8 for Python 2."""
        if not isinstance(text, unicode):
            return text.encode('utf-8')
        return text
else:
    def utf8(text):
        """Convert text to UTF-8 for Python 3."""
        return text.encode('utf-8')
del sys

#
#  Event Types (event.type)
#

FIRSTEVENT = 0                  # Unused (do not remove)
NOEVENT = FIRSTEVENT            # Gumm note: Pygame legacy?

# Application events
QUIT = 0x100                    # User-requested quit

# These application events have special meaning on iOS, see README-ios.txt for details
APP_TERMINATING = 0x101             # The application is being terminated by the OS Called on iOS in
                                        #  applicationWillTerminate() Called on Android in onDestroy()
APP_LOWMEMORY = 0x102               # The application is low on memory, free memory if possible. Called on iOS in
                                        #  applicationDidReceiveMemoryWarning() Called on Android in onLowMemory()
APP_WILLENTERBACKGROUND = 0x103     # The application is about to enter the background Called on iOS in
                                        #  applicationWillResignActive(); Called on Android in onPause()
APP_DIDENTERBACKGROUND = 0x104      # The application did enter the background and may not get CPU for some time
                                        #  Called on iOS in applicationDidEnterBackground() Called on Android in
                                        #  onPause()
APP_WILLENTERFOREGROUND = 0x105     # The application is about to enter the foreground Called on iOS in
                                        #  applicationWillEnterForeground() Called on Android in onResume()
APP_DIDENTERFOREGROUND = 0x106      # The application is now interactive Called on iOS in
                                        #  applicationDidBecomeActive() Called on Android in onResume()
# Window events
WINDOWEVENT = 0x200             # Window state change
SYSWMEVENT = 0x201              # System specific event
# Keyboard events
KEYDOWN = 0x300                 # Key pressed
KEYUP = 0x301                   # Key released
TEXTEDITING = 0x302             # Keyboard text editing (composition)
TEXTINPUT = 0x303               # Keyboard text input
# Mouse events
MOUSEMOTION = 0x400             # Mouse moved
MOUSEBUTTONDOWN = 0x401         # Mouse button pressed
MOUSEBUTTONUP = 0x402           # Mouse button released
MOUSEWHEEL = 0x403              # Mouse wheel motion
# Joystick events
JOYAXISMOTION = 0x600           # Joystick axis motion
JOYBALLMOTION = 0x601           # Joystick trackball motion
JOYHATMOTION = 0x602            # Joystick hat position change
JOYBUTTONDOWN = 0x603           # Joystick button pressed
JOYBUTTONUP = 0x604             # Joystick button released
JOYDEVICEADDED = 0x605          # A new joystick has been inserted into the system
JOYDEVICEREMOVED = 0x606        # An opened joystick has been removed
# Game controller events
CONTROLLERAXISMOTION = 0x650    # Game controller axis motion
CONTROLLERBUTTONDOWN = 0x651    # Game controller button pressed
CONTROLLERBUTTONUP = 0x652      # Game controller button released
CONTROLLERDEVICEADDED = 0x653   # A new Game controller has been inserted into the system
CONTROLLERDEVICEREMOVED = 0x654     # An opened Game controller has been removed
CONTROLLERDEVICEREMAPPED = 0x655    # The controller mapping was updated
# Touch events
FINGERDOWN = 0x700
FINGERUP = 0x701
FINGERMOTION = 0x702
# Gesture events
DOLLARGESTURE = 0x800
DOLLARRECORD = 0x801
MULTIGESTURE = 0x802
# Clipboard events
CLIPBOARDUPDATE = 0x900         # The clipboard changed
# Drag and drop events
DROPFILE = 0x1000               # The system requests a file open
# Render events
RENDER_TARGETS_RESET = 0x2000   # The render targets have been reset

#Events ::SDL_USEREVENT through ::SDL_LASTEVENT are for your use, and should be allocated with SDL_RegisterEvents()
USEREVENT = 0x8000

# This last event is only for bounding internal arrays
LASTEVENT = 0xFFFF


#
#  Keyboard Scancodes (event.scancode)
#

S_UNKNOWN = 0
S_A = 4
S_B = 5
S_C = 6
S_D = 7
S_E = 8
S_F = 9
S_G = 10
S_H = 11
S_I = 12
S_J = 13
S_K = 14
S_L = 15
S_M = 16
S_N = 17
S_O = 18
S_P = 19
S_Q = 20
S_R = 21
S_S = 22
S_T = 23
S_U = 24
S_V = 25
S_W = 26
S_X = 27
S_Y = 28
S_Z = 29
S_1 = 30
S_2 = 31
S_3 = 32
S_4 = 33
S_5 = 34
S_6 = 35
S_7 = 36
S_8 = 37
S_9 = 38
S_0 = 39
S_RETURN = 40
S_ESCAPE = 41
S_BACKSPACE = 42
S_TAB = 43
S_SPACE = 44
S_MINUS = 45
S_EQUALS = 46
S_LEFTBRACKET = 47
S_RIGHTBRACKET = 48
S_BACKSLASH = 49
S_NONUSHASH = 50
S_SEMICOLON = 51
S_APOSTROPHE = 52
S_GRAVE = 53
S_COMMA = 54
S_PERIOD = 55
S_SLASH = 56
S_CAPSLOCK = 57
S_F1 = 58
S_F2 = 59
S_F3 = 60
S_F4 = 61
S_F5 = 62
S_F6 = 63
S_F7 = 64
S_F8 = 65
S_F9 = 66
S_F10 = 67
S_F11 = 68
S_F12 = 69
S_PRINTSCREEN = 70
S_SCROLLLOCK = 71
S_PAUSE = 72
S_INSERT = 73
S_HOME = 74
S_PAGEUP = 75
S_DELETE = 76
S_END = 77
S_PAGEDOWN = 78
S_RIGHT = 79
S_LEFT = 80
S_DOWN = 81
S_UP = 82
S_NUMLOCKCLEAR = 83
S_KP_DIVIDE = 84
S_KP_MULTIPLY = 85
S_KP_MINUS = 86
S_KP_PLUS = 87
S_KP_ENTER = 88
S_KP_1 = 89
S_KP_2 = 90
S_KP_3 = 91
S_KP_4 = 92
S_KP_5 = 93
S_KP_6 = 94
S_KP_7 = 95
S_KP_8 = 96
S_KP_9 = 97
S_KP_0 = 98
S_KP_PERIOD = 99
S_NONUSBACKSLASH = 100
S_APPLICATION = 101
S_POWER = 102
S_KP_EQUALS = 103
S_F13 = 104
S_F14 = 105
S_F15 = 106
S_F16 = 107
S_F17 = 108
S_F18 = 109
S_F19 = 110
S_F20 = 111
S_F21 = 112
S_F22 = 113
S_F23 = 114
S_F24 = 115
S_EXECUTE = 116
S_HELP = 117
S_MENU = 118
S_SELECT = 119
S_STOP = 120
S_AGAIN = 121
S_UNDO = 122
S_CUT = 123
S_COPY = 124
S_PASTE = 125
S_FIND = 126
S_MUTE = 127
S_VOLUMEUP = 128
S_VOLUMEDOWN = 129
S_KP_COMMA = 133
S_KP_EQUALSAS400 = 134

S_INTERNATIONAL1 = 135
S_INTERNATIONAL2 = 136
S_INTERNATIONAL3 = 137
S_INTERNATIONAL4 = 138
S_INTERNATIONAL5 = 139
S_INTERNATIONAL6 = 140
S_INTERNATIONAL7 = 141
S_INTERNATIONAL8 = 142
S_INTERNATIONAL9 = 143
S_LANG1 = 144
S_LANG2 = 145
S_LANG3 = 146
S_LANG4 = 147
S_LANG5 = 148
S_LANG6 = 149
S_LANG7 = 150
S_LANG8 = 151
S_LANG9 = 152
S_ALTERASE = 153
S_SYSREQ = 154
S_CANCEL = 155
S_CLEAR = 156
S_PRIOR = 157
S_RETURN2 = 158
S_SEPARATOR = 159
S_OUT = 160
S_OPER = 161
S_CLEARAGAIN = 162
S_CRSEL = 163
S_EXSEL = 164
S_KP_00 = 176
S_KP_000 = 177
S_THOUSANDSSEPARATOR = 178
S_DECIMALSEPARATOR = 179
S_CURRENCYUNIT = 180
S_CURRENCYSUBUNIT = 181
S_KP_LEFTPAREN = 182
S_KP_RIGHTPAREN = 183
S_KP_LEFTBRACE = 184
S_KP_RIGHTBRACE = 185
S_KP_TAB = 186
S_KP_BACKSPACE = 187
S_KP_A = 188
S_KP_B = 189
S_KP_C = 190
S_KP_D = 191
S_KP_E = 192
S_KP_F = 193
S_KP_XOR = 194
S_KP_POWER = 195
S_KP_PERCENT = 196
S_KP_LESS = 197
S_KP_GREATER = 198
S_KP_AMPERSAND = 199
S_KP_DBLAMPERSAND = 200
S_KP_VERTICALBAR = 201
S_KP_DBLVERTICALBAR = 202
S_KP_COLON = 203
S_KP_HASH = 204
S_KP_SPACE = 205
S_KP_AT = 206
S_KP_EXCLAM = 207
S_KP_MEMSTORE = 208
S_KP_MEMRECALL = 209
S_KP_MEMCLEAR = 210
S_KP_MEMADD = 211
S_KP_MEMSUBTRACT = 212
S_KP_MEMMULTIPLY = 213
S_KP_MEMDIVIDE = 214
S_KP_PLUSMINUS = 215
S_KP_CLEAR = 216
S_KP_CLEARENTRY = 217
S_KP_BINARY = 218
S_KP_OCTAL = 219
S_KP_DECIMAL = 220
S_KP_HEXADECIMAL = 221
S_LCTRL = 224
S_LSHIFT = 225
S_LALT = 226
S_LGUI = 227
S_RCTRL = 228
S_RSHIFT = 229
S_RALT = 230
S_RGUI = 231
S_MODE = 257
S_AUDIONEXT = 258
S_AUDIOPREV = 259
S_AUDIOSTOP = 260
S_AUDIOPLAY = 261
S_AUDIOMUTE = 262
S_MEDIASELECT = 263
S_WWW = 264
S_MAIL = 265
S_CALCULATOR = 266
S_COMPUTER = 267
S_AC_SEARCH = 268
S_AC_HOME = 269
S_AC_BACK = 270
S_AC_FORWARD = 271
S_AC_STOP = 272
S_AC_REFRESH = 273
S_AC_BOOKMARKS = 274
S_BRIGHTNESSDOWN = 275
S_BRIGHTNESSUP = 276
S_DISPLAYSWITCH = 277
S_KBDILLUMTOGGLE = 278
S_KBDILLUMDOWN = 279
S_KBDILLUMUP = 280
S_EJECT = 281
S_SLEEP = 282
S_APP1 = 283
S_APP2 = 284
NUM_SCANCODES = 512


# SDL 1.2-style Keyboard KeySyms (event.key)

K_UNKNOWN = 0
K_RETURN = 13
K_ESCAPE = 27
K_BACKSPACE = 8
K_TAB = 9
K_SPACE = 32
K_EXCLAIM = 33
K_QUOTEDBL = 34
K_HASH = 35
K_PERCENT = 37
K_DOLLAR = 36
K_AMPERSAND = 38
K_QUOTE = 39
K_LEFTPAREN = 40
K_RIGHTPAREN = 41
K_ASTERISK = 42
K_PLUS = 43
K_COMMA = 44
K_MINUS = 45
K_PERIOD = 46
K_SLASH = 47
K_0 = 48
K_1 = 49
K_2 = 50
K_3 = 51
K_4 = 52
K_5 = 53
K_6 = 54
K_7 = 55
K_8 = 56
K_9 = 57
K_COLON = 58
K_SEMICOLON = 59
K_LESS = 60
K_EQUALS = 61
K_GREATER = 62
K_QUESTION = 63
K_AT = 64
K_LEFTBRACKET = 91
K_BACKSLASH = 92
K_RIGHTBRACKET = 93
K_CARET = 94
K_UNDERSCORE = 95
K_BACKQUOTE = 96
K_a = 97
K_b = 98
K_c = 99
K_d = 100
K_e = 101
K_f = 102
K_g = 103
K_h = 104
K_i = 105
K_j = 106
K_k = 107
K_l = 108
K_m = 109
K_n = 110
K_o = 111
K_p = 112
K_q = 113
K_r = 114
K_s = 115
K_t = 116
K_u = 117
K_v = 118
K_w = 119
K_x = 120
K_y = 121
K_z = 122
K_CAPSLOCK = 1073741881
K_F1 = 1073741882
K_F2 = 1073741883
K_F3 = 1073741884
K_F4 = 1073741885
K_F5 = 1073741886
K_F6 = 1073741887
K_F7 = 1073741888
K_F8 = 1073741889
K_F9 = 1073741890
K_F10 = 1073741891
K_F11 = 1073741892
K_F12 = 1073741893
K_PRINTSCREEN = 1073741894
K_SCROLLLOCK = 1073741895
K_PAUSE = 1073741896
K_INSERT = 1073741897
K_HOME = 1073741898
K_PAGEUP = 1073741899
K_DELETE = 127
K_END = 1073741901
K_PAGEDOWN = 1073741902
K_RIGHT = 1073741903
K_LEFT = 1073741904
K_DOWN = 1073741905
K_UP = 1073741906
K_NUMLOCKCLEAR = 1073741907
K_KP_DIVIDE = 1073741908
K_KP_MULTIPLY = 1073741909
K_KP_MINUS = 1073741910
K_KP_PLUS = 1073741911
K_KP_ENTER = 1073741912
K_KP_1 = 1073741913
K_KP_2 = 1073741914
K_KP_3 = 1073741915
K_KP_4 = 1073741916
K_KP_5 = 1073741917
K_KP_6 = 1073741918
K_KP_7 = 1073741919
K_KP_8 = 1073741920
K_KP_9 = 1073741921
K_KP_0 = 1073741922
K_KP_PERIOD = 1073741923
K_APPLICATION = 1073741925
K_POWER = 1073741926
K_KP_EQUALS = 1073741927
K_F13 = 1073741928
K_F14 = 1073741929
K_F15 = 1073741930
K_F16 = 1073741931
K_F17 = 1073741932
K_F18 = 1073741933
K_F19 = 1073741934
K_F20 = 1073741935
K_F21 = 1073741936
K_F22 = 1073741937
K_F23 = 1073741938
K_F24 = 1073741939
K_EXECUTE = 1073741940
K_HELP = 1073741941
K_MENU = 1073741942
K_SELECT = 1073741943
K_STOP = 1073741944
K_AGAIN = 1073741945
K_UNDO = 1073741946
K_CUT = 1073741947
K_COPY = 1073741948
K_PASTE = 1073741949
K_FIND = 1073741950
K_MUTE = 1073741951
K_VOLUMEUP = 1073741952
K_VOLUMEDOWN = 1073741953
K_KP_COMMA = 1073741957
K_KP_EQUALSAS400 = 1073741958
K_ALTERASE = 1073741977
K_SYSREQ = 1073741978
K_CANCEL = 1073741979
K_CLEAR = 1073741980
K_PRIOR = 1073741981
K_RETURN2 = 1073741982
K_SEPARATOR = 1073741983
K_OUT = 1073741984
K_OPER = 1073741985
K_CLEARAGAIN = 1073741986
K_CRSEL = 1073741987
K_EXSEL = 1073741988
K_KP_00 = 1073742000
K_KP_000 = 1073742001
K_THOUSANDSSEPARATOR = 1073742002
K_DECIMALSEPARATOR = 1073742003
K_CURRENCYUNIT = 1073742004
K_CURRENCYSUBUNIT = 1073742005
K_KP_LEFTPAREN = 1073742006
K_KP_RIGHTPAREN = 1073742007
K_KP_LEFTBRACE = 1073742008
K_KP_RIGHTBRACE = 1073742009
K_KP_TAB = 1073742010
K_KP_BACKSPACE = 1073742011
K_KP_A = 1073742012
K_KP_B = 1073742013
K_KP_C = 1073742014
K_KP_D = 1073742015
K_KP_E = 1073742016
K_KP_F = 1073742017
K_KP_XOR = 1073742018
K_KP_POWER = 1073742019
K_KP_PERCENT = 1073742020
K_KP_LESS = 1073742021
K_KP_GREATER = 1073742022
K_KP_AMPERSAND = 1073742023
K_KP_DBLAMPERSAND = 1073742024
K_KP_VERTICALBAR = 1073742025
K_KP_DBLVERTICALBAR = 1073742026
K_KP_COLON = 1073742027
K_KP_HASH = 1073742028
K_KP_SPACE = 1073742029
K_KP_AT = 1073742030
K_KP_EXCLAM = 1073742031
K_KP_MEMSTORE = 1073742032
K_KP_MEMRECALL = 1073742033
K_KP_MEMCLEAR = 1073742034
K_KP_MEMADD = 1073742035
K_KP_MEMSUBTRACT = 1073742036
K_KP_MEMMULTIPLY = 1073742037
K_KP_MEMDIVIDE = 1073742038
K_KP_PLUSMINUS = 1073742039
K_KP_CLEAR = 1073742040
K_KP_CLEARENTRY = 1073742041
K_KP_BINARY = 1073742042
K_KP_OCTAL = 1073742043
K_KP_DECIMAL = 1073742044
K_KP_HEXADECIMAL = 1073742045
K_LCTRL = 1073742048
K_LSHIFT = 1073742049
K_LALT = 1073742050
K_LGUI = 1073742051
K_RCTRL = 1073742052
K_RSHIFT = 1073742053
K_RALT = 1073742054
K_RGUI = 1073742055
K_MODE = 1073742081
K_AUDIONEXT = 1073742082
K_AUDIOPREV = 1073742083
K_AUDIOSTOP = 1073742084
K_AUDIOPLAY = 1073742085
K_AUDIOMUTE = 1073742086
K_MEDIASELECT = 1073742087
K_WWW = 1073742088
K_MAIL = 1073742089
K_CALCULATOR = 1073742090
K_COMPUTER = 1073742091
K_AC_SEARCH = 1073742092
K_AC_HOME = 1073742093
K_AC_BACK = 1073742094
K_AC_FORWARD = 1073742095
K_AC_STOP = 1073742096
K_AC_REFRESH = 1073742097
K_AC_BOOKMARKS = 1073742098
K_BRIGHTNESSDOWN = 1073742099
K_BRIGHTNESSUP = 1073742100
K_DISPLAYSWITCH = 1073742101
K_KBDILLUMTOGGLE = 1073742102
K_KBDILLUMDOWN = 1073742103
K_KBDILLUMUP = 1073742104
K_EJECT = 1073742105
K_SLEEP = 1073742106


# Keyboard Metakeys (event.mod)

KMOD_NONE = 0x0000
KMOD_LSHIFT = 0x0001
KMOD_RSHIFT = 0x0002
KMOD_LCTRL = 0x0040
KMOD_RCTRL = 0x0080
KMOD_LALT = 0x0100
KMOD_RALT = 0x0200
KMOD_LGUI = 0x0400
KMOD_RGUI = 0x0800
KMOD_NUM = 0x1000
KMOD_CAPS = 0x2000
KMOD_MODE = 0x4000
KMOD_RESERVED = 0x8000

KMOD_CTRL = KMOD_LCTRL | KMOD_RCTRL
KMOD_SHIFT = KMOD_LSHIFT | KMOD_RSHIFT
KMOD_ALT = KMOD_LALT | KMOD_RALT
KMOD_GUI = KMOD_LGUI | KMOD_RGUI


# Surface constants

SWSURFACE = 0           # Just here for compatibility
PREALLOC = 0x00000001   # Surface uses preallocated memory
RLEACCEL = 0x00000002   # Surface is RLE encoded
DONTFREE = 0x00000004   # Surface is referenced internally


palette_8bit = (
    (0, 0, 0, 255),
    (0, 0, 85, 255),
    (0, 0, 170, 255),
    (0, 0, 255, 255),
    (0, 36, 0, 255),
    (0, 36, 85, 255),
    (0, 36, 170, 255),
    (0, 36, 255, 255),
    (0, 73, 0, 255),
    (0, 73, 85, 255),
    (0, 73, 170, 255),
    (0, 73, 255, 255),
    (0, 109, 0, 255),
    (0, 109, 85, 255),
    (0, 109, 170, 255),
    (0, 109, 255, 255),
    (0, 146, 0, 255),
    (0, 146, 85, 255),
    (0, 146, 170, 255),
    (0, 146, 255, 255),
    (0, 182, 0, 255),
    (0, 182, 85, 255),
    (0, 182, 170, 255),
    (0, 182, 255, 255),
    (0, 219, 0, 255),
    (0, 219, 85, 255),
    (0, 219, 170, 255),
    (0, 219, 255, 255),
    (0, 255, 0, 255),
    (0, 255, 85, 255),
    (0, 255, 170, 255),
    (0, 255, 255, 255),
    (85, 0, 0, 255),
    (85, 0, 85, 255),
    (85, 0, 170, 255),
    (85, 0, 255, 255),
    (85, 36, 0, 255),
    (85, 36, 85, 255),
    (85, 36, 170, 255),
    (85, 36, 255, 255),
    (85, 73, 0, 255),
    (85, 73, 85, 255),
    (85, 73, 170, 255),
    (85, 73, 255, 255),
    (85, 109, 0, 255),
    (85, 109, 85, 255),
    (85, 109, 170, 255),
    (85, 109, 255, 255),
    (85, 146, 0, 255),
    (85, 146, 85, 255),
    (85, 146, 170, 255),
    (85, 146, 255, 255),
    (85, 182, 0, 255),
    (85, 182, 85, 255),
    (85, 182, 170, 255),
    (85, 182, 255, 255),
    (85, 219, 0, 255),
    (85, 219, 85, 255),
    (85, 219, 170, 255),
    (85, 219, 255, 255),
    (85, 255, 0, 255),
    (85, 255, 85, 255),
    (85, 255, 170, 255),
    (85, 255, 255, 255),
    (170, 0, 0, 255),
    (170, 0, 85, 255),
    (170, 0, 170, 255),
    (170, 0, 255, 255),
    (170, 36, 0, 255),
    (170, 36, 85, 255),
    (170, 36, 170, 255),
    (170, 36, 255, 255),
    (170, 73, 0, 255),
    (170, 73, 85, 255),
    (170, 73, 170, 255),
    (170, 73, 255, 255),
    (170, 109, 0, 255),
    (170, 109, 85, 255),
    (170, 109, 170, 255),
    (170, 109, 255, 255),
    (170, 146, 0, 255),
    (170, 146, 85, 255),
    (170, 146, 170, 255),
    (170, 146, 255, 255),
    (170, 182, 0, 255),
    (170, 182, 85, 255),
    (170, 182, 170, 255),
    (170, 182, 255, 255),
    (170, 219, 0, 255),
    (170, 219, 85, 255),
    (170, 219, 170, 255),
    (170, 219, 255, 255),
    (170, 255, 0, 255),
    (170, 255, 85, 255),
    (170, 255, 170, 255),
    (170, 255, 255, 255),
    (255, 0, 0, 255),
    (255, 0, 85, 255),
    (255, 0, 170, 255),
    (255, 0, 255, 255),
    (255, 36, 0, 255),
    (255, 36, 85, 255),
    (255, 36, 170, 255),
    (255, 36, 255, 255),
    (255, 73, 0, 255),
    (255, 73, 85, 255),
    (255, 73, 170, 255),
    (255, 73, 255, 255),
    (255, 109, 0, 255),
    (255, 109, 85, 255),
    (255, 109, 170, 255),
    (255, 109, 255, 255),
    (255, 146, 0, 255),
    (255, 146, 85, 255),
    (255, 146, 170, 255),
    (255, 146, 255, 255),
    (255, 182, 0, 255),
    (255, 182, 85, 255),
    (255, 182, 170, 255),
    (255, 182, 255, 255),
    (255, 219, 0, 255),
    (255, 219, 85, 255),
    (255, 219, 170, 255),
    (255, 219, 255, 255),
    (255, 255, 0, 255),
    (255, 255, 85, 255),
    (255, 255, 170, 255),
    (255, 255, 255, 255),
    (0, 0, 0, 255),
    (0, 0, 85, 255),
    (0, 0, 170, 255),
    (0, 0, 255, 255),
    (0, 36, 0, 255),
    (0, 36, 85, 255),
    (0, 36, 170, 255),
    (0, 36, 255, 255),
    (0, 73, 0, 255),
    (0, 73, 85, 255),
    (0, 73, 170, 255),
    (0, 73, 255, 255),
    (0, 109, 0, 255),
    (0, 109, 85, 255),
    (0, 109, 170, 255),
    (0, 109, 255, 255),
    (0, 146, 0, 255),
    (0, 146, 85, 255),
    (0, 146, 170, 255),
    (0, 146, 255, 255),
    (0, 182, 0, 255),
    (0, 182, 85, 255),
    (0, 182, 170, 255),
    (0, 182, 255, 255),
    (0, 219, 0, 255),
    (0, 219, 85, 255),
    (0, 219, 170, 255),
    (0, 219, 255, 255),
    (0, 255, 0, 255),
    (0, 255, 85, 255),
    (0, 255, 170, 255),
    (0, 255, 255, 255),
    (85, 0, 0, 255),
    (85, 0, 85, 255),
    (85, 0, 170, 255),
    (85, 0, 255, 255),
    (85, 36, 0, 255),
    (85, 36, 85, 255),
    (85, 36, 170, 255),
    (85, 36, 255, 255),
    (85, 73, 0, 255),
    (85, 73, 85, 255),
    (85, 73, 170, 255),
    (85, 73, 255, 255),
    (85, 109, 0, 255),
    (85, 109, 85, 255),
    (85, 109, 170, 255),
    (85, 109, 255, 255),
    (85, 146, 0, 255),
    (85, 146, 85, 255),
    (85, 146, 170, 255),
    (85, 146, 255, 255),
    (85, 182, 0, 255),
    (85, 182, 85, 255),
    (85, 182, 170, 255),
    (85, 182, 255, 255),
    (85, 219, 0, 255),
    (85, 219, 85, 255),
    (85, 219, 170, 255),
    (85, 219, 255, 255),
    (85, 255, 0, 255),
    (85, 255, 85, 255),
    (85, 255, 170, 255),
    (85, 255, 255, 255),
    (170, 0, 0, 255),
    (170, 0, 85, 255),
    (170, 0, 170, 255),
    (170, 0, 255, 255),
    (170, 36, 0, 255),
    (170, 36, 85, 255),
    (170, 36, 170, 255),
    (170, 36, 255, 255),
    (170, 73, 0, 255),
    (170, 73, 85, 255),
    (170, 73, 170, 255),
    (170, 73, 255, 255),
    (170, 109, 0, 255),
    (170, 109, 85, 255),
    (170, 109, 170, 255),
    (170, 109, 255, 255),
    (170, 146, 0, 255),
    (170, 146, 85, 255),
    (170, 146, 170, 255),
    (170, 146, 255, 255),
    (170, 182, 0, 255),
    (170, 182, 85, 255),
    (170, 182, 170, 255),
    (170, 182, 255, 255),
    (170, 219, 0, 255),
    (170, 219, 85, 255),
    (170, 219, 170, 255),
    (170, 219, 255, 255),
    (170, 255, 0, 255),
    (170, 255, 85, 255),
    (170, 255, 170, 255),
    (170, 255, 255, 255),
    (255, 0, 0, 255),
    (255, 0, 85, 255),
    (255, 0, 170, 255),
    (255, 0, 255, 255),
    (255, 36, 0, 255),
    (255, 36, 85, 255),
    (255, 36, 170, 255),
    (255, 36, 255, 255),
    (255, 73, 0, 255),
    (255, 73, 85, 255),
    (255, 73, 170, 255),
    (255, 73, 255, 255),
    (255, 109, 0, 255),
    (255, 109, 85, 255),
    (255, 109, 170, 255),
    (255, 109, 255, 255),
    (255, 146, 0, 255),
    (255, 146, 85, 255),
    (255, 146, 170, 255),
    (255, 146, 255, 255),
    (255, 182, 0, 255),
    (255, 182, 85, 255),
    (255, 182, 170, 255),
    (255, 182, 255, 255),
    (255, 219, 0, 255),
    (255, 219, 85, 255),
    (255, 219, 170, 255),
    (255, 219, 255, 255),
    (255, 255, 0, 255),
    (255, 255, 85, 255),
    (255, 255, 170, 255),
    (255, 255, 255, 255),
)