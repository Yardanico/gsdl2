import sdl

# taken from pygame-cffi
def get_pressed():
    """ get_pressed() -> bools
    get the state of all keyboard buttons
    """
    if not sdl.wasInit(sdl.INIT_EVERYTHING):
        raise Exception("SDL isn't inited")
    num_keys = sdl.ffi.new('int*')
    key_state = sdl.getKeyboardState(num_keys)[0]
    num_keys = num_keys[0]
    if not key_state or not num_keys:
        return None
    return [key_state[i] for i in range(num_keys)]