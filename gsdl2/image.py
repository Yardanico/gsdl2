from . import sdllibs
from .surface import Surface
from .texture import Texture
from .display import get_renderer
from .locals import utf8


___all___ = ['load', 'load_texture']


def load(name):
    sdl_surface = sdllibs.image_lib.IMG_Load(str(name))
    if sdl_surface == sdllibs.sdl_ffi.NULL:
        raise sdllibs.SDLError()
    surf = Surface((sdl_surface.w, sdl_surface.h), surface=sdl_surface)
    return surf


def load_texture(name):
    renderer = get_renderer()
    sdl_renderer = renderer.sdl_renderer
    sdl_texture = sdllibs.image_lib.IMG_LoadTexture(sdl_renderer, str(name))
    if sdl_texture == sdllibs.sdl_ffi.NULL:
        raise sdllibs.SDLError()
    texture = Texture(renderer, sdl_texture=sdl_texture)
    return texture


def save(surface, name):
    sdllibs.image_lib.IMG_SavePNG(surface.sdl_surface, utf8(name))
