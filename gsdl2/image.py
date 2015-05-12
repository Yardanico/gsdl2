from .sdllibs import image_lib
from .surface import Surface
from .locals import utf8


___all___ = ['load']


def load(name):
    img = image_lib.IMG_Load(utf8(name))
    surf = Surface((img.w, img.h), surface=img)
    return surf


def save(surface, name):
    image_lib.IMG_SavePNG(surface.sdl_surface, utf8(name))
