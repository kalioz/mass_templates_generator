import unittest

import mimetypes
from .context import template

import filecmp

from os import path

from .utils import *

class TestTemplate(unittest.TestCase):
    def test_creation_simple(self):
        templates = [
            template.Template(i) for i in ["test.png", "test.pdf", "test.xml", "test.jpg", "test.jpeg", "i_do_not_exists.pdf"]
        ]
        for t in templates:
            self.assertEqual(mimetypes.guess_type(t.path), t.mimetype_encoding)
            self.assertFalse(t._Template__load_in_memory)
            self.assertIsNone(t.content)

    def test_creation_load_in_memory(self):
        t = template.Template("test.png", load_in_memory=True)
        self.assertTrue(t._Template__load_in_memory)
        self.assertIsNone(t.content, "template content should not be loaded at startup but at the first call to the template")

    def test_write_template_simple(self):
        for f in TEST_FILES_TEMPLATES:
            t = template.Template(f)
            output_path = path.join(OUTPUT_FOLDER, path.split(f)[1])
            t.write_to(output_path)

            self.assertIsNone(t.content)
            self.assertTrue(filecmp.cmp(f, output_path))
        
        clean_output()

    def test_write_template_load_in_memory(self):
        for f in TEST_FILES_TEMPLATES:
            t = template.Template(f, load_in_memory=True)
            output_path = path.join(OUTPUT_FOLDER, path.split(f)[1])
            
            self.assertIsNone(t.content)
            t.write_to(output_path)
            self.assertIsNotNone(t.content)
            self.assertTrue(filecmp.cmp(f, output_path))
        
        clean_output()


if __name__ == '__main__':
    clean_output()
    unittest.main()