# -*- coding: utf-8 -*-
"""Activate virtualenv for current interpreter:

Use exec(open(this_file).read(), {'__file__': this_file}).

This can be used when you must use an existing Python interpreter, not the virtualenv bin/python.
"""
import os
import site
import sys

try:
    abs_file = os.path.abspath(__file__)
except NameError:
    raise AssertionError("You must use exec(open(this_file).read(), {'__file__': this_file}))")

bin_dir = os.path.dirname(abs_file)
base = os.path.realpath(os.path.join(bin_dir, '..'))  # the base is 1 directory above the bin_dir, supported strongly by the comment below for os.environ["VIRTUAL_ENV"]

# prepend bin to PATH (this file is inside the bin directory)
os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))
os.environ["VIRTUAL_ENV"] = base  # virtual env is right above bin directory

# add the virtual environments libraries to the host python import mechanism
# the site-packages are located 3 directories under base, as seen by the execution of the CLI
prev_length = len(sys.path)
for lib in os.listdir(base):
    lib_path = os.path.realpath(os.path.join(base, lib))
    print(f"lib_path : {lib_path}")
    if lib_path != bin_dir and os.path.isdir(lib_path):  # picks out possible candidates for the lib directory
        for ver in os.listdir(lib_path):
            ver_path = os.path.realpath(os.path.join(lib_path, ver))
            if os.path.isdir(ver_path):  # picks out the different python directories that may be present
                for site_path in os.listdir(ver_path):
                    path = os.path.realpath(os.path.join(ver_path, site_path))
                if os.path.isdir(path) and path not in sys.path:  # narrows to possible, unique candidates for the site-packages directory
                    if isinstance(path, str):
                        site.addsitedir(path)
                    elif isinstance(path, bytes):
                        site.addsitedir(path.decode("utf-8"))
                    else:
                        raise AttributeError(f"{site} is an invalid path")
sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

sys.real_prefix = sys.prefix
sys.prefix = base
