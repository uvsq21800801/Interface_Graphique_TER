from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(ext_modules = cythonize('Solving/*.pyx', compiler_directives={'language_level' : "3"}),include_dirs=[numpy.get_include()])
setup(ext_modules = cythonize('Outputs/*.pyx', compiler_directives={'language_level' : "3"}),include_dirs=[numpy.get_include()])
setup(ext_modules = cythonize('Inputs/*.pyx', compiler_directives={'language_level' : "3"}),include_dirs=[numpy.get_include()])
setup(ext_modules = cythonize('Interfaces/*.pyx', compiler_directives={'language_level' : "3"}),include_dirs=[numpy.get_include()])
