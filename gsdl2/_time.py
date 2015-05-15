__all__ = ['Clock', 'FixedDriver', 'GameClock', 'get_ticks', 'wait', 'delay']


import collections
import time


from .sdllibs import sdl_lib
from .gameclock import GameClock


WORST_CLOCK_ACCURACY = 12

_start_time = time.time()


class Clock(object):
    """just yer basic clock, a la pygame"""

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


def _schedule_sort_key(self):
    return self._due


class SteppedSchedule(object):

    __slots__ = ['_callback', 'period', 'step', 'keep_history', '_due', '_last', '_times']

    def __init__(self, callback, period, step, due, keep_history):
        self._callback = callback
        self.period = period
        self.step = step
        self.keep_history = keep_history
        self._times = collections.deque()
        self._due = due
        self._last = due

    def tick(self, now):
        fired = False
        if self.period <= 0.0:
            fired = True
        elif now >= self._due:
            fired = True
            self._callback(self.step)
            last = self._last
            if (self._due - last) * 1000.0 > WORST_CLOCK_ACCURACY:
                self._due = now + self.period
                self._last = now
            else:
                self._due = self._last + self.period
                self._last += self.period
        if fired and self.keep_history:
            times = self._times
            times.append(now)
            t_minus = now - 1.0
            while times and times[0] <= t_minus:
                times.popleft()
        return fired

    def per_second(self):
        return len(self._times) // 1


class InterpolatedSchedule(object):

    __slots__ = ['_callback', 'period', 'keep_history', '_due', '_last', '_times']

    def __init__(self, callback, period, due, keep_history):
        self._callback = callback
        self.period = period
        self.keep_history = keep_history
        self._times = collections.deque()
        self._due = due
        self._last = due

    def tick(self, now, interp):
        fired = False
        if self.period <= 0.0:
            fired = True
        elif now >= self._due:
            self._callback(interp)
            last = self._last
            if (self._due - last) * 1000.0 > WORST_CLOCK_ACCURACY:
                self._due = now + self.period
                self._last = now
            else:
                self._due = self._last + self.period
                self._last += self.period
            fired = True
        if fired and self.keep_history:
            times = self._times
            times.append(now)
            t_minus = now - 1.0
            while times and times[0] <= t_minus:
                times.popleft()
        return fired

    def per_second(self):
        return len(self._times)


