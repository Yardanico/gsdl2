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

if is_pygame_pkg:
    from gsdl2.tests.test_utils import test_not_implemented, unittest
else:
    from test.test_utils import test_not_implemented, unittest

################################################################################

class SysfontModuleTest(unittest.TestCase):
    def todo_test_create_aliases(self):

        # __doc__ (as of 2008-08-02) for gsdl2.sysfont.create_aliases:

          # 

        self.fail() 

    def todo_test_initsysfonts(self):

        # __doc__ (as of 2008-08-02) for gsdl2.sysfont.initsysfonts:

          # 

        self.fail() 

    def todo_test_initsysfonts_darwin(self):

        # __doc__ (as of 2008-08-02) for gsdl2.sysfont.initsysfonts_darwin:

          # 

        self.fail() 

    def todo_test_initsysfonts_unix(self):

        # __doc__ (as of 2008-08-02) for gsdl2.sysfont.initsysfonts_unix:

          # 

        self.fail() 

    def todo_test_initsysfonts_win32(self):

        # __doc__ (as of 2008-08-02) for gsdl2.sysfont.initsysfonts_win32:

          # 

        self.fail()

################################################################################

if __name__ == '__main__':
    unittest.main()
