from gsdl2 import gfx_lib, SDLError
from gsdl2.surface import Surface


def pixel(renderer, x, y, color):
    r, g, b, a = color
    x = int(x)
    y = int(y)
    draw_color = renderer.draw_color
    gfx_lib.pixelRGBA(renderer.sdl_renderer, x, y, r, g, b, a)
    renderer.draw_color = draw_color


def hline(renderer, x1, x2, y, color):
    r, g, b, a = color
    x1 = int(x1)
    x2 = int(x2)
    y = int(y)
    draw_color = renderer.draw_color
    gfx_lib.hlineRGBA(renderer.sdl_renderer, x1, x2, y, r, g, b, a)
    renderer.draw_color = draw_color


def vline(renderer, x, y1, y2, color):
    r, g, b, a = color
    x = int(x)
    y1 = int(y1)
    y2 = int(y2)
    draw_color = renderer.draw_color
    gfx_lib.vlineRGBA(renderer.sdl_renderer, x, y1, y2, r, g, b, a)
    renderer.draw_color = draw_color


def rectangle(renderer, rect, color):
    x1, y1, w, h = rect
    x1 = int(x1)
    y1 = int(y1)
    x2, y2 = int(x1 + w), int(y1 + h)
    r, g, b, a = color
    draw_color = renderer.draw_color
    gfx_lib.rectangleRGBA(renderer.sdl_renderer, x1, y1, x2, y2, r, g, b, a)
    renderer.draw_color = draw_color


def rounded_rectangle(renderer, rect, radius, color):
    assert radius >= 0.0
    x1, y1, w, h = rect
    x1 = int(x1)
    y1 = int(y1)
    x2, y2 = int(x1 + w), int(y1 + h)
    r, g, b, a = color
    draw_color = renderer.draw_color
    gfx_lib.roundedRectangleRGBA(renderer.sdl_renderer, x1, y1, x2, y2, radius, r, g, b, a)
    renderer.draw_color = draw_color


def box(renderer, rect, color):
    x1, y1, w, h = rect
    x1 = int(x1)
    y1 = int(y1)
    x2, y2 = int(x1 + w), int(y1 + h)
    r, g, b, a = color
    draw_color = renderer.draw_color
    gfx_lib.boxRGBA(renderer.sdl_renderer, x1, y1, x2, y2, r, g, b, a)
    renderer.draw_color = draw_color


def rounded_box(renderer, rect, radius, color):
    assert radius >= 0.0
    x1, y1, w, h = rect
    x1 = int(x1)
    y1 = int(y1)
    x2, y2 = int(x1 + w), int(y1 + h)
    r, g, b, a = color
    draw_color = renderer.draw_color
    gfx_lib.roundedBoxRGBA(renderer.sdl_renderer, x1, y1, x2, y2, radius, r, g, b, a)
    renderer.draw_color = draw_color


def line(renderer, startpos, endpos, color, width=1):
    assert width > 0
    r, g, b, a = color
    x1, y1 = startpos
    x1 = int(x1)
    y1 = int(y1)
    x2, y2 = endpos
    x2 = int(x2)
    y2 = int(y2)
    draw_color = renderer.draw_color
    if width == 1:
        gfx_lib.lineRGBA(renderer.sdl_renderer, x1, y1, x2, y2, r, g, b, a)
    else:
        gfx_lib.thickLineRGBA(renderer.sdl_renderer, x1, y1, x2, y2, width, r, g, b, a)
    renderer.draw_color = draw_color


def aaline(renderer, startpos, endpos, color):
    r, g, b, a = color
    x1, y1 = startpos
    x2, y2 = endpos
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    draw_color = renderer.draw_color
    gfx_lib.aalineRGBA(renderer.sdl_renderer, x1, y1, x2, y2, r, g, b, a)
    renderer.draw_color = draw_color


def circle(renderer, x, y, radius, color):
    assert radius >= 0.0
    r, g, b, a = color
    draw_color = renderer.draw_color
    x = int(x)
    y = int(y)
    gfx_lib.circleRGBA(renderer.sdl_renderer, x, y, radius, r, g, b, a)
    renderer.draw_color = draw_color


