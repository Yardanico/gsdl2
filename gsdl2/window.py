import logging

import sdl

from sdl import WINDOWPOS_UNDEFINED, WINDOW_FULLSCREEN, WINDOW_FULLSCREEN_DESKTOP
from gsdl2.locals import utf8

__all__ = ['Window']

open_windows = []


# log = logging.getLogger(__name__)


def get_list():
    return list(open_windows)


class Window(object):
    def __init__(self, title='gsdl2', x=WINDOWPOS_UNDEFINED, y=WINDOWPOS_UNDEFINED, w=0, h=0, flags=0):
        self.__sdl_window = sdl.createWindow(utf8(title), x, y, w, h, flags)
        open_windows.append(self)

    def __getsurface(self):
        surface = sdl.getWindowSurface(self.__sdl_window)
        return Surface((surface.w, surface.h), surface=surface)

    surface = property(__getsurface)

    def create_renderer(self, index=-1, flags=sdl.RENDERER_ACCELERATED):
        renderer = sdl.createRenderer(self.__sdl_window, index, flags)
        return Renderer(self, sdl_renderer=renderer)

    def show(self):
        sdl.showWindow(self.__sdl_window)

    def update_surface(self):
        sdl.updateWindowSurface(self.__sdl_window)

    def set_title(self, title):
        sdl.setWindowTitle(self.__sdl_window, utf8(title))

    def set_fullscreen(self, bool):
        flag = WINDOW_FULLSCREEN if bool else 0
        sdl.setWindowFullscreen(self.sdl_window, flag)

    def set_fullscreen_desktop(self, bool):
        flag = WINDOW_FULLSCREEN_DESKTOP if bool else 0
        sdl.setWindowFullscreen(self.sdl_window, flag)

    def close(self):
        if self in open_windows:
            open_windows.remove(self)
        sdl_window = self.__sdl_window
        sdl.destroyWindow(sdl_window)
        self.__sdl_window = None

    def __getrenderer(self):
        return sdl.getRenderer(self.__sdl_window)

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
                sdl.destroyWindow(garbage)
            except Exception as e:
                # log.info('sdl_lib.SDL_DestroyWindow() failed')
                # log.info(e)
                pass


from gsdl2.renderer import Renderer
from gsdl2.surface import Surface
