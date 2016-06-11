import logging

from .sdllibs import sdl_lib
from .sdlconstants import SDL_WINDOWPOS_UNDEFINED, SDL_WINDOW_FULLSCREEN, SDL_WINDOW_FULLSCREEN_DESKTOP
from .locals import utf8


__all__ = ['Window']


open_windows = []

# log = logging.getLogger(__name__)


def get_list():
    return list(open_windows)


class Window(object):

    def __init__(self, title='gsdl2', x=SDL_WINDOWPOS_UNDEFINED, y=SDL_WINDOWPOS_UNDEFINED, w=0, h=0, flags=0):
        self.__sdl_window = sdl_lib.SDL_CreateWindow(utf8(title), x, y, w, h, flags)
        open_windows.append(self)

    def __getsurface(self):
        surface = sdl_lib.SDL_GetWindowSurface(self.__sdl_window)
        return Surface((surface.w, surface.h), surface=surface)
    surface = property(__getsurface)

    def create_renderer(self, index=-1, flags=sdl_lib.SDL_RENDERER_ACCELERATED):
        renderer = sdl_lib.SDL_CreateRenderer(self.__sdl_window, index, flags)
        return Renderer(self, sdl_renderer=renderer)

    def show(self):
        sdl_lib.SDL_ShowWindow(self.__sdl_window)

    def update_surface(self):
        sdl_lib.SDL_UpdateWindowSurface(self.__sdl_window)

    def set_title(self, title):
        sdl_lib.SDL_SetWindowTitle(self.__sdl_window, utf8(title))

    def set_fullscreen(self, bool):
        flag = SDL_WINDOW_FULLSCREEN if bool else 0
        sdl_lib.SDL_SetWindowFullscreen(self.sdl_window, flag)

    def set_fullscreen_desktop(self, bool):
        flag = SDL_WINDOW_FULLSCREEN_DESKTOP if bool else 0
        sdl_lib.SDL_SetWindowFullscreen(self.sdl_window, flag)

    def close(self):
        if self in open_windows:
            open_windows.remove(self)
        sdl_window = self.__sdl_window
        sdl_lib.SDL_DestroyWindow(sdl_window)
        self.__sdl_window = None

    def __getrenderer(self):
        return sdl_lib.SDL_GetRenderer(self.__sdl_window)
    sdl_renderer = property(__getrenderer)

    def __getsdlwindow(self):
        return self.__sdl_window
    sdl_window = property(__getsdlwindow)

    def __del__(self):
        # TODO: unreliable
        if self.__sdl_window:
            try:
                garbage = self.__sdl_window
                self.__sdl_window = None
                sdl_lib.SDL_DestroyWindow(garbage)
            except Exception as e:
                # log.info('sdl_lib.SDL_DestroyWindow() failed')
                # log.info(e)
                pass


from .renderer import Renderer
from .surface import Surface
