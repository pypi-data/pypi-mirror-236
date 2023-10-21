#!/bin/python
import subprocess
from distutils.core import setup, Extension

packagename = "dclpy"
dcllib=[]

output = subprocess.getoutput("dclconfig --ldlibs")
for token in output.strip().split():
    dcllib.append(token[2:])
#    kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])

#print (libraries)

setup(
    name='dclpy',
    version='0.0.5',
    ext_modules = [
        Extension(
            'dclpy',
            ['dclpy/dclpy_wrapper.c'],
            libraries=dcllib
        ),
    ],
)
