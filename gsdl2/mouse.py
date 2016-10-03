import sdl
from gsdl2 import display

__all__ = []


class _Internal:
    x = None
    y = None


def get_pressed():
    pass


def get_pos():
    if _Internal.x is None:
        _Internal.x = sdl.ffi.new('int *')
        _Internal.y = sdl.ffi.new('int *')
        sdl.mixer.getMouseState(_Internal.x, _Internal.y)
    return _Internal.x[0], _Internal.y[0]


def get_rel():
    pass


def set_pos(x, y, window=None):
    if window is None:
        window = display.get_window()
    return sdl.mixer.warpMouseInWindow(window.sdl_window, int(x), int(y))


def set_visible(bool):
    bool = 1 if bool else 0
    return sdl.mixer.showCursor(bool)


def get_focused():
    pass


def set_cursor():
    pass


def get_cursor():
    pass
