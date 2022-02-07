from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["solver_cython.pyx", "solver_cython8.pyx", "solver_cython9.pyx", "solver_cython10.pyx"]),
)
    
# Run: python setup.py build_ext --inplace