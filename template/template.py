#!/usr/bin/python3

from shutil import copyfile
from os import listdir, path
from mimetypes import guess_type
from sys import stderr
from random import choice

class Template:
    content = None
    path    = None
    mimetype_encoding = None
    __load_in_memory   = False

    def __init__(self, template_path: str, load_in_memory=False):
        self.path     = template_path
        self.mimetype_encoding = guess_type(self.path)

        self.__load_in_memory = load_in_memory

    def load_in_memory(self):
        with open(self.path, "rb") as f:
            self.content = f.read()

    def write_to(self, output_path: str):
        # lazy loading
        if self.__load_in_memory and self.content is None:
            self.load_in_memory()

        if self.content is None:
            copyfile(self.path, output_path)
        else:
            with open(output_path, "wb") as fo:
                fo.write(self.content)


class Templates:
    def __init__(self, template_folder, load_in_memory = False, load_subfolder = True):
        self.root_folder = template_folder
        self.template_dict = {}

        if not path.exists(self.root_folder):
            raise FileNotFoundError(self.root_folder + " not found")

        if not path.isdir(self.root_folder):
            raise FileNotFoundError(self.root_folder + " is not a directory")

        self.load_templates(load_in_memory=load_in_memory, load_subfolder=load_subfolder)

    def load_templates(self, templates_subfolder=None, load_in_memory = False, load_subfolder = True):
        folder_path = self.root_folder if templates_subfolder is None else path.join(self.root_folder, templates_subfolder)

        if templates_subfolder is not None:
            self.template_dict[templates_subfolder] = {}
            templates_dict = self.template_dict[templates_subfolder]
        else:
            self.template_dict["/"] = {}
            templates_dict = self.template_dict["/"]

        for f in listdir(folder_path):
            full_path = path.join(folder_path, f)
            if path.isfile(full_path):
                tmp = Template(full_path, load_in_memory)
                if tmp.mimetype_encoding == None:
                    #TODO warning message
                    continue

                if tmp.mimetype_encoding not in templates_dict:
                    templates_dict[tmp.mimetype_encoding] = []
                templates_dict[tmp.mimetype_encoding].append(tmp)
            elif path.isdir(full_path) and load_subfolder:
                subfolder_path = f if templates_subfolder is None else path.join(templates_subfolder, f)
                self.load_templates(subfolder_path, load_in_memory=load_in_memory, load_subfolder=load_subfolder)

    def get_templates_for_mimetype(self, mimetype_encoding, subfolder=None):
        if type(mimetype_encoding) is str: # if it is a string, it is probably only the mimetype
            mimetype_encoding = (mimetype_encoding, None)
        key = "/"
        if subfolder is not None:
            if subfolder not in self.template_dict:
                raise Exception("templating subfolder "+ subfolder+" not found")
            key = subfolder

        return self.template_dict[key].get(mimetype_encoding, [])

    def get_random_template_for_mimetype(self, mimetype_encoding, subfolder=None):
        try:
            templates = self.get_templates_for_mimetype(mimetype_encoding, subfolder)
        except Exception as e:
            print(e, file=stderr)

        if len(templates) == 0:
            return None

        return choice(templates)

    def write_random_template_to(self, destination, mimetype_encoding=None, subfolder=None):
        if mimetype_encoding is None:
            mimetype_encoding = guess_type(destination)

        template = self.get_random_template_for_mimetype(mimetype_encoding, subfolder)

        if template is None:
            raise Exception("No templates found for {destination} (mimetype_encoding = f{mimetype_encoding}, subfolder = f{subfolder})".format(
              destination, mimetype_encoding, subfolder
            ))

        template.write_to(destination)
