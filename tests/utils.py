from shutil import rmtree
from os import path, mkdir

TEST_DIRECTORY = path.dirname(path.realpath(__file__))

TEST_FILES_CSV = [
    path.join(TEST_DIRECTORY, "files/small.csv")
]

TEST_FILES_TEMPLATES = [
    path.join(TEST_DIRECTORY, "templates/test.png"),
    path.join(TEST_DIRECTORY, "templates/test.jpg"),
    path.join(TEST_DIRECTORY, "templates/test.pdf")
]

TEST_FOLDER_TEMPLATES = path.join(TEST_DIRECTORY, "templates")

OUTPUT_FOLDER = path.join(TEST_DIRECTORY, "output")

def clean_output():
    rmtree(OUTPUT_FOLDER, ignore_errors=True)
    mkdir(OUTPUT_FOLDER)