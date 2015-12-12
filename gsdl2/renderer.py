__all__ = ['Renderer']


from .sdllibs import sdl_lib
from .sdlffi import sdl_ffi
#from .window import Window     # see bottom for delayed import
from .rect import Rect


class Renderer(object):

    __src_rect = Rect(0, 0, 1, 1)
    __dst_rect = Rect(0, 0, 1, 1)

    def __init__(self, window, index=-1, flags=0, sdl_renderer=None):
        assert isinstance(window, Window)
        self.__window = window
        if sdl_renderer:
            assert isinstance(sdl_renderer, sdl_ffi.CData)
            self.__sdl_renderer = sdl_renderer
        else:
            self.__sdl_renderer = window.sdl_renderer

    def __getwindow(self):
        return self.__window
    window = property(__getwindow)

    def __getsdlrenderer(self):
        return self.__sdl_renderer
    sdl_renderer = property(__getsdlrenderer)

    def get_logical_size(self):
        return sdl_lib.SDL_RenderGetLogicalSize(self.__sdl_renderer)

    def set_logical_size(self, size):
        sdl_lib.SDL_RenderSetLogicalSize(self.__sdl_renderer, *size)

    def get_draw_color(self):
        return sdl_lib.SDL_GetRenderDrawColor(self.__sdl_renderer)

    def set_draw_color(self, color):
        sdl_lib.SDL_SetRenderDrawColor(self.__sdl_renderer, *color)

    def get_viewport(self):
        return sdl_lib.SDL_RrenderGetViewport(self.__sdl_renderer)

    def set_viewport(self, rect):
        if not isinstance(rect, Rect):
            self.__dst_rect[:] = rect
            rect = self.__dst_rect
        sdl_lib.SDL_RenderSetViewport(self.__sdl_renderer, rect.sdl_rect)

    def get_scale(self):
        return sdl_lib.SDL_RenderGetScale(self.__sdl_renderer)

    def set_scale(self, x, y):
        sdl_lib.SDL_RenderSetScale(self.__sdl_renderer, x, y)

    def clear(self):
        sdl_lib.SDL_RenderClear(self.__sdl_renderer)

    def copy(self, texture, dst_rect, src_rect=None):
        if not isinstance(src_rect, Rect):
            if src_rect is None:
                w, h = texture.size
                src_rect = self.__src_rect
                src_rect[:] = 0, 0, w, h
            elif not isinstance(src_rect, Rect):
                self.__src_rect[:] = src_rect
                src_rect = self.__src_rect
        if not isinstance(dst_rect, Rect):
            self.__dst_rect[:] = dst_rect
            dst_rect = self.__dst_rect
        sdl_lib.SDL_RenderCopy(self.__sdl_renderer, texture.sdl_texture, src_rect.sdl_rect, dst_rect.sdl_rect)

    def copy_ex(self, texture, dst_rect, src_rect, angle, center, flip):
        if not isinstance(src_rect, Rect):
            self.__src_rect[:] = src_rect
            src_rect = self.__src_rect
        if not isinstance(dst_rect, Rect):
            self.__dst_rect[:] = dst_rect
            dst_rect = self.__dst_rect
        if center is None:
            center = sdl_ffi.NULL
        elif not isinstance(center, sdl_ffi.CData):
            center = sdl_ffi.new('SDL_Point const *', center)
        sdl_lib.SDL_RenderCopyEx(
            self.__sdl_renderer, texture.sdl_texture, src_rect.sdl_rect, dst_rect.sdl_rect, angle, center, flip)

    def present(self):
        sdl_lib.SDL_RenderPresent(self.__sdl_renderer)

    def __del__(self):
        # TODO: unreliable
        if self.__sdl_renderer:
            try:
                garbage = self.__sdl_renderer
                self.__sdl_renderer = None
                sdl_lib.SDL_DestroyRenderer(garbage)
            except Exception as e:
                print('error: sdl_lib.SDL_DestroyRenderer() failed')
                print(e)
        else:
            print('gc: renderer is None')


from .window import Window
