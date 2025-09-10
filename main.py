# -*- coding: utf-8 -*-
import os
import sys

# Add lib directory to Python path to use vendored dependencies
basedir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(basedir, "lib")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


from plugin import Main

if __name__ == "__main__":
    Main()
