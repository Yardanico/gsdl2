from .sdllibs import sdl_lib
from .sdlffi import sdl_ffi
from .rect import Rect
from .color import Color
from .sdlconstants import SDL_BYTEORDER, SDL_BIG_ENDIAN


# static int set_at(SDL_Surface* surf, int x, int y, Uint32 color)
# {
# 	SDL_PixelFormat* format = surf->format;
# 	Uint8* pixels = (Uint8*)surf->pixels;
# 	Uint8* byte_buf, rgb[4];
#
# 	if(x < surf->clip_rect.x || x >= surf->clip_rect.x + surf->clip_rect.w ||
# 				y < surf->clip_rect.y || y >= surf->clip_rect.y + surf->clip_rect.h)
# 	return 0;
#
# 	switch(format->BytesPerPixel)
# 	{
# 		case 1:
# 			*((Uint8*)pixels + y * surf->pitch + x) = (Uint8)color;
# 			break;
# 		case 2:
# 			*((Uint16*)(pixels + y * surf->pitch) + x) = (Uint16)color;
# 			break;
# 		case 4:
# 			*((Uint32*)(pixels + y * surf->pitch) + x) = color;
# /*			  *((Uint32*)(pixels + y * surf->pitch) + x) =
# 				 ~(*((Uint32*)(pixels + y * surf->pitch) + x)) * 31;
# */			  break;
# 		default:/*case 3:*/
# 			SDL_GetRGB(color, format, rgb, rgb+1, rgb+2);
# 			byte_buf = (Uint8*)(pixels + y * surf->pitch) + x * 3;
# #if (SDL_BYTEORDER == SDL_LIL_ENDIAN)
#                         *(byte_buf + (format->Rshift >> 3)) = rgb[0];
#                         *(byte_buf + (format->Gshift >> 3)) = rgb[1];
#                         *(byte_buf + (format->Bshift >> 3)) = rgb[2];
# #else
#                         *(byte_buf + 2 - (format->Rshift >> 3)) = rgb[0];
#                         *(byte_buf + 2 - (format->Gshift >> 3)) = rgb[1];
#                         *(byte_buf + 2 - (format->Bshift >> 3)) = rgb[2];
# #endif
# 			break;
# 	}
# 	return 1;
# }


def drawhorzline(surface, color, x1, y1, x2):
    pixel = end = 0
    colorptr = color.sdl_color

    set_at = surface.set_at
    surf = surface.sdl_surface

    if x1 == x2:
        set_at(x1, y1, color)
        return

    pixel = surf.pixels + surf.pitch * y1
    if x1 < x2:
        end = pixel + x2 * surf.format.BytesPerPixel
        pixel += x1 * surf.format.BytesPerPixel
    else:
        end = pixel + x1 * surf.format.BytesPerPixel
        pixel += x2 * surf.format.BytesPerPixel
    if surf.format.BytesPerPixel == 1:
        pixel = sdl_ffi.cast('Uint8 *', pixel)
        colorptr = sdl_ffi.cast('Uint8 *', colorptr)
        while pixel <= end:
            pixel[0] = colorptr[0]
            pixel += 1
    elif surf.format.BytesPerPixel == 2:
        pixel = sdl_ffi.cast('Uint16 *', pixel)
        colorptr = sdl_ffi.cast('Uint16 *', colorptr)
        while pixel <= end:
            pixel[0] = colorptr[0]
            pixel += 2
    elif surf.format.BytesPerPixel == 3:
        pixel = sdl_ffi.cast('Uint8 *', pixel)
        colorptr = sdl_ffi.cast('Uint8 *', colorptr)
        # TODO: test me
        if SDL_BYTEORDER == SDL_BIG_ENDIAN:
            colorptr[0] <<= 8
        while pixel <= end:
            pixel[0] = colorptr[0]
            pixel[1] = colorptr[1]
            pixel[2] = colorptr[2]
            pixel += 3
    else:  # case 4
        pixel = sdl_ffi.cast('Uint32 *', pixel)
        colorptr = sdl_ffi.cast('Uint32 *', colorptr)
        # for(; pixel <= end; pixel+=4) {
        while pixel <= end:
            pixel[0] = colorptr[0]
            pixel += 1


