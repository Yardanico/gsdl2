# README #

### What is this repository for? ###

Note: This project is a reboot of pypygame, this time using a pysdl2-cffi library.

gsdl2 is a --proof-of-concept-- proven concept Pythonic likeness of pygame for SDL2 using pypy and pysdl2-cffi. Some effort is made to keep pygame drop-in compatibility, but there are performance considerations and features new to SDL2 that will factor into decisions.

Version 0.1 - a lot of the pygame staples are done. Bug warning: here be monsters. I have tried to be thorough in documenting known bugs with FIXME comments.

There are three demo games:

* pymike's Bubbman - action platformer
* gsdl2_shooter - bullets galore
* gsdl2_tol - redux of Trolls Outta Luckland shooter, [Gumm's first pygame](http://www.pygame.org/project-Trolls+Outta+Luckland-1358-2536.html)

See downloads. =)

### How do I get set up? ###

* Recommended pypy 5.4, cffi, and pycparser. See (http://cffi.readthedocs.org/en/latest/#installation-and-status).
* Summary of set up:
    * (Optional) Install [pypy 5.4](http://pypy.org/download.html)
    * Fix environment to use pypy (e.g. set PATH in Windows, or use virtualenv) so that pip will work
    * Install [pip](https://pip.pypa.io/en/latest/installing.html)
    * pip install pysdl2-cffi
    * Install dynamic libraries for [SDL2](https://www.libsdl.org/download-2.0.php), [SDL2_image](https://www.libsdl.org/projects/SDL_image/), [SDL2_ttf](https://www.libsdl.org/projects/SDL_ttf/), [SDL2_mixer](https://www.libsdl.org/projects/SDL_mixer/), and [SDL2_gfx](https://sourceforge.net/projects/sdl2gfx/). On Windows: for pypy I simply copied *.dll to the C:\pypy folder, and for CPython to the C:\Python\DLLs folder. You may need to put the folder in the system path. NEW: for Windows convenience the DLLs are packaged in a sdl_dlls*.zip file; see Downloads.

Here is how I installed SDL2 in Xubuntu 16:

    sudo apt-get install libsdl2-dev
    sudo apt-get install libsdl2-gfx-dev
    sudo apt-get install libsdl2-image-dev
    sudo apt-get install libsdl2-mixer-dev
    sudo apt-get install libsdl2-net-dev
    sudo apt-get install libsdl2-ttf-dev

So far I periodically check that changes work with CPython 2.7, but the focus is pypy. Probably rects and other spammy bytecode objects are going to require pypy's JIT compiler, or some brutal optimizations for CPython. Certainly the 20,000 balls in 80_megaballs.py is a CPU killer: I can barely get 2,000 in CPython.

On one of my Windows 7 + ActivePython 2.7 computers IMG_Load experiences a segfault when run from Cygwin. It may be a configuration issue. The segfault does not occur when I run it from a Windows CMD prompt. I do not have this issue in the same configuration on other computers.

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

Note to self: [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### Who do I talk to? ###

* Gummbum
* Salvakiya
* #pygame on IRC freenode.net
* [pygame-users mailing list](http://www.mail-archive.com/pygame-users@seul.org/)
