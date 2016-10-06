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

# if is_pygame_pkg:
#     from gsdl2.tests import test_utils
#     from gsdl2.tests.test_utils \
#          import test_not_implemented, unordered_equality, unittest
# else:
#     from test import test_utils
#     from test.test_utils \
#          import test_not_implemented, unordered_equality, unittest
from test import test_utils
from test.test_utils import expected_failure, unittest
import gsdl2
from gsdl2 import draw

################################################################################

class DrawModuleTest(unittest.TestCase):
    def setUp(self):
        (self.surf_w, self.surf_h) = self.surf_size = (320, 200)
        self.surf = gsdl2.Surface(self.surf_size, gsdl2.SRCALPHA)
        self.color = (1, 13, 24, 255)
    
    def test_rect__fill(self):
        # __doc__ (as of 2008-06-25) for gsdl2.draw.rect:
    
          # gsdl2.draw.rect(Surface, color, Rect, width=0): return Rect
          # draw a rectangle shape

        rect = gsdl2.Rect(10, 10, 25, 20)
        drawn = draw.rect(self.surf, self.color, rect, 0)

        self.assert_(drawn == rect)

        #Should be colored where it's supposed to be
        for pt in test_utils.rect_area_pts(rect):
            color_at_pt = self.surf.get_at(pt)
            self.assert_(color_at_pt == self.color)

        #And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(rect):
            color_at_pt = self.surf.get_at(pt)
            self.assert_(color_at_pt != self.color)

    @expected_failure
    def test_rect__one_pixel_lines(self):
        # __doc__ (as of 2008-06-25) for gsdl2.draw.rect:

          # gsdl2.draw.rect(Surface, color, Rect, width=0): return Rect
          # draw a rectangle shape
        rect = gsdl2.Rect(10, 10, 56, 20)
    
        drawn = draw.rect(self.surf, self.color, rect, 1)
        self.assert_(drawn == rect)

        #Should be colored where it's supposed to be
        for pt in test_utils.rect_perimeter_pts(drawn):
            color_at_pt = self.surf.get_at(pt)
            self.assert_(color_at_pt == self.color)

        #And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(drawn):
            color_at_pt = self.surf.get_at(pt)
            self.assert_(color_at_pt != self.color)

    def test_line(self):

        # __doc__ (as of 2008-06-25) for gsdl2.draw.line:

          # gsdl2.draw.line(Surface, color, start_pos, end_pos, width=1): return Rect
          # draw a straight line segment

        drawn = draw.line(self.surf, self.color, (1, 0), (200, 0)) #(l, t), (l, t)
        self.assert_(drawn.right == 201,
            "end point arg should be (or at least was) inclusive"
        )

        #Should be colored where it's supposed to be
        for pt in test_utils.rect_area_pts(drawn):
            self.assert_(self.surf.get_at(pt) == self.color)

        #And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(drawn):
            self.assert_(self.surf.get_at(pt) != self.color)

        #Line width greater that 1
        line_width = 2
        offset = 5
        a = (offset, offset)
        b = (self.surf_size[0] - offset, a[1])
        c = (a[0], self.surf_size[1] - offset)
        d = (b[0], c[1])
        e = (a[0] + offset, c[1])
        f = (b[0], c[0] + 5)
        lines = [(a, d), (b, c), (c, b), (d, a),
                 (a, b), (b, a), (a, c), (c, a),
                 (a, e), (e, a), (a, f), (f, a),
                 (a, a),]
        for p1, p2 in lines:
            msg = "%s - %s" % (p1, p2)
            if p1[0] <= p2[0]:
                plow = p1
                phigh = p2
            else:
                plow = p2
                phigh = p1
            self.surf.fill((0, 0, 0))
            rec = draw.line(self.surf, (255, 255, 255), p1, p2, line_width)
            xinc = yinc = 0
            if abs(p1[0] - p2[0]) > abs(p1[1] - p2[1]):
                yinc = 1
            else:
                xinc = 1
            for i in range(line_width):
                p = (p1[0] + xinc * i, p1[1] + yinc * i)
                self.assert_(self.surf.get_at(p) == (255, 255, 255), msg)
                p = (p2[0] + xinc * i, p2[1] + yinc * i)
                self.assert_(self.surf.get_at(p) == (255, 255, 255), msg)
            p = (plow[0] - 1, plow[1])
            self.assert_(self.surf.get_at(p) == (0, 0, 0), msg)
            p = (plow[0] + xinc * line_width, plow[1] + yinc * line_width)
            self.assert_(self.surf.get_at(p) == (0, 0, 0), msg)
            p = (phigh[0] + xinc * line_width, phigh[1] + yinc * line_width)
            self.assert_(self.surf.get_at(p) == (0, 0, 0), msg)
            if p1[0] < p2[0]:
                rx = p1[0]
            else:
                rx = p2[0]
            if p1[1] < p2[1]:
                ry = p1[1]
            else:
                ry = p2[1]
            w = abs(p2[0] - p1[0]) + 1 + xinc * (line_width - 1)
            h = abs(p2[1] - p1[1]) + 1 + yinc * (line_width - 1)
            msg += ", %s" % (rec,)
            self.assert_(rec == (rx, ry, w, h), msg)
        
    def todo_test_aaline(self):

        # __doc__ (as of 2008-08-02) for gsdl2.draw.aaline:

          # gsdl2.draw.aaline(Surface, color, startpos, endpos, blend=1): return Rect
          # draw fine antialiased lines
          # 
          # Draws an anti-aliased line on a surface. This will respect the
          # clipping rectangle. A bounding box of the affected area is returned
          # returned as a rectangle. If blend is true, the shades will be be
          # blended with existing pixel shades instead of overwriting them. This
          # function accepts floating point values for the end points.
          # 

        self.fail() 

    def todo_test_aalines(self):

        # __doc__ (as of 2008-08-02) for gsdl2.draw.aalines:

          # gsdl2.draw.aalines(Surface, color, closed, pointlist, blend=1): return Rect
          # 
          # Draws a sequence on a surface. You must pass at least two points in
          # the sequence of points. The closed argument is a simple boolean and
          # if true, a line will be draw between the first and last points. The
          # boolean blend argument set to true will blend the shades with
          # existing shades instead of overwriting them. This function accepts
          # floating point values for the end points.
          # 

        self.fail() 

    def todo_test_arc(self):

        # __doc__ (as of 2008-08-02) for gsdl2.draw.arc:

          # gsdl2.draw.arc(Surface, color, Rect, start_angle, stop_angle,
          # width=1): return Rect
          # 
          # draw a partial section of an ellipse
          # 
          # Draws an elliptical arc on the Surface. The rect argument is the
          # area that the ellipse will fill. The two angle arguments are the
          # initial and final angle in radians, with the zero on the right. The
          # width argument is the thickness to draw the outer edge.
          # 

        self.fail() 

    def todo_test_circle(self):

        # __doc__ (as of 2008-08-02) for gsdl2.draw.circle:

          # gsdl2.draw.circle(Surface, color, pos, radius, width=0): return Rect
          # draw a circle around a point
          # 
          # Draws a circular shape on the Surface. The pos argument is the
          # center of the circle, and radius is the size. The width argument is
          # the thickness to draw the outer edge. If width is zero then the
          # circle will be filled.
          # 

        self.fail() 

    def todo_test_ellipse(self):

        # __doc__ (as of 2008-08-02) for gsdl2.draw.ellipse:

          # gsdl2.draw.ellipse(Surface, color, Rect, width=0): return Rect
          # draw a round shape inside a rectangle
          # 
          # Draws an elliptical shape on the Surface. The given rectangle is the
          # area that the circle will fill. The width argument is the thickness
          # to draw the outer edge. If width is zero then the ellipse will be
          # filled.
          # 

        self.fail() 

    def todo_test_lines(self):

        # __doc__ (as of 2008-08-02) for gsdl2.draw.lines:

          # gsdl2.draw.lines(Surface, color, closed, pointlist, width=1): return Rect
          # draw multiple contiguous line segments
          # 
          # Draw a sequence of lines on a Surface. The pointlist argument is a
          # series of points that are connected by a line. If the closed
          # argument is true an additional line segment is drawn between the
          # first and last points.
          # 
          # This does not draw any endcaps or miter joints. Lines with sharp
          # corners and wide line widths can have improper looking corners.
          # 

        self.fail() 

    def todo_test_polygon(self):

        # __doc__ (as of 2008-08-02) for gsdl2.draw.polygon:

          # gsdl2.draw.polygon(Surface, color, pointlist, width=0): return Rect
          # draw a shape with any number of sides
          # 
          # Draws a polygonal shape on the Surface. The pointlist argument is
          # the vertices of the polygon. The width argument is the thickness to
          # draw the outer edge. If width is zero then the polygon will be
          # filled.
          # 
          # For aapolygon, use aalines with the 'closed' parameter. 

        self.fail() 

################################################################################

if __name__ == '__main__':
    unittest.main()