def drawhorzlineclip(surf, color, x1, y1, x2):
    if y1 < surf.clip_rect.y or y1 >= surf.clip_rect.y + surf.clip_rect.h:
        return

    if x2 < x1:
        temp = x1
        x1 = x2
        x2 = temp

    set_at = surf.set_at

    x1 = max(x1, surf.clip_rect.x)
    x2 = min(x2, surf.clip_rect.x + surf.clip_rect.w - 1)

    if x2 < surf.clip_rect.x or x1 >= surf.clip_rect.x + surf.clip_rect.w:
        return

    if x1 == x2:
        set_at(surf, x1, y1, color)
    else:
        drawhorzline(surf, color, x1, y1, x2)


def drawvertline(surface, color, x1, y1, y2):
    pixel = end = 0
    colorptr = color.sdl_color
    surf = surface.sdl_surface
    pitch = surf.pitch

    set_at = surface.set_at

    if y1 == y2:
        set_at(surf, x1, y1, color)
        return

    pixel = surf.pixels + x1 * surf.format.BytesPerPixel
    if y1 < y2:
        end = pixel + surf.pitch * y2
        pixel += surf.pitch * y1
    else:
        end = pixel + surf.pitch * y1
        pixel += surf.pitch * y2

    if surf.format.BytesPerPixel == 1:
        pixel = sdl_ffi.cast('Uint8 *', pixel)
        colorptr = sdl_ffi.cast('Uint8 *', colorptr)
        while pixel <= end:
            pixel[0] = colorptr[0]
            pixel += pitch
    elif surf.format.BytesPerPixel == 2:
        pixel = sdl_ffi.cast('Uint16 *', pixel)
        colorptr = sdl_ffi.cast('Uint16 *', colorptr)
        while pixel <= end:
            pixel[0] = colorptr[0]
            pixel += pitch // 2
    elif surf.format.BytesPerPixel == 3:
        pixel = sdl_ffi.cast('Uint8 *', pixel)
        colorptr = sdl_ffi.cast('Uint8 *', colorptr)
        # TODO: test me
        if SDL_BYTEORDER == SDL_BIG_ENDIAN:
            colorptr[0] <<= 8
        while pixel <= end:
            pixel[0] = colorptr[0]
            pixel[1] = colorptr[1]
            pixel[2] = colorptr[2]
            pixel += pitch
    else:  # case 4
        # FIXME: this draws a dotted line
        pixel = sdl_ffi.cast('Uint32 *', pixel)
        colorptr = sdl_ffi.cast('Uint32 *', colorptr)
        while pixel <= end:
            pixel[0] = colorptr[0]
            pixel += pitch // 4


def drawvertlineclip(surface, color, x1, y1, y2):
    surf = surface.sdl_surface
    set_at = surface.set_at

    if x1 < surf.clip_rect.x or x1 >= surf.clip_rect.x + surf.clip_rect.w:
        return
    if y2 < y1:
        temp = y1
        y1 = y2
        y2 = temp
    y1 = max(y1, surf.clip_rect.y)
    y2 = min(y2, surf.clip_rect.y + surf.clip_rect.h - 1)
    if y2 - y1 < 1:
        set_at(x1, y1, color)
    else:
        drawvertline(surface, color, x1, y1, y2)


