# from .constants import pypygameerror
import sdl

__all__ = ['Rect']


class Rect(object):
    # TODO: Optimize the use of cdata with this object.
    # I think creating the cdata is a huge bottleneck for this spammy object. When many rects are created and
    # destroyed it hits the CPU really hard.

    # __slots__ = ['__i2a', '__sdl_rect']

    # This is used to iterate slices in __getitem__.
    __i2a = {0: 'x', 1: 'y', 2: 'w', 3: 'h'}

    def __init__(self, *args):
        # self.__dim = []
        self.__sdl_rect = sdl.ffi.new('SDL_Rect *')
        r = self
        if len(args) == 4:
            r.x, r.y, r.w, r.h = args
        elif len(args) == 2:
            r.x, r.y = args[0]
            r.w, r.h = args[1]
        elif len(args) == 1:
            # self.__dim[:] = args[0][:]
            r.x, r.y, r.w, r.h = args[0]
        else:
            # TODO: proper exception
            raise Exception('Rect.__init__(): wrong number of arguments')

    def __get_sdl_rect(self):
        return self.__sdl_rect

    sdl_rect = property(__get_sdl_rect)

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
        return self.__sdl_rect.x

    def __setx(self, x):
        self.__sdl_rect.x = int(x)

    x = property(__getx, __setx)
    left = x

    def __gety(self):
        return self.__sdl_rect.y

    def __sety(self, y):
        self.__sdl_rect.y = int(y)

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
        return self.__sdl_rect.w

    def __setw(self, width):
        self.__sdl_rect.w = int(width)

    w = property(__getw, __setw)
    width = w

    def __geth(self):
        return self.__sdl_rect.h

    def __seth(self, height):
        self.__sdl_rect.h = int(height)

    h = property(__geth, __seth)
    height = h

    def __getsize(self):
        return self.w, self.h

    def __setsize(self, size):
        self.w, self.h = size

    size = property(__getsize, __setsize)

    # corners: topleft, bottomleft, topright, bottomright

    def __gettopleft(self):
        return self.left, self.top

    def __settopleft(self, pos):
        self.left, self.top = pos

    topleft = property(__gettopleft, __settopleft)

    def __getbottomleft(self):
        return self.left, self.bottom

    def __setbottomleft(self, pos):
        self.left, self.bottom = pos

    bottomleft = property(__getbottomleft, __setbottomleft)

    def __gettopright(self):
        return self.right, self.top

    def __settopright(self, pos):
        self.right, self.top = pos

    topright = property(__gettopright, __settopright)

    def __getbottomright(self):
        return self.right, self.bottom

    def __setbottomright(self, pos):
        self.right, self.bottom = pos

    bottomright = property(__getbottomright, __setbottomright)

    # centers: center, centerx, centery, midtop, midleft, midbottom, midright

    def __getcenter(self):
        return self.centerx, self.centery

    def __setcenter(self, pos):
        self.centerx, self.centery = pos

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

    def __setmidtop(self, pos):
        self.centerx, self.top = pos

    midtop = property(__getmidtop, __setmidtop)

    def __getmidleft(self):
        return self.left, self.centery

    def __setmidleft(self, pos):
        self.left, self.centery = pos

    midleft = property(__getmidleft, __setmidleft)

    def __getmidbottom(self):
        return self.centerx, self.bottom

    def __setmidbottom(self, pos):
        self.centerx, self.bottom = pos

    midbottom = property(__getmidbottom, __setmidbottom)

    def __getmidright(self):
        return self.right, self.centery

    def __setmidright(self, pos):
        self.right, self.centery = pos

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

    def inflate(self, x, y):
        return Rect(self.x - x // 2, self.y - y // 2, self.w + x, self.h + y)

    def inflate_ip(self, x, y):
        self.x -= x / 2
        self.y -= y / 2
        self.w += x
        self.h += y

    def copy(self):
        return Rect(self)

    def collidepoint(self, point):
        x, y = point
        return self.x <= x < self.right and self.y <= y < self.bottom

    def colliderect(self, other):
        ax = self.x
        ay = self.y
        ar = self.right
        ab = self.bottom
        bx = other.x
        by = other.y
        br = other.right
        bb = other.bottom
        return ax < br and ay < bb and ar > bx and ab > by

    def collidelist(self, rect_list):
        colliderect = self.colliderect
        for i, r in enumerate(rect_list):
            if colliderect(r):
                return i

    def collidelistall(self, rect_list):
        colliderect = self.colliderect
        return [i for i, r in enumerate(rect_list) if colliderect(r)]

    def collidedict(self, rect_dict):
        colliderect = self.colliderect
        for k, r in iter(rect_dict.items()):
            if colliderect(r):
                return k, r

    def collidedictall(self, rect_dict):
        colliderect = self.colliderect
        return [(k, r) for k, r in iter(rect_dict.items()) if colliderect(r)]

    def contains(self, rect):
        rect_x = rect.x
        rect_y = rect.y
        self_right = self.right
        self_bottom = self.bottom
        return (self.x <= rect_x and self.y <= rect_y and
                self_right >= rect.right and
                self_bottom >= rect.bottom and
                self_right > rect_x and
                self_bottom > rect_y)

    def normalize(self):
        if self.width < 0:
            self.x += self.w
            self.w = -self.w
        if self.h < 0:
            self.y += self.h
            self.h = -self.h

    def scale(self, factor_x, factor_y):
        x, y, w, h = self
        w *= factor_x
        h *= factor_y
        rect = Rect(x, y, w, h)
        rect.center = self.center
        return rect

    def scale_ip(self, factor_x, factor_y):
        c = self.center
        self.w *= factor_x
        self.h *= factor_y
        self.center = c
        return self

    def clamp(self, rect):
        if self.w >= rect.w:
            x = rect.x + rect.w / 2 - self.w / 2
        elif self.x < rect.x:
            x = rect.x
        elif self.x + self.w > rect.x + rect.w:
            x = rect.x + rect.w - self.w
        else:
            x = self.x

        if self.h >= rect.h:
            y = rect.y + rect.h / 2 - self.h / 2
        elif self.y < rect.y:
            y = rect.y
        elif self.y + self.h > rect.y + rect.h:
            y = rect.y + rect.h - self.h
        else:
            y = self.y

        return Rect(x, y, self.w, self.h)

    def clamp_ip(self, rect):
        if self.w >= rect.w:
            x = rect.x + rect.w / 2 - self.w / 2
        elif self.x < rect.x:
            x = rect.x
        elif self.x + self.w > rect.x + rect.w:
            x = rect.x + rect.w - self.w
        else:
            x = self.x

        if self.h >= rect.h:
            y = rect.y + rect.h / 2 - self.h / 2
        elif self.y < rect.y:
            y = rect.y
        elif self.y + self.h > rect.y + rect.h:
            y = rect.y + rect.h - self.h
        else:
            y = self.y

        self.x = x
        self.y = y

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [getattr(self.__sdl_rect, self.__i2a[i]) for i in (0, 1, 2, 3)[key]]
        else:
            return getattr(self.__sdl_rect, self.__i2a[key])

    def __setitem__(self, key, value):
        i2a = self.__i2a
        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            for i in (0, 1, 2, 3)[key]:
                setattr(self, i2a[i], value[i - start])
        else:
            setattr(self, i2a[key], value)

    def __iter__(self):
        r = self.__sdl_rect
        return iter((r.x, r.y, r.w, r.h))

    def __len__(self):
        return 4

    def __str__(self):
        return '<Rect({}, {}, {}, {})>'.format(*self)
