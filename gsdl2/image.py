import sdl

from gsdl2.surface import Surface
from gsdl2.texture import Texture
from gsdl2.display import get_renderer
from gsdl2.locals import utf8

___all___ = ['load', 'load_texture']


def load(name):
    sdl_surface = sdl.image.load(str(name))
    if sdl_surface == sdl.ffi.NULL:
        raise sdl.SDLError()
    surf = Surface((sdl_surface.w, sdl_surface.h), surface=sdl_surface)
    return surf


def load_texture(name):
    renderer = get_renderer()
    sdl_renderer = renderer.sdl_renderer
    sdl_texture = sdl.image.loadTexture(sdl_renderer, str(name))
    if sdl_texture == sdl.ffi.NULL:
        raise sdl.SDLError()
    texture = Texture(renderer, sdl_texture=sdl_texture)
    return texture


def save(surface, name):
    sdl.image.savePNG(surface.sdl_surface, utf8(name))
