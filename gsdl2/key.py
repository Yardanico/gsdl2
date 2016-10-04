import sdl

# taken from pygame-cffi
def get_pressed():
    """ get_pressed() -> bools
    get the state of all keyboard buttons
    """
    if not sdl.wasInit(sdl.INIT_EVERYTHING):
        raise Exception("SDL isn't inited")
    return sdl.getKeyboardState()[0]