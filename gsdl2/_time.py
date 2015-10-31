__all__ = ['Clock', 'FixedDriver', 'GameClock', 'get_ticks', 'wait', 'delay']


import collections
import sys
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


class Schedule(object):
    """See FixedDriver.new_schedule() docs."""

    def __init__(self, callback, period, due=0, keep_history=False, name=None):
        self._callback = callback
        if period < 0.0:
            period = 0.0
        self.period = period
        self.keep_history = keep_history
        self.name = name
        self._times = collections.deque()
        self._last = time.time()
        if due == 0:
            due = self._last
        elif due == 1:
            due = self._last + period
        self._due = due
        self.interp = 1.0
        self.running = True

    def set_running(self, boolean):
        self.running = boolean

    def tick(self, now, interp):
        fired = False
        if self.period <= 0.0:
            fired = True
        elif now >= self._due:
            last = self._last
            if (self._due - last) * 1000.0 > WORST_CLOCK_ACCURACY:
                self._due = now + self.period
                self._last = now
                # sys.stdout.write('-')
            else:
                period = self.period
                self._due = last + period
                self._last += period
                # sys.stdout.write('+')
            fired = True
        if fired:
            if self.keep_history:
                times = self._times
                times.append(now)
                t_minus = now - 1.0
                while times and times[0] <= t_minus:
                    times.popleft()
            self.interp = interp
            self._callback(self)
        return fired

    def per_second(self):
        return len(self._times)


