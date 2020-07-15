import unittest

import mimetypes
from .context import main, template

import filecmp

from os import path, listdir

from .utils import *

class TestTemplate(unittest.TestCase):
    def test_small_template(self):
        clean_output()
        template_path = path.join(TEST_DIRECTORY, "files/small.csv")
        templates = template.Templates(TEST_FOLDER_TEMPLATES)
        done_success, done_failed = main.templatize_csv_line_by_line(template_path, templates, output_directory= OUTPUT_FOLDER, verbose=False)
        
        self.assertEqual(main.number_of_lines(template_path), done_success, "the number of file created successfuly should be the same as the number of lines" )
        self.assertEqual(0, done_failed, "the number of file who failed creation should be 0" )
        self.assertEqual(len(listdir(OUTPUT_FOLDER)), main.number_of_lines(template_path), "the same number of elements should be created as the number of lines")
        # TODO check each output

if __name__ == '__main__':
    clean_output()
    unittest.main()