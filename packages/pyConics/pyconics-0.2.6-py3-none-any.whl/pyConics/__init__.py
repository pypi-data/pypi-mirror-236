#------------------------------------------------------------------
# __init__ dunder.
#
# It defines a package in Python.
#

#------------------------------------------------------------------
# read version from installed package
#
from importlib.metadata import version
__version__ = version( 'pyConics' )

#------------------------------------------------------------------
# Modules that belong to pyConics package.
#
from .origin import *
from .tolerance import *
from .point import *
from .line import *
from .functions import *