def circle(surface, color, center, radius, width=1):
    surf = surface.sdl_surface
    # rgba = color.sdl_color
    posx, posy = center
    t = l = b = r = 0
    loop = 0

    # surf = PySurface_AsSurface(surfobj);
    if surf.format.BytesPerPixel <= 0 or surf.format.BytesPerPixel > 4:
        raise Exception("unsupport bit depth for drawing")  # TODO

    # TODO
    # if(PyInt_Check(colorobj))
    #     color = (Uint32)PyInt_AsLong(colorobj);
    # else if(RGBAFromColorObj(colorobj, rgba))
    #     color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
    # else
    #     return RAISE(PyExc_TypeError, "invalid color argument");
    # pixel = sdl_lib.SDL_MapRGBA(surf.format, color.r, color.g, color.b, color.a)

    # TODO
    # if ( radius < 0 )
    #     return RAISE(PyExc_ValueError, "negative radius");
    # if ( width < 0 )
    #     return RAISE(PyExc_ValueError, "negative width");
    # if ( width > radius )
    #     return RAISE(PyExc_ValueError, "width greater than radius");

    # if(!PySurface_Lock(surfobj)) return NULL;
    surface.lock()

    if not width:
        draw_fillellipse(surf, posx, posy, radius, radius, color)
    else:
        # for (loop=0; loop<width; ++loop)
        for loop in range(width):
            draw_ellipse(surface, posx, posy, radius - loop, radius - loop, color)

    surface.unlock()

    l = max(posx - radius, surf.clip_rect.x)
    t = max(posy - radius, surf.clip_rect.y)
    r = min(posx + radius, surf.clip_rect.x + surf.clip_rect.w)
    b = min(posy + radius, surf.clip_rect.y + surf.clip_rect.h)
    return Rect(l, t, max(r - l, 0), min(b - t, 0))


def draw_ellipse(surface, x, y, rx, ry, color):
    # int ix, iy;
    # int h, i, j, k;
    # int oh, oi, oj, ok;
    # int xmh, xph, ypk, ymk;
    # int xmi, xpi, ymj, ypj;
    # int xmj, xpj, ymi, ypi;
    # int xmk, xpk, ymh, yph;

    # TODO: this is slow; it converts the color to a format-pixel each call
    def set_at(x, y, c):
        surf_set_at((x, y), c)

    surf_set_at = surface.set_at

    if rx == 0 and ry == 0:  # Special case - draw a single pixel
        set_at(x, y, color)
        return

    if rx == 0:  # Special case for rx=0 - draw a vline
        drawvertlineclip(surface, color, x, y - ry, y + ry)
        return

    if ry == 0:  # Special case for ry=0 - draw a hline
        drawhorzlineclip(surface, color, x - rx, y, x + rx)
        return

    # Init vars
    oh = oi = oj = ok = 0xFFFF
    if rx > ry:
        ix = 0
        iy = rx * 64
        # do {
        h = (ix + 16) >> 6
        i = (iy + 16) >> 6
        while i > h:
            j = (h * ry) / rx
            k = (i * ry) / rx

            if ok != k and oj != k or oj != j and ok != j or k != j:
                xph = x + h - 1
                xmh = x - h
                if k > 0:
                    ypk = y + k - 1
                    ymk = y - k
                    if h > 0:
                        set_at(xmh, ypk, color)
                        set_at(xmh, ymk, color)
                    set_at(xph, ypk, color)
                    set_at(xph, ymk, color)
                ok = k
                xpi = x + i - 1
                xmi = x - i
                if j > 0:
                    ypj = y + j - 1
                    ymj = y - j
                    set_at(xmi, ypj, color)
                    set_at(xpi, ypj, color)
                    set_at(xmi, ymj, color)
                    set_at(xpi, ymj, color)
                oj = j
            ix += iy / rx
            iy -= ix / rx

            h = (ix + 16) >> 6
            i = (iy + 16) >> 6
        # } while (i > h);
    else:
        ix = 0
        iy = ry * 64
        # do {
        h = (ix + 32) >> 6
        i = (iy + 32) >> 6
        while i > h:
            j = (h * rx) / ry
            k = (i * rx) / ry

            if oi != i and oh != i or oh != h and oi != h and i != h:
                xmj = x - j
                xpj = x + j - 1
                if i > 0:
                    ypi = y + i - 1
                    ymi = y - i
                    if j > 0:
                        set_at(xmj, ypi, color)
                        set_at(xmj, ymi, color)
                    set_at(xpj, ypi, color)
                    set_at(xpj, ymi, color)
                oi = i
                xmk = x - k
                xpk = x + k - 1
                if h > 0:
                    yph = y + h - 1
                    ymh = y - h
                    set_at(xmk, yph, color)
                    set_at(xpk, yph, color)
                    set_at(xmk, ymh, color)
                    set_at(xpk, ymh, color)
                oh = h
            ix += iy / ry
            iy -= ix / ry

            h = (ix + 32) >> 6
            i = (iy + 32) >> 6
        # } while(i > h);