class FixedDriver(object):
    """
    This is an experimental clock. It is much like GameClock, but it uses significantly less CPU, and still provides
    scheduled callbacks with good accuracy. It supports fixed timestep only.

    One master callback is required. It runs on a fixed schedule. It must accept the master's period as its argument:
    callback(dt).

    Additional callbacks can be added. Stepped schedules pass the fixed period for the schedule: callback(dt).
    Interpolated schedules pass the interpolation value between the previous and current timestep for the master's
    period: callback(interp).

    Stepped schedules are run before interpolated schedules. This probably isn't a concern, but it is worth mentioning
    in case one expects one of each that use the same period to fire in a particular order. If synchronization of two or
    more callables is needed, it is best to wrap them in a single scheduled callback.

    The interpolation value can also be gotten by reading clock.interp after calling clock.tick().

    Usage 1, master callback; the master calls everything in sequence:

        def __init__(self):
            clock = FixedDriver(self.update, 1.0 / 60.0, 1.0 / 60.0)
        def run(self):
            # clock driver
            self.running = True
            while self.running:
                self.clock.tick()
        def update(self, dt):
            # master callback
            self.update_game()
            self.draw()
        def draw(self):
            self.draw_everything(...)  # every time master is called

    Usage 2, master with extra callbacks; update and draw are decoupled (1 to many), and display entities are
    interpolated:

        def __init__(self):
            self.clock = gsdl2.time.FixedDriver(self.update, 1.0 / 30.0, 1.0 / 30.0)
            sched = self.clock.schedule_interpolated(self.draw, 0.0, keep_history=True, nice=0.0)
            self.draw_sched = sched  # save this so we can report the FPS
            self.clock.schedule_stepped(self.update_caption, 1.0)
        def run(self):
            # clock driver
            self.running = True
            while self.running:
                self.clock.tick()
        def update(self, dt):
            # maser callback
            self.update_model(...)  # 30 times / sec
        def update_caption(self, dt):
            # callback
            gsdl2.display.set_caption('FPS {}'.format(self.draw_sched.per_second()))
        def draw(self, interp):
            # callback
            self.draw_everything(...)  # as fast as CPU can handle
    """

    def __init__(self, master, period, step, nice=10.0):
        self.clock = Clock()
        self.master = master
        self.period = period
        self.step = step
        self._last_time = time.time()
        self._elapsed = 0
        self.interp = 0.0
        # TODO: make these a heapq?
        # callbacks
        self._interpolated = []
        self._stepped = []
        self._shortest = period

        # Tunable: nice is used to calculate opportunistic wait cycles in place of busy cycles. Lower values permit
        # longer wait cycles, i.e. somewhat sloppier timing. Gentle values are probably around 10.0. If you set it too
        # low no wait cycles will be imposed. If you set it too high (100?) the wait cycles will be very, very small and
        # use more CPU, but should gain some accuracy. A value < 1.0 disables the feature.
        #
        # If you have a schedule with a period of 0.0 it makes no sense to use nice. In this case turn if off.
        self.nice = nice
        self._wasted = collections.deque()

    def tick(self):
        t1 = time.time()
        t0 = self._last_time
        self._last_time = t1

        dt = t1 - t0
        ms = dt * 1000.0

        # step the master timer
        step = self.step
        self._elapsed -= dt

        any_work = False

        # call the master function on time
        if self._elapsed <= 0.0:
            self.master(self.step)
            self._elapsed += step
            any_work = True

        # calculate interpolation
        interp = (self.step - self._elapsed) / step
        if interp < 0.0:
            interp = 0.0
        elif interp > 1.0:
            interp = 1.0
        self.interp = interp

        # run the stepped schedules
        sort_me = False
        for sched in self._stepped:
            if sched.tick(t1):
                sort_me = True
            else:
                break
        if sort_me:
            # TODO: sort would only be required to optimize a great number of timers
            # self._stepped.sort(key=_schedule_sort_key)
            any_work = True

        # run the interpolated schedules
        sort_me = False
        for sched in self._interpolated:
            if sched.tick(t1, interp):
                sort_me = True
            else:
                break
        if sort_me:
            # TODO: sort would only be required to optimize a great number of timers
            # self._interpolated.sort(key=_schedule_sort_key)
            any_work = True

        # TODO: EXPERIMENTAL: detect wasted cycles and sleep a tiny bit instead of returning immediately
        # this sacrifices a little accuracy to use less CPU
        if self.nice >= 1.0:
            wasted = self._wasted
            if not any_work and dt:
                wasted.append((t1, dt))
            t_minus = t1 - 1.0
            while wasted and wasted[0][0] < t_minus:
                wasted.popleft()
            time_wasted = sum([w for t, w in wasted])
            # if time_wasted:
            #     print('time_wasted={:0.4f}'.format(time_wasted))
            sleep_secs = time_wasted / (1.0 / self._shortest) / self.nice
            if sleep_secs > 0.0001:  # sleep only if greater than 0.1 ms
                # print('zzz', sleep_secs)
                time.sleep(sleep_secs)

        return ms

    def schedule_stepped(self, callback, period, step=0.0, keep_history=False):
        """set a stepped schedule

        Returns a SteppedSchedule object.

        A stepped schedule calls the callback, passing step as dt each period. The schedule is typically periodic (the
        period argument), but can be 0.0 to create a callback that is always spammed.

        In order to read the history one must save the returned object and call its per_second() method.

        :param callback: callable that will receive dt or varargs
        :param period: float; the timer's interval in seconds
        :param step: float; the timestep (dt) the timer will provide to the caller
        :param keep_history: boolean; if True, a one-second history is kept that can be read via obj.per_second()
        :return: SteppedSchedule
        """
        if period < 0.0:
            period = 0.0
        if step < 0.0:
            step = 0.0
        due = time.time() + period
        sched = SteppedSchedule(callback, period, step, due, keep_history)
        self._insert_stepped(sched)
        return sched

    def schedule_interpolated(self, callback, period=0.0, keep_history=False):
        """set an interpolated schedule

        Returns an InterpolatedSchedule object.

        An interpolated schedule calls the callback, passing the interpolation value for that moment. The interpolation
        value is the position between 0.0 and 1.0 in the current timestep of the master. The schedule can be periodic
        (the period argument), but can be 0.0 to create a callback that is always spammed.

        In order to read the history one must save the returned object and call its per_second() method.

        :param callback: callable that will receive dt or varargs
        :param period: float; the timer's interval in seconds
        :param keep_history: boolean; if True, a one-second history is kept that can be read via obj.per_second()
        :return: InterpolatedSchedule
        """
        if period < 0.0:
            period = 0.0
        due = time.time() + period
        sched = InterpolatedSchedule(callback, period, due, keep_history)
        self._insert_interpolated(sched)
        return sched

    def remove_stepped(self, sched):
        """remove the schedule object from the stepped schedules list"""
        try:
            period = sched.period
            self._stepped.remove(sched)
        except (AttributeError, ValueError):
            return
        if period == self._shortest:
            shortest = self.period
            for scheds in self._stepped, self._interpolated:
                for sched in scheds:
                    if sched.period < shortest:
                        shortest = sched.period

    def remove_interpolated(self, sched):
        """remove the schedule object from the interpolated schedules list"""
        try:
            period = sched.period
            self._interpolated.remove(sched)
        except (AttributeError, ValueError):
            return
        if period == self._shortest:
            shortest = self.period
            for scheds in self._stepped, self._interpolated:
                for sched in scheds:
                    if sched.period < shortest:
                        shortest = sched.period

    def _insert_stepped(self, sched):
        self._stepped.append(sched)
        # self._stepped.sort(key=_schedule_sort_key)
        shortest = self._shortest
        if sched.period < shortest:
            self._shortest = sched.period

    def _insert_interpolated(self, sched):
        self._interpolated.append(sched)
        # self._interpolated.sort(key=_schedule_sort_key)
        shortest = self._shortest
        if sched.period < shortest:
            self._shortest = sched.period


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
