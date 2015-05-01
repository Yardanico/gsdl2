import gsdl2

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption('00_window.py - Window will close in 4 seconds...')

gsdl2.time.wait(4000)
