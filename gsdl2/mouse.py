import sdl
from gsdl2 import display, SDLError

__all__ = []


def get_pressed():
    pass


def get_pos():
    state, x, y = sdl.getMouseState()
    return x, y


def get_rel():
    pass


def set_pos(x, y, window=None):
    if window is None:
        window = display.get_window()
    return sdl.warpMouseInWindow(window.sdl_window, int(x), int(y))


def set_visible(bool):
    bool = 1 if bool else 0
    return sdl.showCursor(bool)


def get_focused():
    pass


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
