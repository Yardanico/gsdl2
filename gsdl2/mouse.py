from .sdllibs import sdl_lib, sdl_ffi
from . import display


__all__ = []


class _Internal:
    x = None
    y = None


def get_pressed():
    pass


def get_pos():
    if _Internal.x is None:
        _Internal.x = sdl_ffi.new('int *')
        _Internal.y = sdl_ffi.new('int *')
    sdl_lib.SDL_GetMouseState(_Internal.x, _Internal.y)
    return _Internal.x[0], _Internal.y[0]


def get_rel():
    pass


def set_pos(x, y, window=None):
    if window is None:
        window = display.get_window()
    return sdl_lib.SDL_WarpMouseInWindow(window.sdl_window, int(x), int(y))


def set_visible(bool):
    bool = 1 if bool else 0
    return sdl_lib.SDL_ShowCursor(bool)


def get_focused():
    pass


def set_cursor():
    pass


def get_cursor():
    pass