class FixedDriver(object):
    """
    This is an experimental clock. It is much like GameClock, but it uses significantly less CPU, and still provides
    scheduled callbacks with good accuracy. It supports fixed timestep only. In brief, the FixedDriver provides:
        - one master callback
        - optional ad hoc callbacks, each with its own period
        - optional history on master and ad hoc, to measure rate of fire (FPS)
        - global interpolation based on the master
        - opportunistic sleep cycles to reduce CPU load, without getting too sloppy
        - optional adjustable timestep to simulate time dilation and contraction

    One master callback is required. It runs on a fixed period. It must accept the master's step as its argument:
    callback(step). The master schedule determines global interpolation. The constructor's period argument is the
    timestep in realtime that the master attempts to match. The step argument is the fixed timestep value that is
    returned; this is the same as period by default, but can be used to simulate time dilation and contraction. If the
    master schedule cannot match the realtime period it will run as fast as the CPU allows (slower than optimal) while
    still simulating the fixed time step: so the game will seem to run slower, but the physics should remain stable.

    Changing the period of the master and ad hoc schedules may be done using the provided convenience methods:
    change_master() and change_schedule().

    Ad hoc callbacks can be added via new_schedule() and insert_schedule().

    Each ad hoc schedule calls the callback, passing itself as the argument. The schedule is typically periodic (the
    period argument), but can be 0.0 for a callback that is always fired whenever tick() is called.

    From the Schedule object passed to the callback one can get the period, which can be used as this schedule object's
    fixed time-step, aka dt; and interp, running, and per_second(). Note: per_second() is only active if keep_history is
    True.

    The interpolation value can also be gotten by reading the FixedDriver object's interp after calling tick().

    Tunable: nice is used to calculate opportunistic wait cycles in place of busy cycles. Lower values permit longer
    wait cycles, with somewhat sloppier timing. Gentle values are probably around 10.0. If set too low no wait cycles
    will be inserted (because the calculated wait is always too big to fit in the master's time slice). If set too high
    (100?) the wait cycles will be very, very small and use more CPU, but may gain some accuracy. A value < 1.0 disables
    the feature so that no nice waits will be inserted.

    Usage 1, master callback; the master callback runs everything in sequence:

        def __init__(self):
            clock = FixedDriver(self.update, 1.0 / 60.0)
        def run(self):
            # clock driver
            self.running = True
            while self.running:
                self.clock.tick()
        def update(self, dt):
            # master callback
            update_everything(...)
            draw_everything(...)

    Usage 2, master with ad hoc callbacks; update and draw are decoupled (1 to many), and display entities are
    interpolated:

        def __init__(self):
            # the model runs at 30 times per second
            self.clock = gsdl2.time.FixedDriver(self.update, 1.0 / 30.0, keep_history=False)
            # the display is spammed as fast as possible; save the sched object's per_second() method for convenience
            self.get_fps = self.clock.new_schedule(self.draw, 0.0, keep_history=True).per_second
            # the window caption runs once per second
            self.clock.new_schedule(self.update_caption, 1.0)
        def run(self):
            # clock driver
            self.running = True
            while self.running:
                self.clock.tick()
        def update(self, dt):
            # master callback
            self.update_model(...)  # 30 times / sec
        def update_caption(self, sched):
            # ad hoc callback
            gsdl2.display.set_caption('FPS {}'.format(self.get_fps()))
        def draw(self, sched):
            # ad hoc callback; display uses global interpolation
            self.draw_everything(sched.interp)
    """

    def __init__(self, master, period, keep_history=True, step=None, nice=10.0):
        self.master = master
        self.period = period
        self.keep_history = keep_history
        self._times = collections.deque()
        if step is None:
            self.step = period
        elif step < 0.0:
            self.step = 0.0
        else:
            self.step = step
        self.time = time.time()
        self._elapsed = 0
        self.interp = 0.0
        self._schedules = []
        self._shortest = period

        self.nice = nice
        self._wasted = collections.deque()

    def change_master(self, period, step=None, schedules_too=False):
        if step is None:
            step = period
        self.period = period
        self.step = step
        self._elapsed = 0.0
        if schedules_too:
            for sched in self._schedules:
                self.change_schedule(sched, period)

    @staticmethod
    def change_schedule(sched, period):
        elapsed = sched._due - sched._last
        new_due = min(sched._last + (elapsed / sched.period) * period, period)
        sched.period = period
        sched._due = new_due

    def tick(self):
        """run schedules and return the milliseconds spent"""
        t1 = time.time()
        t0 = self.time
        self.time = t1

        dt = t1 - t0
        ms = dt * 1000.0

        # step the master timer
        step = self.step
        self._elapsed -= dt

        # any_spam detects if any schedules are set to spam (period <= 0.0); if so, then tick() will not sleep
        any_spam = self.period <= 0.0
        any_work = False

        # call the master function on time
        if self._elapsed <= 0.0:
            self.master(step)
            self._elapsed += step
            any_work = True
            # print('')
            if self.keep_history:
                times = self._times
                times.append(t1)
                t_minus = t1 - 1.0
                while times and times[0] <= t_minus:
                    times.popleft()

        # calculate interpolation
        interp = (step - self._elapsed) / step
        if interp < 0.0:
            interp = 0.0
        elif interp > 1.0:
            interp = 1.0
        self.interp = interp

        # run the schedules
        for sched in self._schedules:
            if sched.running and sched.tick(t1, interp):
                any_work = True
                if sched.period <= 0.0:
                    any_spam = True

        # detect wasted cycles and sleep a tiny bit instead of returning immediately
        if not any_spam and self.nice >= 1.0:
            wasted = self._wasted
            if not any_work and dt:
                wasted.append((t1, dt))
            t_minus = t1 - 1.0
            while wasted and wasted[0][0] < t_minus:
                wasted.popleft()
            time_wasted = sum([w for t, w in wasted])
            sleep_secs = time_wasted / (1.0 / self._shortest) / self.nice
            if sleep_secs > 0.0001:  # sleep only if greater than 0.1 ms
                # sys.stdout.write('z')
                time.sleep(sleep_secs)

        return ms

    def per_second(self):
        return len(self._times)

    def new_schedule(self, callback, period, due=0, keep_history=False, pos=None, name=None):
        """create a new schedule and add it to the run list in the specified position

        A schedule calls the callback, passing itself as the argument. The schedule is typically periodic (the period
        argument), but can be 0.0 to create a callback that is always fired when FixedDriver.tick() is called.

        From the Schedule object passed to the callback one can get the period, which can be used as the fixed
        time-step, aka dt; and interp, count, running, and per_second().

        The period is how often, in seconds, the schedule should be called.

        due is the real time (time.time()) when the schedule will first fire. If due is 0, it will be set to
        time.time(). If due is 1, it will be set to time.time() + period.

        If keep_history is True then a one-second history is kept. This enabled a meaningful return value from
        per_second().

        If pos is None, the schedule is appended to the list. Otherwise pos will be inserted as documented for
        list.insert(pos, sched).

        The name is an optional identity to name or group schedules. The name can be used with get_schedules() in order
        to manage or modify them.

        :param callback: callable that will receive dt or varargs
        :param period: float; the timer's interval in seconds
        :param keep_history: boolean; if True, a one-second history is kept that can be read via obj.per_second()
        :param pos: int; insert position in the schedules list
        :return: SteppedSchedule
        """
        if due == 0:
            due = self.time
        sched = Schedule(callback, period, due, keep_history, name)
        self.insert_schedule(sched, pos)
        return sched

    def insert_schedule(self, sched, pos=None):
        """add a Schedule object to the run list in the specified position

        If pos is None, the schedule is appended to the list. Otherwise pos will be inserted as documented for
        list.insert(pos, sched).

        If sched._due == 0 it will be set to the clock's current time.

        No other sanity checking is done on the Schedule object.

        See new_schedule() for additional docs.

        :param sched: a Schedule object
        :param pos: int; insert position in the schedules list
        :return:
        """
        if pos is None:
            self._schedules.append(sched)
        else:
            self._schedules.insert(pos, sched)
        if sched._due == 0:
            sched.__due = self.time
        shortest = self._shortest
        if sched.period < shortest:
            self._shortest = sched.period

        return sched

    def remove_schedule(self, sched):
        """remove the schedule object from the stepped schedules list"""
        try:
            period = sched.period
            self._schedules.remove(sched)
        except (AttributeError, ValueError):
            return

        if period == self._shortest:
            shortest = self.period
            for scheds in self._schedules:
                for sched in scheds:
                    if sched.period < shortest:
                        shortest = sched.period

    def cleanup_idle(self):
        """remove all schedules that have been set_running(False)"""
        remove = self._schedules.remove
        for sched in self._schedules[:]:
            if not sched.running:
                remove(sched)


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
