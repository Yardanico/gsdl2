# README #

### What is this repository for? ###

Note: This project is a reboot of pypygame.

* gsdl2 is a proof-of-concept Pythonic likeness of pygame for SDL2 using pypy and cffi. Some effort is made to keep pygame drop-in compatibility, but there are performance considerations and features new to SDL2 that will factor into decisions.
* Version 0.0 - got a lot of the pygame staples done. Even a demo game, pymike's Bubbman. See downloads. =)

### How do I get set up? ###

* Requires pypy 2.5, cffi, and pycparser. See (http://cffi.readthedocs.org/en/latest/#installation-and-status).
* Summary of set up:
    * (Optional) Install [pypy 2.5](http://pypy.org/download.html)
    * Fix environment to use pypy (e.g. set PATH in Windows, or use virtualenv) so that pip will work
    * Install [pip](https://pip.pypa.io/en/latest/installing.html)
    * pip install [pysdl2-cffi](https://bitbucket.org/dholth/pysdl2-cffi). Or install cffi and pycparser by another means. (Note: this project does not require or use pysdl2-cffi. pysdl2-cffi does provide a nice and easy installation of cffi and pycparser, though.)
    * Install dynamic libraries for [SDL 2.0](https://www.libsdl.org/download-2.0.php), [SDL_image 2.0](https://www.libsdl.org/projects/SDL_image/), [SDL_ttf 2.0](https://www.libsdl.org/projects/SDL_ttf/), and [SDL_mixer 2.0](https://www.libsdl.org/projects/SDL_mixer/).

So far I periodically check that the updates work with CPython 2.7, but the focus is pypy. Probably rects and other spammy bytecode objects are going to require the JIT compiler. Certainly the 20,000 balls in 80_megaballs.py is a CPU killer in CPython.

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

Note to self: [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Who do I talk to? ###

* Gummbum