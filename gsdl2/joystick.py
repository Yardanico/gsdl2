import sdl
from _sdl.structs import SDLError

from gsdl2.sdlffi import to_string
from .sdlconstants import SDL_INIT_JOYSTICK, SDL_HAT_UP, SDL_HAT_DOWN, SDL_HAT_RIGHT, SDL_HAT_LEFT


def init():
    # register auto_quit
    pass


def quit():
    # auto_quit
    pass


def get_init():
    return sdl.wasInit(SDL_INIT_JOYSTICK) != 0


def get_count():
    return sdl.numJoysticks()


class Joystick(object):
    # TODO: test this; I only have an Xbox 360

    def __init__(self, num):
        self.__num = num
        self.__sdl_joystick = None

    def init(self):
        self.__sdl_joystick = sdl.joystickOpen(self.__num)
        if self.__sdl_joystick == sdl.ffi.NULL:
            raise SDLError()

    def quit(self):
        sdl.joystickClose(self.__num)

    def get_id(self):
        return self.__num

    def get_name(self):
        return to_string(sdl.joystickNameForIndex(self.__num))

    def get_numaxes(self):
        return sdl_lib.SDL_JoystickNumAxes(self.__num)

    def get_axis(self, axis):
        return sdl_lib.SDL_JoystickGetAxis(self.__num, axis)

    def get_numballs(self):
        return sdl_lib.SDL_JoystickNumBalls(self.__num)

    def get_ball(self, ball):
        dx = sdl_ffi.new('Uint16 *')
        dy = sdl_ffi.new('Uint16 *')
        sdl_lib.SDL_JoystickGetBall(self.__num, ball, dx, dy)
        return dx[0], dy[0]

    def get_numbuttons(self):
        return sdl_lib.SDL_JoystickNumButtons(self.__num)

    def get_button(self, button):
        return sdl_lib.SDL_JoystickGetButton(self.__num, button)

    def get_numhats(self):
        return sdl_lib.SDL_JoystickNumHats(self.__num)

    def get_hat(self, hat):
        value = sdl_lib.SDL_JoystickGetHat(self.__num, hat)
        px, py = 0, 0
        if value & SDL_HAT_UP:
            py = 1
        elif value & SDL_HAT_DOWN:
            py = -1
        elif value & SDL_HAT_RIGHT:
            px = 1
        elif value & SDL_HAT_LEFT:
            px = -1
        return px, py

    def __get_sdl_joystick(self):
        return self.__sdl_joystick

    sdl_joystick = property(__get_sdl_joystick)
