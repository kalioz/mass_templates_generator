import unittest

import mimetypes
from .context import template

import filecmp

from os import path

from .utils import *

class TestTemplate(unittest.TestCase):
    def test_creation_simple(self):
        t = template.Templates(TEST_FOLDER_TEMPLATES, load_in_memory=False, load_subfolder=False)

        self.assertIsNotNone(t.root_folder)
        self.assertTrue(len(t.template_dict.keys()) == 1, "only the root folder should be loaded (current keys = "+", ".join(t.template_dict.keys())+")")

    
    def test_creation_subfolder_check(self):
        t = template.Templates(TEST_FOLDER_TEMPLATES, load_in_memory=False, load_subfolder=True)

        self.assertTrue(len(t.template_dict.keys()) > 1, "the root folder and at least one subfolder should be loaded (current keys = "+", ".join(t.template_dict.keys())+")")

    def test_creation_bad_path(self):
        try:
            template.Templates("bad/path", load_in_memory=False, load_subfolder=True)
            self.fail("should fail at bad path")
        except FileNotFoundError:
            pass


    def test_template_loaded(self):
        t = template.Templates(TEST_FOLDER_TEMPLATES, load_in_memory=False, load_subfolder=False)

        self.assertGreater(len(t.template_dict['/'].keys()), 0, "there should be at least one template loaded under the (test) template root directory")

    
    def test_template_for_mimetype(self):
        t = template.Templates(TEST_FOLDER_TEMPLATES, load_in_memory=False, load_subfolder=False)
        self.assertGreater(len(t.get_templates_for_mimetype("image/png")), 0, "at least one png image should be under the (test) template root directory")

    def test_template_for_mimetype_missing(self):
        t = template.Templates(TEST_FOLDER_TEMPLATES, load_in_memory=False, load_subfolder=False)
        self.assertEqual(len(t.get_templates_for_mimetype("image/pdf")), 0)

if __name__ == '__main__':
    clean_output()
    unittest.main()