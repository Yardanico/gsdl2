import sdl
from gsdl2 import display

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


def set_cursor():
    pass


def get_cursor():
    pass
