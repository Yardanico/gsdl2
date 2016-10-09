import sdl
from gsdl2 import display, SDLError

__all__ = []


def get_pressed():
    """ get_pressed() -> (button1, button2, button3)
    get the state of the mouse buttons
    """
    state, x, y = sdl.getMouseState()
    return (int((state & sdl.BUTTON_LEFT) != 0),
            int((state & sdl.BUTTON_MIDDLE) != 0),
            int((state & sdl.BUTTON_RIGHT) != 0))


def get_pos():
    '''Get mouse position (x and y)'''
    state, x, y = sdl.getMouseState()
    return x, y


def get_mouse_state():
    '''Get mouse state (buttons list [lbm,mmb,rmb] and x, y)'''
    state = get_pressed()
    x, y = get_pos()
    return state, x, y


def set_visible(toggle):
    '''Set visibility of the mouse
        :param toggle 1 - visible; 0 - not visible; -1 - get current state
    '''
    if not isinstance(toggle, int):
        raise TypeError("expected int, got %s" % (toggle,))
    return sdl.showCursor(toggle)


def get_rel():
    """ get_rel() -> (x, y)
    get the amount of mouse movement
    """
    x, y = sdl.getRelativeMouseState()
    return x, y


def set_pos(x, y, window=None):
    if window is None:
        window = display.get_window()
    return sdl.warpMouseInWindow(window.sdl_window, int(x), int(y))

def get_focused():
    """ get_focused() -> bool
    check if the display is receiving mouse input
    """
    return int(sdl.getWindowFlags(display.Runtime.window.sdl_window) & sdl.WINDOW_MOUSE_FOCUS != 0)


def set_cursor(size, hotspot, xormasks, andmasks):
    """ set_cursor(size, hotspot, xormasks, andmasks) -> None
    set the image for the system mouse cursor
    """
    spotx, spoty = int(hotspot[0]), int(hotspot[1])
    w, h = int(size[0]), int(size[1])
    if w % 8 != 0:
        raise ValueError("Cursor width must be divisible by 8")

    if not hasattr(xormasks, '__iter__') or not hasattr(andmasks, '__iter__'):
        raise TypeError("xormask and andmask must be sequences")
    if len(xormasks) != w * h / 8.0 or len(andmasks) != w * h / 8.0:
        raise ValueError("bitmasks must be sized width*height/8")
    try:
        xordata = sdl.ffi.new('uint8_t[]', [int(m) for m in xormasks])
        anddata = sdl.ffi.new('uint8_t[]', [int(andmasks[i]) for i
                                            in range(len(xormasks))])
    except (ValueError, TypeError):
        raise TypeError("Invalid number in mask array")
    except OverflowError:
        raise TypeError("Number in mask array is larger than 8 bits")

    cursor = sdl.createCursor(xordata, anddata, w, h, spotx, spoty)
    if not cursor:
        raise SDLError()
    lastcursor = sdl.getCursor()
    sdl.setCursor(cursor)
    sdl.freeCursor(lastcursor)


def get_cursor():
    pass
