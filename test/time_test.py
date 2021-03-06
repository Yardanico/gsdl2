#################################### IMPORTS ###################################

if __name__ == '__main__':
    import sys
    import os
    pkg_dir = os.path.split(os.path.abspath(__file__))[0]
    parent_dir, pkg_name = os.path.split(pkg_dir)
    is_pygame_pkg = (pkg_name == 'tests' and
                     os.path.split(parent_dir)[1] == 'gsdl2')
    if not is_pygame_pkg:
        sys.path.insert(0, parent_dir)
else:
    is_pygame_pkg = __name__.startswith('gsdl2.tests.')

if is_pygame_pkg:
    from gsdl2.tests.test_utils import test_not_implemented, unittest
else:
    from test.test_utils import test_not_implemented, unittest
import gsdl2

import time

Clock = gsdl2.time.Clock

################################################################################

class ClockTypeTest(unittest.TestCase):
    def test_construction(self):
        c = Clock()
        self.assert_(c, "Clock can be constructed")
    
    def todo_test_get_fps(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.Clock.get_fps:

          # Clock.get_fps(): return float
          # compute the clock framerate
          # 
          # Compute your game's framerate (in frames per second). It is computed
          # by averaging the last few calls to Clock.tick().
          # 

        self.fail()

        # delay_per_frame = 1 / 100.0
        # 
        # c = Clock()
        # 
        # for f in range(100):
        #     c.tick()
        #     time.sleep(delay_per_frame)
        # 
        # self.assert_(99.0 < c.get_fps() < 101.0)

    def todo_test_get_rawtime(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.Clock.get_rawtime:

          # Clock.get_rawtime(): return milliseconds
          # actual time used in the previous tick
          # 
          # Similar to Clock.get_time(), but this does not include any time used
          # while Clock.tick() was delaying to limit the framerate.
          # 

        self.fail() 

    def todo_test_get_time(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.Clock.get_time:

          # Clock.get_time(): return milliseconds
          # time used in the previous tick
          # 
          # Returns the parameter passed to the last call to Clock.tick(). It is
          # the number of milliseconds passed between the previous two calls to
          # gsdl2.tick().
          # 
        
        self.fail() 

        # c = Clock()
        # c.tick()                    #between   here 
        # time.sleep(0.02)         
        #                                              #get_time()
        # c.tick()                    #          here
        # 
        # time.sleep(0.02)
        # 
        # self.assert_(20 <= c.get_time() <= 30)
        

    def todo_test_tick(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.Clock.tick:

          # Clock.tick(framerate=0): return milliseconds
          # control timer events
          # update the clock
          # 
          # This method should be called once per frame. It will compute how
          # many milliseconds have passed since the previous call.
          # 
          # If you pass the optional framerate argument the function will delay
          # to keep the game running slower than the given ticks per second.
          # This can be used to help limit the runtime speed of a game. By
          # calling Clock.tick(40) once per frame, the program will never run at
          # more than 40 frames per second.
          # 
          # Note that this function uses SDL_Delay function which is not
          # accurate on every platform, but does not use much cpu.  Use
          # tick_busy_loop if you want an accurate timer, and don't mind chewing
          # cpu.
          # 

        self.fail() 

        # collection = []
        # c = Clock()
        # 
        # c.tick()
        # for i in range(100):
        #     time.sleep(0.005)
        #     collection.append(c.tick())
        # 
        # for outlier in [min(collection), max(collection)]:
        #     if outlier != 5: collection.remove(outlier)
        # 
        # self.assert_(sum(collection) / len(collection) == 5)

    def todo_test_tick_busy_loop(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.Clock.tick_busy_loop:

          # Clock.tick_busy_loop(framerate=0): return milliseconds
          # control timer events
          # update the clock
          # 
          # This method should be called once per frame. It will compute how
          # many milliseconds have passed since the previous call.
          # 
          # If you pass the optional framerate argument the function will delay
          # to keep the game running slower than the given ticks per second.
          # This can be used to help limit the runtime speed of a game. By
          # calling Clock.tick(40) once per frame, the program will never run at
          # more than 40 frames per second.
          # 
          # Note that this function uses gsdl2.time.delay, which uses lots of
          # cpu in a busy loop to make sure that timing is more acurate.
          # 
          # New in gsdl2 1.8.0.

        self.fail() 

class TimeModuleTest(unittest.TestCase):
    def todo_test_delay(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.delay:

          # gsdl2.time.delay(milliseconds): return time
          # pause the program for an amount of time
          # 
          # Will pause for a given number of milliseconds. This function will
          # use the processor (rather than sleeping) in order to make the delay
          # more accurate than gsdl2.time.wait().
          # 
          # This returns the actual number of milliseconds used. 

        self.fail() 

    def todo_test_get_ticks(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.get_ticks:

          # gsdl2.time.get_ticks(): return milliseconds
          # get the time in milliseconds
          # 
          # Return the number of millisconds since gsdl2.init() was called.
          # Before gsdl2 is initialized this will always be 0.
          # 

        self.fail() 

    def test_set_timer(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.set_timer:

          # gsdl2.time.set_timer(eventid, milliseconds): return None
          # repeatedly create an event on the event queue
          # 
          # Set an event type to appear on the event queue every given number of
          # milliseconds. The first event will not appear until the amount of
          # time has passed.
          # 
          # Every event type can have a separate timer attached to it. It is
          # best to use the value between gsdl2.USEREVENT and gsdl2.NUMEVENTS.
          # 
          # To disable the timer for an event, set the milliseconds argument to 0.

        # We need to init gsdl2, otherwise we don't actually test anything
        gsdl2.init()
        gsdl2.time.set_timer(gsdl2.USEREVENT, 25)
        # Pause so an event is actually generate
        time.sleep(0.1)
        gsdl2.time.set_timer(gsdl2.USEREVENT, 0)
        events = [x.type for x in gsdl2.event.get() if x.type == gsdl2.USEREVENT]
        # We don't check very tightly on the results, since the timing here isn't
        # very precise, and there's a great deal of scope to be off by one because
        # of that
        self.assertTrue(len(events) >= 2)

    def todo_test_wait(self):

        # __doc__ (as of 2008-08-02) for gsdl2.time.wait:

          # gsdl2.time.wait(milliseconds): return time
          # pause the program for an amount of time
          # 
          # Will pause for a given number of milliseconds. This function sleeps
          # the process to share the processor with other programs. A program
          # that waits for even a few milliseconds will consume very little
          # processor time. It is slightly less accurate than the
          # gsdl2.time.delay() function.
          # 
          # This returns the actual number of milliseconds used. 

        self.fail() 
    
################################################################################

if __name__ == '__main__':
    unittest.main()
