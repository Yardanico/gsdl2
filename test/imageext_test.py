import os
import sys
if __name__ == '__main__':
    pkg_dir = os.path.split(os.path.abspath(__file__))[0]
    parent_dir, pkg_name = os.path.split(pkg_dir)
    is_pygame_pkg = (pkg_name == 'tests' and
                     os.path.split(parent_dir)[1] == 'gsdl2')
    if not is_pygame_pkg:
        sys.path.insert(0, parent_dir)
else:
    is_pygame_pkg = __name__.startswith('gsdl2.tests.')

if is_pygame_pkg:
    from gsdl2.tests.test_utils \
         import expected_error, test_not_implemented, example_path, unittest
else:
    from test.test_utils \
         import expected_error, test_not_implemented, example_path, unittest
import gsdl2, gsdl2.image, gsdl2.pkgdata
from gsdl2.compat import unicode_
from gsdl2.image import save as save_extended, load as load_extended
import os.path

class ImageextModuleTest( unittest.TestCase ):
    # Most of the testing is done indirectly through image_test.py
    # This just confirms file path encoding and error handling.
    def test_save_non_string_file(self):
        im = gsdl2.Surface((10, 10), 0, 32)
        self.assertRaises(TypeError, save_extended, im, [])

    def test_load_non_string_file(self):
        self.assertRaises(gsdl2.error, load_extended, [])

    def test_save_bad_filename(self):
        im = gsdl2.Surface((10, 10), 0, 32)
        u = u"a\x00b\x00c.png"
        self.assertRaises(gsdl2.error, save_extended, im, u)

    def test_load_bad_filename(self):
        u = u"a\x00b\x00c.png"
        self.assertRaises(gsdl2.error, load_extended, u)
        
    # No longer necessary since image and imageext have been merged.
    #def test_save_unknown_extension(self):
    #    im = gsdl2.Surface((10, 10), 0, 32)
    #    s = "foo.bar"
    #    self.assertRaises(gsdl2.error, save_extended, im, s)
        
    def test_load_unknown_extension(self):
        s = "foo.bar"
        self.assertRaises(gsdl2.error, load_extended, s)

    def test_load_unicode_path(self):
        u = unicode_(example_path("data/alien1.png"))
        im = load_extended(u)
    
    def test_save_unicode_path(self):
        temp_file = unicode_("tmpimg.png")
        im = gsdl2.Surface((10, 10), 0, 32)
        try:
            os.remove(temp_file)
        except EnvironmentError:
            pass
        self.assert_(not os.path.exists(temp_file))
        try:
            save_extended(im, temp_file)
            self.assert_(os.path.getsize(temp_file) > 10)
        finally:
            try:
                os.remove(temp_file)
            except EnvironmentError:
                pass

if __name__ == '__main__':
    unittest.main()
