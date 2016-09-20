from distutils.core import setup, Extension

eternity_subsidy_module = Extension('eternity_subsidy', sources = ['eternity_subsidy.cpp'])

setup (name = 'eternity_subsidy',
       version = '1.2',
       description = 'Subsidy function for Eternity',
       ext_modules = [eternity_subsidy_module])
