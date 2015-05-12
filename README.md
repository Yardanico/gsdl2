# README #

### What is this repository for? ###

Note: This project is a reboot of pypygame, this time using a manually constructed FFI interface. Personally, I need this because the pkgapi mechanism is not kind to PyCharm's inspection.

gsdl2 is a proof-of-concept Pythonic likeness of pygame for SDL2 using pypy and cffi. Some effort is made to keep pygame drop-in compatibility, but there are performance considerations and features new to SDL2 that will factor into decisions.

Version 0.0 - a lot of the pygame staples are done. Bug warning: here be monsters. I have tried to be thorough in documenting known bugs with FIXME comments.

There is a demo game already, pymike's Bubbman. See downloads. =)

### How do I get set up? ###

* Recommended pypy 2.5, cffi, and pycparser. See (http://cffi.readthedocs.org/en/latest/#installation-and-status).
* Summary of set up:
    * (Optional) Install [pypy 2.5](http://pypy.org/download.html)
    * Fix environment to use pypy (e.g. set PATH in Windows, or use virtualenv) so that pip will work
    * Install [pip](https://pip.pypa.io/en/latest/installing.html)
    * pip install cffi  (if necessary)
    * pip install pycparser
    * Install dynamic libraries for [SDL 2.0](https://www.libsdl.org/download-2.0.php), [SDL_image 2.0](https://www.libsdl.org/projects/SDL_image/), [SDL_ttf 2.0](https://www.libsdl.org/projects/SDL_ttf/), and [SDL_mixer 2.0](https://www.libsdl.org/projects/SDL_mixer/). On Windows, for pypy I simply copied *.dll to the C:\pypy25 folder, and for CPython to the DLLs folder.

So far I periodically check that changes work with CPython 2.7, but the focus is pypy. Probably rects and other spammy bytecode objects are going to require pypy's JIT compiler, or some savvy optimizations for CPython. Certainly the 20,000 balls in 80_megaballs.py is a CPU killer: I can barely get 2,000 in CPython.

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

Note to self: [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Who do I talk to? ###

* Gummbum