def arc(renderer, x, y, radius, start, end, color):
    assert radius >= 0.0
    r, g, b, a = color
    x = int(x)
    y = int(y)
    draw_color = renderer.draw_color
    gfx_lib.arcRGBA(renderer.sdl_renderer, x, y, radius, start, end, r, g, b, a)
    renderer.draw_color = draw_color


def aacircle(renderer, x, y, radius, color):
    assert radius >= 0.0
    r, g, b, a = color
    x = int(x)
    y = int(y)
    draw_color = renderer.draw_color
    gfx_lib.aacircleRGBA(renderer.sdl_renderer, x, y, radius, r, g, b, a)
    renderer.draw_color = draw_color


def filled_circle(renderer, x, y, radius, color):
    assert radius >= 0.0
    r, g, b, a = color
    x = int(x)
    y = int(y)
    draw_color = renderer.draw_color
    gfx_lib.filledCircleRGBA(renderer.sdl_renderer, x, y, radius, r, g, b, a)
    renderer.draw_color = draw_color


def ellipse(renderer, x, y, rx, ry, color):
    assert rx >= 0.0
    assert ry >= 0.0
    r, g, b, a = color
    x = int(x)
    y = int(y)
    rx = int(rx)
    ry = int(ry)
    draw_color = renderer.draw_color
    gfx_lib.ellipseRGBA(renderer.sdl_renderer, x, y, rx, ry, r, g, b, a)
    renderer.draw_color = draw_color


def filled_ellipse(renderer, x, y, rx, ry, color):
    assert rx >= 0.0
    assert ry >= 0.0
    r, g, b, a = color
    x = int(x)
    y = int(y)
    rx = int(rx)
    ry = int(ry)
    draw_color = renderer.draw_color
    gfx_lib.filledEllipseRGBA(renderer.sdl_renderer, x, y, rx, ry, r, g, b, a)
    renderer.draw_color = draw_color


def aaellipse(renderer, x, y, rx, ry, color):
    assert rx >= 0.0
    assert ry >= 0.0
    r, g, b, a = color
    x = int(x)
    y = int(y)
    rx = int(rx)
    ry = int(ry)
    draw_color = renderer.draw_color
    gfx_lib.aaellipseRGBA(renderer.sdl_renderer, x, y, rx, ry, r, g, b, a)
    renderer.draw_color = draw_color


def pie(renderer, x, y, radius, start, end, color):
    assert radius >= 0.0
    r, g, b, a = color
    x = int(x)
    y = int(y)
    draw_color = renderer.draw_color
    gfx_lib.pieRGBA(renderer.sdl_renderer, x, y, radius, start, end, r, g, b, a)
    renderer.draw_color = draw_color


def filled_pie(renderer, x, y, radius, start, end, color):
    assert radius >= 0.0
    r, g, b, a = color
    x = int(x)
    y = int(y)
    draw_color = renderer.draw_color
    gfx_lib.filledPieRGBA(renderer.sdl_renderer, x, y, radius, start, end, r, g, b, a)
    renderer.draw_color = draw_color


def trigon(renderer, x1, y1, x2, y2, x3, y3, color):
    r, g, b, a = color
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    draw_color = renderer.draw_color
    gfx_lib.trigonRGBA(renderer.sdl_renderer, x1, y1, x2, y2, x3, y3, r, g, b, a)
    renderer.draw_color = draw_color


def aatrigon(renderer, x1, y1, x2, y2, x3, y3, color):
    r, g, b, a = color
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    draw_color = renderer.draw_color
    gfx_lib.aatrigonRGBA(renderer.sdl_renderer, x1, y1, x2, y2, x3, y3, r, g, b, a)
    renderer.draw_color = draw_color


def filled_trigon(renderer, x1, y1, x2, y2, x3, y3, color):
    r, g, b, a = color
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    x3 = int(x3)
    y3 = int(y3)
    draw_color = renderer.draw_color
    gfx_lib.filledTrigonRGBA(renderer.sdl_renderer, x1, y1, x2, y2, x3, y3, r, g, b, a)
    renderer.draw_color = draw_color


def polygon(renderer, points, color):
    r, g, b, a = color
    vx, vy = zip(*points)
    vx = [int(i) for i in vx]
    vy = [int(i) for i in vy]
    n = len(vx)
    draw_color = renderer.draw_color
    gfx_lib.polygonRGBA(renderer.sdl_renderer, vx, vy, n, r, g, b, a)
    renderer.draw_color = draw_color


