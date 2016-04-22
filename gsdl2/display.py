from . import sdlconstants


__all__ = [
    'set_mode', 'get_surface', 'flip', 'set_caption',
    'get_window', 'get_renderer', 'set_clear_color', 'clear', 'present', 'Runtime',
]


class Runtime:
    # TODO: is this defeating __del__() in the classes?

        window = None
        renderer = None


def set_mode(resolution=(0, 0), flags=0, depth=0,
             renderer_flags=(sdlconstants.SDL_WINDOW_HIDDEN |
                             sdlconstants.SDL_RENDERER_ACCELERATED |
                             sdlconstants.SDL_RENDERER_TARGETTEXTURE),
             x=sdlconstants.SDL_WINDOWPOS_UNDEFINED, y=sdlconstants.SDL_WINDOWPOS_UNDEFINED):
    if Runtime.window is not None:
        return

    Runtime.window = Window(w=resolution[0], h=resolution[1], flags=flags, x=x, y=y)

    Runtime.renderer = Runtime.window.create_renderer(flags=renderer_flags)

    Runtime.window.show()

    w, h = Runtime.window.surface.get_size()
    Runtime.renderer.logical_size = w, h
    Runtime.renderer.draw_color = 0, 0, 0, 0
    Runtime.renderer.clear()
    Runtime.renderer.present()

    return get_surface()


def get_surface():
    if Runtime.window is not None:
        return Runtime.window.surface


def flip():
    Runtime.window.update_surface()


def set_caption(caption):
    Runtime.window.set_title(caption)


def get_window():
    return Runtime.window


def get_renderer():
    return Runtime.renderer


from .window import Window
