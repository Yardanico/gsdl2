from .sdl import ffi as sdl_ffi
# from .constants import pypygameerror


__all__ = ['Rect']


class Rect(object):
    # TODO: Optimize the use of cdata with this object.
    # I think creating the cdata is a huge bottleneck for this spammy object. When many rects are created and
    # destroyed it hits the CPU really hard.

    # This is used to iterate slices in __getitem__.
    __i2a = {0: 'x', 1: 'y', 2: 'w', 3: 'h'}

    def __init__(self, *args):
        self.__dim = []
        self.__cdata = sdl_ffi.new('SDL_Rect *')
        if len(args) == 4:
            self.__dim[:] = args[:]
        elif len(args) == 2:
            self.__dim[:2] = args[0][:]
            self.__dim[2:] = args[1][:]
        elif len(args) == 1:
            self.__dim[:] = args[0][:]
        else:
            # TODO: proper exception
            raise Exception('Rect.__init__(): wrong number of arguments')
        d = self.__dim
        c = self.__cdata
        c.x = int(d[0])
        c.y = int(d[1])
        c.w = int(d[2])
        c.h = int(d[3])

    def _get_sdl_rect(self):
        return self.__cdata
    sdl_rect = property(_get_sdl_rect)

    # The following directly access __dim and/or perform calculations:
    #
    # x, left       __dim
    # y, top        __dim
    # right         calculation
    # bottom        calculation
    # w, width      __dim, calculation
    # h, height     __dim, calculation
    # centerx       calculation
    # centery       calculation
    #
    #  The rest get or set their values by the above attributes.

    # simple edges: x, y, left, top, right, bottom

    def __getx(self):
        return self.__dim[0]
    def __setx(self, x):
        self.__dim[0] = x
        self.__cdata.x = int(x)
    x = property(__getx, __setx)
    left = x

    def __gety(self):
        return self.__dim[1]
    def __sety(self, y):
        self.__dim[1] = y
        self.__cdata.y = int(y)
    y = property(__gety, __sety)
    top = y

    def __getright(self):
        return self.x + self.w
    def __setright(self, x):
        self.x = x - self.w
    right = property(__getright, __setright)

    def __getbottom(self):
        return self.y + self.h
    def __setbottom(self, y):
        self.y = y - self.h
    bottom = property(__getbottom, __setbottom)

    # dimensions: w, width, h, height, size

    def __getw(self):
        return self.__dim[2]
    def __setw(self, width):
        self.__dim[2] = width
        self.__cdata.w = width
    w = property(__getw, __setw)
    width = w

    def __geth(self):
        return self.__dim[3]
    def __seth(self, height):
        self.__dim[3] = height
        self.__cdata.h = height
    h = property(__geth, __seth)
    height = h

    def __getsize(self):
        return self.w, self.h
    def __setsize(self, (width, height)):
        self.w = width
        self.h = height
    size = property(__getsize, __setsize)

    # corners: topleft, bottomleft, topright, bottomright

    def __gettopleft(self):
        return self.left, self.top
    def __settopleft(self, (x, y)):
        self.left = x
        self.top = y
    topleft = property(__gettopleft, __settopleft)

    def __getbottomleft(self):
        return self.left, self.bottom
    def __setbottomleft(self, (x, y)):
        self.left = x
        self.bottom = y
    bottomleft = property(__getbottomleft, __setbottomleft)

    def __gettopright(self):
        return self.right, self.top
    def __settopright(self, (x, y)):
        self.right = x
        self.top = y
    topright = property(__gettopright, __settopright)

    def __getbottomright(self):
        return self.right, self.bottom
    def __setbottomright(self, (x, y)):
        self.right = x
        self.bottom = y
    bottomright = property(__getbottomright, __setbottomright)

    # centers: center, centerx, centery, midtop, midleft, midbottom, midright

    def __getcenter(self):
        return self.centerx, self.centery
    def __setcenter(self, (x, y)):
        self.centerx = x
        self.centery = y
    center = property(__getcenter, __setcenter)

    def __getcenterx(self):
        return self.x + self.w // 2
    def __setcenterx(self, x):
        self.x = x - self.w // 2
    centerx = property(__getcenterx, __setcenterx)

    def __getcentery(self):
        return self.y + self.h // 2
    def __setcentery(self, y):
        self.y = y - self.h // 2
    centery = property(__getcentery, __setcentery)

    def __getmidtop(self):
        return self.centerx, self.top
    def __setmidtop(self, (x, y)):
        self.centerx = x
        self.top = y
    midtop = property(__getmidtop, __setmidtop)

    def __getmidleft(self):
        return self.left, self.centery
    def __setmidleft(self, (x, y)):
        self.left = x
        self.centery = y
    midleft = property(__getmidleft, __setmidleft)

    def __getmidbottom(self):
        return self.centerx, self.bottom
    def __setmidbottom(self, (x, y)):
        self.centerx = x
        self.bottom = y
    midbottom = property(__getmidbottom, __setmidbottom)

    def __getmidright(self):
        return self.right, self.centery
    def __setmidright(self, (x, y)):
        self.right = x
        self.centery = y
    midright = property(__getmidright, __setmidright)

    # utilities

    def move(self, x, y):
        r = Rect(self)
        r.x += x
        r.y += y
        return r

    def move_ip(self, x, y):
        self.x += x
        self.y += y

    @staticmethod
    def _do_rect_intersect(a, b):
        # return ((a[0] >= b[0] and a[0] < b[0] + b[2])  or (b[0] >= a[0] and b[0] < a[0] + a[2])) and \
        #     ((a[1] >= b[1] and a[1] < b[1] + b[3])	or (b[1] >= a[1] and b[1] < a[1] + a[3]))
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        ar, ab = ax + aw, ay + ah
        br, bb = bx + bw, by + bh
        return (ax >= bx and ax < br or bx >= ax and bx < ar) and (ay >= by and ay < bb or by >= ay and by < ab)

    def colliderect(self, other):
        return self._do_rect_intersect(self, other)

    # FIXME:
    # def scale_ip(self, factor_x, factor_y):
    #     self.__scale_rect(self, factor_x, factor_y)
    #     return self
    #
    # def scale(self, factor_x, factor_y):
    #     rect = Rect(self)
    #     rect.w = rect.w
    #     self.__scale_rect(rect, factor_x, factor_y)
    #     return rect
    #
    # def __scale_rect(self, rect, factor_x, factor_y):
    #     center = rect.center
    #     x, y, w, h = rect
    #     w *= factor_x
    #     h *= factor_y
    #     rect.w = w
    #     rect.h = h
    #     rect.center = center

    def scale(self, factor_x, factor_y):
        x, y, w, h = self
        w *= factor_x
        h *= factor_y
        rect = Rect(x, y, w, h)
        rect.center = self.center
        return rect

    def __getitem__(self, i):
        return self.__dim[i]

    def __setitem__(self, key, value):
        for i, attr in iter(self.__i2a.items()):
            setattr(self, attr, value[i])

    def __iter__(self):
        return iter(self.__dim)

    def __len__(self):
        return len(self.__dim)

    def __str__(self):
        return '<Rect({}, {}, {}, {})>'.format(*self)
