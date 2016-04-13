from .sdllibs import image_lib
from .surface import Surface
from .texture import Texture
from .display import get_renderer
from .locals import utf8


___all___ = ['load', 'load_texture']


def load(name):
    sdl_surface = image_lib.IMG_Load(utf8(name))
    surf = Surface((sdl_surface.w, sdl_surface.h), surface=sdl_surface)
    return surf


def load_texture(name):
    sdl_renderer = get_renderer().sdl_renderer
    sdl_texture = image_lib.IMG_LoadTexture(sdl_renderer, utf8(name))
    texture = Texture(sdl_renderer, sdl_texture=sdl_texture)
    return texture


def save(surface, name):
    image_lib.IMG_SavePNG(surface.sdl_surface, utf8(name))