def aapolygon(renderer, points, color):
    r, g, b, a = color
    vx, vy = zip(*points)
    vx = [int(i) for i in vx]
    vy = [int(i) for i in vy]
    n = len(vx)
    draw_color = renderer.draw_color
    gfx_lib.aapolygonRGBA(renderer.sdl_renderer, vx, vy, n, r, g, b, a)
    renderer.draw_color = draw_color


def filled_polygon(renderer, points, color):
    r, g, b, a = color
    vx, vy = zip(*points)
    vx = [int(i) for i in vx]
    vy = [int(i) for i in vy]
    n = len(vx)
    draw_color = renderer.draw_color
    gfx_lib.filledPolygonRGBA(renderer.sdl_renderer, vx, vy, n, r, g, b, a)
    renderer.draw_color = draw_color


def textured_polygon(renderer, points, surface, texture_dx, texture_dy):
    vx, vy = zip(*points)
    vx = [int(i) for i in vx]
    vy = [int(i) for i in vy]
    n = len(vx)
    draw_color = renderer.draw_color
    gfx_lib.texturedPolygon(renderer.sdl_renderer, vx, vy, n, surface.sdl_surface, texture_dx, texture_dy)
    renderer.draw_color = draw_color


def bezier(renderer, points, s, color):
    r, g, b, a = color
    vx, vy = zip(*points)
    vx = [int(i) for i in vx]
    vy = [int(i) for i in vy]
    n = len(vx)
    draw_color = renderer.draw_color
    gfx_lib.bezierRGBA(renderer.sdl_renderer, vx, vy, n, s, r, g, b, a)
    renderer.draw_color = draw_color


def set_font(fontdata, cw, ch):
    gfx_lib.gfxPrimitivesSetFont(fontdata, cw, ch)


def set_font_rotation(rotation):
    gfx_lib.gfxPrimitivesSetFontRotation(rotation)


def character(renderer, x, y, c, color):
    r, g, b, a = color
    draw_color = renderer.draw_color
    gfx_lib.characterRGBA(renderer.sdl_renderer, x, y, c, r, g, b, a)
    renderer.draw_color = draw_color


def string(renderer, x, y, s, color):
    r, g, b, a = color
    draw_color = renderer.draw_color
    gfx_lib.stringRGBA(renderer.sdl_renderer, x, y, s, r, g, b, a)
    renderer.draw_color = draw_color


# Disable anti-aliasing (no smoothing).
SMOOTHING_OFF = 0

# Enable anti-aliasing (smoothing).
SMOOTHING_ON = 1


# Rotozoom functions

def rotozoom(surface, angle, zoom, smooth):
    sdl_surface = gfx_lib.rotozoomSurface(surface.sdl_surface, angle, zoom, smooth)
    if not sdl_surface:
        raise SDLError()
    return Surface(None, surface=sdl_surface)


def rotozoom_xy(surface, angle, zoomx, zoomy, smooth):
    return Surface(None, surface=gfx_lib.rotozoomSurfaceXY(surface.sdl_surface, angle, zoomx, zoomy, smooth))


def rotozoom_size(width, height, angle, zoom, dstwidth, dstheight):
    return gfx_lib.rotozoomSurfaceSize(width, height, angle, zoom, dstwidth, dstheight)


def rotozoom_size_xy(width, height, angle, zoomx, zoomy, dstwidth, dstheight):
    return gfx_lib.rotozoomSurfaceSizeXY(width, height, angle, zoomx, zoomy, dstwidth, dstheight)


# Zooming functions

def zoom(surface, zoomx, zoomy, smooth):
    return Surface(None, surface=gfx_lib.zoomSurface(surface.sdl_surface, zoomx, zoomy, smooth))


def zoom_size(width, height, zoomx, zoomy, dstwidth, dstheight):
    return gfx_lib.zoomSurfaceSize(width, height, zoomx, zoomy, dstwidth, dstheight)


# Shrinking functions

def shrink(surface, factorx, factory):
    return Surface(None, surface=gfx_lib.shrinkSurface(surface.sdl_surface, factorx, factory))


# Specialized rotation functions
def rotate_90_degrees(surface, numclockwiseturns):
    return Surface(None, surface=gfx_lib.rotateSurface90Degrees(surface.sdl_surface, numclockwiseturns))
