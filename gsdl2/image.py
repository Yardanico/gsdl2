from .sdllibs import image_lib
from .surface import Surface


___all___ = ['load']


def load(name):
    img = image_lib.IMG_Load(name)
    surf = Surface((img.w, img.h), surface=img)
    return surf


def save(surface, name):
    image_lib.IMG_SavePNG(surface.sdl_surface, name)
