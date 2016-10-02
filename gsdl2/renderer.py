import _sdl
import sdl

__all__ = ['Renderer']


#from .window import Window     # see bottom for delayed import
from .rect import Rect
from .color import Color


class Renderer(object):

    __src_rect = Rect(0, 0, 1, 1)
    __dst_rect = Rect(0, 0, 1, 1)

    def __init__(self, window, index=-1, flags=0, sdl_renderer=None):
        assert isinstance(window, Window)
        self.__window = window
        if sdl_renderer:
            assert isinstance(sdl_renderer, _sdl.autohelpers.SDL_Renderer)
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
        return sdl.renderGetLogicalSize(self.__sdl_renderer)
    def set_logical_size(self, size):
        sdl.renderSetLogicalSize(self.__sdl_renderer, *size)
    logical_size = property(get_logical_size, set_logical_size)

    def get_draw_color(self):
        r, g, b, a = [sdl.ffi.new('Uint8 *') for i in range(4)]
        sdl.getRenderDrawColor(self.__sdl_renderer, r, g, b, a)
        return Color(r[0], g[0], b[0], a[0])
    def set_draw_color(self, color):
        sdl.setRenderDrawColor(self.__sdl_renderer, *color)
    draw_color = property(get_draw_color, set_draw_color)

    def get_viewport(self):
        return sdl.renderGetViewport(self.__sdl_renderer)
    def set_viewport(self, rect):
        if not isinstance(rect, Rect):
            self.__dst_rect[:] = rect
            rect = self.__dst_rect
        sdl.renderSetViewport(self.__sdl_renderer, rect.sdl_rect)
    viewport = property(get_viewport, set_viewport)

    def get_scale(self):
        return sdl.renderGetScale(self.__sdl_renderer)
    def set_scale(self, size):
        sdl.renderSetScale(self.__sdl_renderer, *size)
    scale = property(get_scale, set_scale)

    def get_target(self):
        """NOTE: this returns a SDL_Texture, not a gsdl2.texture.Texture
        """
        return sdl.getRenderTarget(self.sdl_renderer)

    def set_target(self, texture=None, sdl_texture=None):
        if texture:
            return sdl.setRenderTarget(self.sdl_renderer, texture.sdl_texture)
        elif sdl_texture:
            return sdl.setRenderTarget(self.sdl_renderer, sdl_texture)
        else:
            return sdl.setRenderTarget(self.sdl_renderer, sdl.ffi.NULL)

    def get_blendmode(self):
        blendmode = sdl.ffi.new('SDL_BlendMode *')
        sdl.getRenderDrawBlendMode(self.sdl_renderer, blendmode)
        value = int(blendmode[0])
        return value
    def set_blendmode(self, blendmode):
        sdl.setRenderDrawBlendMode(self.sdl_renderer, blendmode)
    blendmode = property(get_blendmode, set_blendmode)

    def fill(self, color, texture=None):
        restore_target = None
        if texture:
            restore_target = self.get_target()
            self.set_target(texture)
        restore_blendmode = self.get_blendmode()
        restore_draw_color = self.get_draw_color()
        # restore_blendmode = texture.get_blendmode()

        self.set_blendmode(sdl.BLENDMODE_NONE)
        self.set_draw_color(color)
        sdl.renderFillRect(self.sdl_renderer, sdl.ffi.NULL)

        self.set_blendmode(restore_blendmode)
        self.set_draw_color(restore_draw_color)
        # texture.set_blendmode(restore_blendmode)
        if restore_target:
            self.set_target(sdl_texture=restore_target)

    def clear(self):
        sdl.renderClear(self.__sdl_renderer)

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
        sdl.renderCopy(self.__sdl_renderer, texture.sdl_texture, src_rect.sdl_rect, dst_rect.sdl_rect)

    def copy_ex(self, texture, dst_rect, src_rect, angle, center, flip):
        if not isinstance(src_rect, Rect):
            self.__src_rect[:] = src_rect
            src_rect = self.__src_rect
        if not isinstance(dst_rect, Rect):
            self.__dst_rect[:] = dst_rect
            dst_rect = self.__dst_rect
        if center is None:
            center = sdl.ffi.NULL
        elif not isinstance(center, sdl.ffi.CData):
            center = sdl.ffi.new('SDL_Point const *', center)
        sdl.renderCopyEx(
            self.__sdl_renderer, texture.sdl_texture, src_rect.sdl_rect, dst_rect.sdl_rect, angle, center, flip)

    def present(self):
        sdl.renderPresent(self.__sdl_renderer)

    def __del__(self):
        # TODO: unreliable
        if self.__sdl_renderer:
            try:
                garbage = self.__sdl_renderer
                self.__sdl_renderer = None
                sdl.destroyRenderer(garbage)
            except Exception as e:
                print('error: sdl_lib.SDL_DestroyRenderer() failed')
                print(e)
        else:
            print('gc: renderer is None')


from .window import Window
