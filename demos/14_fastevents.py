#!/usr/bin/env python
"""  This is a stress test for the fastevents module.

*Fast events does not appear faster!*

So far it looks like normal pygame.event is faster by up to two times.
So maybe fastevent isn't fast at all.

Tested on windowsXP sp2 athlon, and freebsd.

However... on my debian duron 850 machine fastevents is faster.
"""

# the config to try different settings out with the event queues.

# TODO: re-enable when the fastevent module is implemented
# use the fastevent module or not.
try:
    import gsdl2 as pygame
    from gsdl2 import event, USEREVENT, time

    use_fast_events = 0
except:
    import pygame
    from pygame import event, USEREVENT, time
    import pygame.fastevent as fastevent

    use_fast_events = 1

# limit the game loop to 60 fps.
slow_tick = 1

# I'm able to get 200,000 events/s on my PC with fastevent
# Without it 100,000 events/s
# With gsdl2 - 1mil events/s - maybe because of SDL2
NUM_EVENTS_TO_POST = 2000000

if use_fast_events:
    event_module = fastevent
else:
    event_module = event

from threading import Thread


class post_them(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.done = []
        self.stop = []

    def run(self):
        self.done = []
        self.stop = []
        for x in range(NUM_EVENTS_TO_POST):
            ee = event.Event(USEREVENT)
            try_post = 1

            # the pygame.event.post raises an exception if the event
            #   queue is full.  so wait a little bit, and try again.
            while try_post:
                try:
                    event_module.post(ee)
                    try_post = 0
                except:
                    pytime.sleep(0.001)
                    try_post = 1

            if self.stop:
                return
        self.done.append(1)


import time as pytime


def main():
    pygame.init()

    if use_fast_events:
        fastevent.init()
    clock = time.Clock()

    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("fastevent Workout")

    poster = post_them()

    t1 = pytime.time()
    poster.start()

    going = True
    while going:
        #        for e in event.get():
        # for x in range(200):
        #    ee = event.Event(USEREVENT)
        #    r = event_module.post(ee)
        #    print (r)

        # for e in event_module.get():
        event_list = []
        event_list = event_module.get()

        for e in event_list:
            if e.type == pygame.QUIT:
                print (clock.get_fps())
                poster.stop.append(1)
                going = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    print(clock.get_fps())
                    poster.stop.append(1)
                    going = False
        if poster.done:
            print (clock.get_fps())
            t2 = pytime.time()
            print ("total time:%s" % (t2 - t1))
            print ("events/second:%s" % (NUM_EVENTS_TO_POST / (t2 - t1)))
            going = False
        if with_display:
            pygame.display.flip()
        if slow_tick:
            clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
