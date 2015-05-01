__all__ = ['Clock', 'GameClock', 'get_ticks', 'wait', 'delay']


import collections
import time


from .sdllibs import sdl_lib
from .gameclock import GameClock


WORST_CLOCK_ACCURACY = 12

_start_time = time.time()


class Clock(object):

    def __init__(self):
        self._times = collections.deque()
        self._last_time = time.time()
        self._dt = 0
        self._raw = 0
        self._history = 1.0

    def tick(self, fps=0):
        t1 = time.time()
        t0 = self._last_time
        self._last_time = t1

        times = self._times
        times.append(t1)
        t_minus = t1 - self._history
        while times[0] <= t_minus:
            times.popleft()

        if fps <= 0:
            ms = (t1 - t0) * 1000.0
            self._raw = 0
        else:
            dt = 1.0 / fps
            ms = _accurate_delay(dt * 1000)
            self._raw = ms - dt * 1000

        self._dt = ms
        return ms

    def tick_busy_loop(self, fps=0):
        # TODO
        return self.tick(fps)

    def get_time(self):
        return int(self._dt)

    def get_raw_time(self):
        # TODO: did I do this right?
        return self._raw

    def get_fps(self):
        return len(self._times) // int(self._history)


def get_ticks():
    return int((time.time() - _start_time) * 1000.0)


def wait(ms):
    sdl_lib.SDL_Delay(int(ms))
    return time.time()


def delay(ms):
    _accurate_delay(ms)
    return time.time()


def set_timer(eventid, ms):
    # TODO
    raise NotImplemented


def _accurate_delay(ticks):
    ticks = int(ticks)
    if ticks <= 0:
        return 0

    funcstart = sdl_lib.SDL_GetTicks ()
    if ticks >= WORST_CLOCK_ACCURACY:
        delay = (ticks - 2) - (ticks % WORST_CLOCK_ACCURACY)
        if delay >= WORST_CLOCK_ACCURACY:
            sdl_lib.SDL_Delay(delay)
    else:
        delay = ticks

    while delay > 0:
        delay = ticks - (sdl_lib.SDL_GetTicks () - funcstart)

    return sdl_lib.SDL_GetTicks () - funcstart
