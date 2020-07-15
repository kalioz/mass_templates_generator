
from sys import path as syspath
from os import path as ospath

syspath.insert(0, ospath.abspath(ospath.join(ospath.dirname(__file__), '..')))

import template
import main